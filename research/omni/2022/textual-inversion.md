---
title: "An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion"
org: "Tel Aviv University / NVIDIA"
country: US
date: "2022-08"
type: paper
category: edit
tags: [personalization, textual-inversion, embedding-optimization, latent-diffusion, subject-driven, pseudo-word]
url: "https://arxiv.org/abs/2208.01618"
arxiv: "https://arxiv.org/abs/2208.01618"
pdf_url: "https://arxiv.org/pdf/2208.01618"
github_url: "https://github.com/rinongal/textual_inversion"
hf_url: ""
modelscope_url: ""
project_url: "https://textual-inversion.github.io/"
downloaded: [arxiv-2208.01618.pdf, textual-inversion--readme.md, textual-inversion--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Textual Inversion 用 3–5 张图、只优化**一个新的"伪词"嵌入向量 v\***（不改动任何模型权重），就能把一个特定物体或风格"注入"冻结的文生图模型词表，之后像普通单词一样组合进任意 prompt 做个性化生成；论文给出关键发现——**单个 word embedding 足以编码独特概念**，且其重建质量在 CLIP 语义空间上与"直接采样训练集真图"相当，同时编辑性远超多词/正则化等变体。

## 背景与定位
解决的问题：大规模文生图模型（[[dall-e-2]]、[[imagen]]、[[latent-diffusion-ldm]] 等）虽强，但**受限于用户用文字描述目标的能力**——你无法用语言精确描述"我家的猫""我童年的玩具""某位艺术家独有的画风"。把新概念塞进模型的传统做法都不理想：(1) 为每个新概念重训整模型代价过高；(2) 在少量样本上微调整模型会**灾难性遗忘**先验知识。

本工作的定位：把"引入新概念"重新框定为一个**inversion（反演）问题**——给定冻结的预训练文生图模型 + 一小撮（3–5 张）目标概念图片，在**文本编码器的词嵌入空间**里找到一个新的嵌入向量 v\*，使得 "A photo of S\*" 这类句子能重建出这组图。这个 v\* 对应一个论文记作 S\* 的"伪词（pseudo-word）"，可被任意复用、组合。

技术脉络上的位置：
- 思想源头是 **GAN inversion**（StyleGAN 把真图反演回 latent code）。作者把 GAN inversion 的多套工具（扩展 latent 空间 W+、渐进式多向量、靠近真实分布的正则化、pivotal tuning）系统地搬到扩散模型的文本嵌入空间做消融，结论是**很多 GAN 套路在这里无效甚至有害**，朴素的单向量反而最好。
- 与最相关的前作 PALAVRA（Cohen et al., 2022，同组）对比：PALAVRA 也在 CLIP 文本嵌入空间找伪词，但用的是**判别式（对比/检索）目标**，只需区分概念、无需重建细节，因此无法用于合成（图 5 显示其结果严重失真）。本工作改用**生成式视觉重建目标**，这是能做合成的关键。
- 它与**几乎同期**（2022-08）的 [[dreambooth]] 形成"个性化双子星"：Textual Inversion 只学嵌入、不动权重（极轻量、checkpoint 仅几 KB）；DreamBooth 微调整个 UNet（更高保真但 checkpoint 是整模型、易过拟合）。两者奠定了后续 subject-driven 生成与 LoRA 个性化的整条路线。

## 模型架构
本工作**不提出新架构**，而是在一个冻结的现成文生图模型上做嵌入优化。所用底座是 [[latent-diffusion-ldm]]（Rombach et al., 2021）公开的 **14 亿参数文生图 LDM**：

- **生成主干**：Latent Diffusion / DDPM——先用自编码器把图像 x 压到空间隐码 z = E(x)（用 KL 散度或向量量化正则），扩散模型在该隐空间去噪，最后解码器 D 还原图像。
- **text encoder cθ**：在该 LDM 里由 **BERT** 文本编码器实现（注意：不是后来 SD 的 CLIP-ViT-L 文本编码器；这版 LDM 用 BERT + LAION-400M 预训练）。
- **被反演的目标空间——词嵌入查表（embedding lookup）层**：文本先 tokenize 成词/子词索引，每个 token 通过查表得到连续嵌入向量 v。作者**只在这一步介入**：指定占位串 S\*，把它 tokenize 后对应的嵌入向量替换为一个**新学习的向量 v\***，相当于往词表"注入"了一个新词。下游 Transformer、扩散 UNet、解码器**全程冻结**。
- **可学参数量**：本质上就是**一个嵌入向量**（维度等于该模型的词嵌入维度，约几百~上千维，即论文标题"One Word"）。这是它最极致的轻量性——存盘只需保存这一个向量。
- **条件注入**：标准 LDM 的 cross-attention 文本条件，无任何改动。
- README 补充的工程细节：占位符默认用 `*`；merge_embeddings 脚本可把多个学到的伪词合并进一个 checkpoint，从而在同一句里同时引用多概念（如 "A photo of \* in the style of @"）。

## 数据
本工作**不做大规模数据训练**，"数据"指每个概念的小样本集：

- **每概念 3–5 张图**（典型），覆盖不同背景/姿态以利泛化。论文附录 B 做了训练集大小消融：从 1 张扫到 25 张，**~5 张是最佳点**——更多图会把嵌入推离真实词分布，损害编辑性，且重建几乎不再提升。
- **风格概念**：同样只给一小组共享风格的图，把训练模板换成 "A painting in the style of S\*"。
- **去偏（bias reduction）数据**：为有偏概念（如 "Doctor"/"CEO"）人工策划一个**更多样的小数据集**，学出一个"更公平"的新词替换原词，从而提升生成人物的性别/族裔多样性（图 8）。
- **训练用的中性上下文模板**：从 **CLIP ImageNet templates** 随机采样（"A photo of S\*"、"A rendition of S\*" 等），完整列表在附录。
- **评测里收集的人类 caption**：用 Mechanical Turk，每概念 10 条（5 短 ≤12 词 + 5 长 ≤30 词），作为"人类语言描述"基线。
- 底座 LDM 的预训练数据是 **LAION-400M**（Schuhmann et al., 2021），但那不是本工作训练的。

## 训练方法
核心就是**复用 LDM 原训练目标，只对一个嵌入向量做梯度下降**：

- **优化目标**：直接最小化 LDM 的去噪重建损失（式 1/2），但只对 v\* 求梯度，cθ 与去噪网络 εθ 全冻结：

  v\* = argmin_v 𝔼[ ‖ε − εθ(z_t, t, cθ(y)) ‖²₂ ]

  其中 y 是含占位符 S\* 的随机模板句。**注意这是一个重建任务**——正因目标是视觉重建（而非 PALAVRA 的判别目标），学到的嵌入才会去捕捉概念独有的细粒度视觉细节。
- **初始化**：v\* 用概念的**单 token 粗描述词**的嵌入初始化（如雕塑用 "sculpture"、猫用 "cat"；README 强调该 init_word 只是优化起点，不是最终占位符）。
- **关键超参（论文实现细节）**：
  - 硬件 **2× V100**，batch size 4，5000 步优化。
  - base learning rate 0.005，按 GPU 数 × batch size 缩放 → **有效学习率 0.04**（沿用 LDM 缩放规则）。
  - 学习率是**控制失真-编辑性权衡的旋钮**：调高 LR（2e-2，"High-LR"）→ 更像但更难编辑；调低 LR（1e-4，"Low-LR"）→ 更易编辑但更不像。论文展示单嵌入模型可沿这条权衡曲线滑动。
- **被验证为"无用甚至有害"的扩展（消融，第 5 节）**——这是论文重要的负面结论：
  - **多向量（2-word / 3-word）**：重建没明显变好，编辑性反而显著下降。
  - **渐进式多向量**（2000 步加第二个、4000 步加第三个向量）：同上。
  - **正则化**（把 v\* 拉向粗描述词嵌入的 L2）：增编辑性但损重建——只是在权衡曲线上换个点。
  - **per-image token**（共享 S\* + 每图私有 S_i 编码背景）：作者提出的新方案，但也未超过单向量。
  - 附录还试了 **bipartite DDIM 反演** 与 **pivotal tuning**（二阶段：先反演拿 pivot 码、再微调生成器）：bipartite 在 LDM 高 guidance（5–10）下无法保形、低 guidance 下又不贴 prompt；pivotal tuning 改善了形状但高 guidance 下编辑塌缩、出现伪影。两者都被列为"留待未来"。
- **加速/蒸馏**：本工作**无蒸馏**。论文明确指出主要工程短板是**优化慢——单概念约 2 小时**，并提议未来用一个 encoder 直接把图像集映射到文本嵌入来加速（这正是后续 encoder-based 个性化的方向）。

## Infra（训练 / 推理工程）
- **训练算力**：单概念 **2× V100、5000 步、约 2 小时**（论文"Limitations"明确给出）。README 称后续优化梯度存储/checkpointing 后，**显存需求与训练时间降低约 55%**。
- **存储成本极低**：产物只是一个嵌入向量（几 KB 量级），是该方法相对 DreamBooth（整模型 checkpoint）的核心工程优势——一个概念一个小文件，可任意叠加/分享。
- **推理**：标准 LDM 文生图采样。README 给的生成默认 **50 DDIM steps、guidance scale 10.0、ddim_eta 0.0**。
- **底座规模**：14 亿参数 LDM。论文强调方法**不依赖 LDM 任何架构特性**，可直接迁到更大模型（后续社区很快移植到 Stable Diffusion，README 中标注 SD 支持为 WIP）。
- 量化/并行/吞吐等大规模训练 infra **不适用**（本工作不训练大模型）。

## 评测 benchmark（把效果讲清楚）
论文用的是**自定义 CLIP 空间指标 + 用户研究**，无 FID/GenEval 这类标准盘（2022-08 时这些榜尚未普及）。**具体数字**：

- **两个评测轴**：
  - **重建（reconstruction）/ 失真**：对每概念用 "A photo of S\*" 生成 **64 张**图，计算它们与训练集真图在 **CLIP 空间的平均成对余弦相似度**（越高越像）。
  - **可编辑性（editability）**：对一组难度递增的编辑 prompt（换背景 "on the moon"、换风格 "An oil painting of"、组合 "Elmo holding a S\*"），每 prompt 用 **50 DDIM steps 生成 64 张**，算生成图的平均 CLIP 嵌入与**去掉占位符后的 prompt 文本**的 CLIP 嵌入余弦相似度（越高越贴 prompt）。
- **核心定量结论（图 10a）**：
  1. **单词模型（ours）的语义重建质量 ≈ 直接从训练集随机采样真图**——说明单向量已能高保真捕捉概念。
  2. **单词模型在编辑性上显著优于所有多词基线**，同时重建相当——印证"一个词就够"。
  3. 所有基线勾勒出一条**失真-编辑性权衡曲线**：越靠近真实词分布（正则化/更少伪词/更低 LR）越易编辑但越不像；越远离则越像但越难编辑。单嵌入模型可靠改 LR 在曲线上移动。
  4. **人类 caption 基线**（短/长描述替换 S\*）不仅不像，**编辑性也更差**——长 caption 让模型只盯着物体描述、忽略想要的场景设定（与 Paiss et al. 的"selective-similarity"现象一致）。
- **用户研究（图 10b）**：两份问卷各收 **600 份、共 1200 份**响应——按"与概念训练图相似度"和"与目标文本相似度"对 5 个模型排序。结果与 CLIP 指标一致，复现同一条重建-编辑权衡曲线，验证 CLIP 指标对齐人类偏好。
- **重要 caveat（作者自陈）**：CLIP 指标对**形状保持不敏感**——重建分数与真图持平要"打个折扣看"，方法在精确形状重建上仍有不足。
- **图像策展**：定性结果**部分策展**——每 prompt 生成 16 张（DALLE-2 为 6 张）人工选最好；附录提供未策展大图廊与失败案例。
- **未报告**：FID、CLIPScore（标准版）、GenEval、T2I-CompBench、DPG-Bench、HPSv2、ImageReward、ELO/Arena 等当下常用指标在本论文中均**未涉及**（时代所限）。

## 创新点与影响
**核心贡献**：
1. 提出"**个性化文生图（personalized text-to-image generation）**"这一任务范式：用自然语言把用户自带概念放进新场景。
2. 提出"**Textual Inversion**"——把概念反演成文本嵌入空间里的**单个伪词**，既抓高层语义又抓细粒度视觉细节，且**完全不动模型权重**。
3. 系统地用 **GAN inversion 视角**分析扩散模型的文本嵌入空间，证明其同样存在**失真-编辑性权衡**，但 GAN 的诸多反演技巧在此失效——朴素单向量最优。

**影响**：
- 是**轻量个性化（lightweight personalization）的奠基方法**：与同期 [[dreambooth]] 一起开创 subject-driven / 概念定制生成的整条研究线，直接启发后续 **encoder-based 个性化、LoRA 个性化、custom diffusion、P+/扩展嵌入空间**等大量工作。其"只学一个/几个 token 嵌入、模型冻结"的范式被无数下游沿用。
- 工程上**极致便携**：一个概念一个几 KB 嵌入，可任意叠加/分享/合并——成为 SD 生态早期社区分享"概念词"（embeddings）的事实标准之一。
- 顺带展示了"**用小而多样的策划集学新词来去偏**"这一有趣应用方向。

**已知局限（作者明确列出）**：
- **难精确还原形状**，更多是抓概念的"语义本质"——对艺术创作够用，对需高精度的任务不足。
- **优化慢**（单概念约 2 小时），作者建议用 encoder 直接映射来加速。
- **多概念组合受限**：能并行理解多个伪词，但难处理它们之间的关系（如"两个概念并排放置"会失败），归因于训练只见单概念居中场景。
- 社会影响：可能被用于伪造、放大训练数据偏见、未经许可学习艺术家画风侵权；但作者称当时身份保真度尚不足以构成伪造担忧，且去偏能力可正向利用。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2208.01618
- arxiv_pdf: https://arxiv.org/pdf/2208.01618
- project_page: https://textual-inversion.github.io/
- github: https://github.com/rinongal/textual_inversion

## 一手源存档（sources/）
- [arxiv-2208.01618.pdf](https://arxiv.org/pdf/2208.01618)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/textual-inversion--readme.md)
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/textual-inversion--project-page.md)
