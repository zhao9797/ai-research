---
title: "CM3Leon: Scaling Autoregressive Multi-Modal Models (Pretraining and Instruction Tuning)"
org: "Meta FAIR"
country: US
date: "2023-07"
type: paper
category: unified
tags: [autoregressive, token-based, retrieval-augmented, text-to-image, image-to-text, instruction-tuning, contrastive-decoding, cm3, chameleon-lineage]
url: "https://arxiv.org/abs/2309.02591"
arxiv: "https://arxiv.org/abs/2309.02591"
pdf_url: "https://arxiv.org/pdf/2309.02591"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://ai.meta.com/blog/generative-ai-text-images-cm3leon/"
downloaded: [arxiv-2309.02591.pdf, chameleon-cm3leon--blog.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
CM3Leon（读作 "Chameleon"）是 Meta FAIR 的**检索增强、token-based、decoder-only 多模态语言模型**，用一套"照搬自纯文本 LLM 的配方"（大规模检索增强预训练 + 多任务指令微调 SFT）同时做文→图与图→文生成；7B 模型以**比同类 transformer 方法少 5× 的训练算力**拿下 zero-shot MS-COCO **FID 4.88** 的当时 SOTA，首次证明自回归 token 模型在 T2I 上能**又省又强**地压过扩散模型，是后续 [[chameleon]]（早融合统一多模态）路线的直接前身。

## 背景与定位
2023 年文→图被扩散模型（[[latent-diffusion-ldm]] / Imagen / [[dall-e-2]]）统治，原因是性能强且算力开销适中；而 token-based 自回归模型（DALL-E 1、Parti）虽然全局一致性更好，却被认为**训练/推理太贵**。CM3Leon 的核心论点是：把原本为纯文本 LLM 开发的训练与推理 idea 移植过来，可以**翻转这个叙事**——自回归模型既能高效又能高性能，还能突破"只做 T2I"的格局，被指令微调成一个能干各种图文任务的通用模型。

技术脉络上 CM3Leon 站在三块工作之上：
- **CM3**（Aghajanyan et al. 2022，Causal Masked Multimodal）：提供了"因果掩码"目标，使一个 decoder 既能自回归续写又能 infilling。
- **RA-CM3**（Yasunaga et al. 2022，arXiv:2211.12561）：把**静态检索**到的多模态文档拼进每条训练样本的上下文，带来巨大训练效率增益。
- **混合模态 scaling laws**（Aghajanyan et al. 2023）：直接借用其学习率、batch size 等超参，保证训练曲线平滑稳定。

CM3Leon 在 RA-CM3 基础上做了三处简化与放大：精简目标函数、换成纯授权数据集、并把规模与数据多样性显著放大。它相比纯扩散路线的差异化在于**单模型双向生成 + CM3 目标天然支持免微调的 classifier-free guidance + 检索增强省算力**。

## 模型架构
**Backbone：decoder-only transformer（自回归 token 模型，非扩散、非 U-Net/DiT）**，结构沿用 OPT（Zhang et al. 2022）与 GPT-3（Brown et al. 2020），但做了如下修改：
- 去掉 bias 项、dropout，以及 layer norm 的可学习参数；
- 序列长度从 2048 提到 **4096**；
- 权重用截断正态初始化（mean 0、std 0.006、截断到 3σ）；输出层初始化为 0；可学习的**绝对位置嵌入**近零初始化（std 0.0002）。
- 三个尺寸：**350M / 760M / 7B**（层数 24/24/32，dmodel 1024/1536/4096）。
- 框架：**Metaseq**（facebookresearch/metaseq），实验追踪用 Aim。

**Visual tokenizer（关键）**：直接复用 Make-A-Scene（Gafni et al. 2022）的 image tokenizer——把一张 **256×256** 图编码成 **1024 个 token**，码本词表大小 **8192**（VQ 离散化）。文本侧自训了词表大小 **56320** 的 tokenizer（在 OPT 数据上训）。引入一个新特殊 token **`<break>`** 标记模态切换。

**没有独立的 text encoder（T5/CLIP）**：文本与图像统一进同一个 decoder 的 token 序列里，CLIP 仅出现在两处——(1) 作为**检索器**的 bi-encoder（ViT-B-32，编码 query/文档），(2) 推理时对 8 个候选生成做 **CLIP re-ranking**。

**条件注入方式**：靠 CM3 目标的 prompt 格式与 infilling 实现，不用 cross-attention。例如 caption→image 是从 `"Image of a chameleon:"` 续写；image→caption 是 `"Image of <mask>: [image] <infill>"`。

**检索增强架构**：稠密检索器（DPR 式 bi-encoder，CLIP-based）把多模态文档拆成文/图两部分分别用冻结的 CLIP 文/图编码器编码、取平均做文档向量，再用 **MIPS（最大内积搜索）** 在 memory bank 检索。采样检索文档时综合 **relevance / modality / diversity** 三因素：只用 relevance ≤ 0.9 的文档（过滤近重复），优先检索图文兼有的多模态文档，并用 **query dropout**（丢 query 里 20% 的 token）增加多样性。训练中每条 caption-image 对各按图、按文检索 2 个文档、随机选 3 个拼入上下文，等效把预训练 token 量放大约 **4×**。

## 数据
- **预训练全部用 Shutterstock 授权数据**：仅用 Shutterstock 的授权图像与文本，规避了图像版权/归属争议——博客与论文都强调这是**用与以往所有模型截然不同的数据分布仍达 SOTA**，是一次"transparency / 合规数据"示范。
- 数据集规模：**340M**（图文对，即检索 memory bank / 训练池大小，论文 Table 1 标注 "Dataset Size 340M"）。
- token 消耗：350M / 760M / 7B 分别训到 **1.4T / 1.9T / 2.4T tokens**（含检索增强带来的有效放大）；图→文方向训练只见过约 **3B 文本 token**（远少于 Flamingo 100B、OpenFlamingo 40B）。
- 数据处理：检索侧做 relevance≤0.9 去重、query dropout；图像 tokenize 到 256×256/1024 token。
- 美学/安全过滤：**论文未单列美学打分流程**；合规性主要靠"只用授权数据"这一前置约束实现，博客也提到训练数据可能带有偏见、需要透明度来逐步解决（未披露具体安全过滤 pipeline）。

## 训练方法
**两阶段配方，全程用同一个 CM3 next-token 目标（非 diffusion / 非 flow matching）：**

**阶段一 · 检索增强预训练**
- 目标函数：**CM3 因果掩码目标**——把输入里的若干 span mask 掉、搬到序列末尾做 infilling，整体仍是标准 next-token 预测损失 −log p(x)。这使一个 decoder 同时具备**自回归生成 + 任意位置 infilling**能力，且对图文都适用。
- 相对 RA-CM3 的修改：(1) **去掉 RA-CM3 对 query 图文对 loss 的 up-weighting**（该加权会损害 zero-shot 无检索生成）；(2) **禁止跨 `<break>` token 做 masking**（避免模型从图像中段乱起生成）。
- 超参（Table 3）：序列长 4096，全局 batch **8M tokens**，warmup **1500 步**，peak LR 分别 6e-4 / 5e-4 / 1.2e-4（350M/760M/7B）。760M 与 7B 跑满一个 epoch 后 resume 续训（LR 突增带来一小段 PPL 上扬）。三个模型 loss 全程稳降，未饱和。

**阶段二 · 多任务监督微调（SFT / 指令微调）**
- 把每个任务组织成**交错的图文示例**，仍用预训练同款 CM3 目标，把指令与输出拼接训练。
- 上/下采样平衡数据（阈值 3 / 0.3）；SFT 共处理约 **30B tokens**；LR 5e-5、warmup 150 步、batch 2M。
- SFT 任务覆盖两大类：
  - **可控图像生成**：文本引导编辑（用 InstructPix2Pix 方法 + 自有人脸过滤造 ~60 万样本）、图到图 grounded 生成（用 ControlNet 处理 Shutterstock 造 ~700 万样本，含 canny/hed/sketch/pose）、空间 grounded 生成（用 MS-COCO/OpenImage/Object365 造 ~300 万）、how-to-write 写字/logo（OCR 筛 Shutterstock ~20 万）。
  - **条件文本生成（视觉-语言）**：8 个任务——MS-COCO、Flickr30k、Image Paragraph、Localized Narratives、VQA2、VizWiz、OKVQA、ScienceQA，每任务多模板增强鲁棒性。

**解码方法创新（不是蒸馏，而是推理时增益）**：
- **Classifier-Free Guidance（CFG）**：把文本换成 `<mask>` token 即可得到无条件流，**无需额外微调**（CM3 目标天然支持），logit 上做 `uncond + αc·(cond − uncond)`。
- **Contrastive Decoding-K（CD-K）**：本文提出的对比解码变体。原始 CD 用强/弱两个模型；这里改为 **pEXP=有文本条件、pAMA=无文本条件**（自包含、单模型），并把候选集约束从"最大概率"放宽为"第 k 大概率"（避免退化成贪婪）。CD-K 与 CFG 效果相当但**互补**：把 `1/2 TopP + 1/2 CD-K` 混合采样能在增加生成数时持续压低 FID（两者单用都会停滞）。
- 推理仍走 DALL-E 式：每 prompt 生成 8 个候选，用 CLIP re-rank 选最优；CFG 最优权重在所有尺寸上一致。

## Infra（训练 / 推理工程）
- **训练算力**：350M/760M 用 **256 GPU**、7B 用 **512 GPU**（Table 3）；SFT 阶段 760M/7B 分别用 **64 / 128 张 80GB A100**。框架 Metaseq。
- **效率主张**：摘要原文称达到 SOTA FID 时训练算力仅为"同类 transformer 方法（comparable methods）"的 **1/5**（论文未逐一指名是哪个基线）；论文 Figure 2 用"等效 A100 小时 vs FID"曲线显示 CM3Leon 在 350M/760M/7B 三个尺寸上比 DALLE/SD/PARTI **scaling 更优**。
- **推理加速**：用 **FasterTransformer (FT)** 实现 + 模型并行（MP1/2/4/8）+ 量化（**INT8**）。Figure 11 给出不同 MP/dtype/batch 的吞吐曲线。
- **推理延迟（Figure 10，256×256 单图）**：CM3Leon-7B **BF16 11.8s、INT8 9.1s**；对比 Imagen 256² 9.1s、LDM(250 步) 18.5s、Parti-3B 6.4s、MUSE-3B 0.5s。即自回归推理延迟仍高于非自回归的 MUSE，但量化后可与扩散模型同量级。
- 部署形态：研究模型，**未开源权重 / 未提供 API**（博客明确为 research showcase，"未来会发布更多模型"）。

## 评测 benchmark（把效果讲清楚）

**文→图（zero-shot MS-COCO 30K，FID↓，每 prompt 生 8 候选 + CLIP re-rank）— Table 1：**

| 模型 | 训练检索 | 检索文档数(推理) | 数据规模 | 模型规模 | FID-30K |
|---|---|---|---|---|---|
| RA-CM3 | ✓ | 2 | 2.7B | 150M | 15.70 |
| Stable Diffusion | ✗ | – | 800M | 400M | 12.60 |
| KNN-Diffusion | ✓ | 10 | 400M | 70M | 12.50 |
| MUSE | ✗ | – | 3B | 500M | 7.88 |
| PARTI | ✗ | – | 20B | 5B | 7.23 |
| RE-IMAGEN | ✓ | 2 | 3.6B | 450M | 5.25 |
| **CM3Leon-7B** | ✓ | **0** | 340M | 7B | 10.82 |
| **CM3Leon-7B** | ✓ | **1** | 340M | 7B | 5.78 |
| **CM3Leon-350M** | ✓ | 2 | 340M | 350M | 14.20 |
| **CM3Leon-760M** | ✓ | 2 | 340M | 760M | 6.61 |
| **CM3Leon-7B** | ✓ | **2** | 340M | 7B | **4.88** |

要点：**7B + 2 检索文档拿下 SOTA FID 4.88**，优于 PARTI（7.23）与 RE-IMAGEN（5.25）。按 Table 1 列示，对比的 PARTI 行参数量 **5B**、训练数据 **20B**（数据约 CM3Leon 的 60×），其 FID 仍逊于 CM3Leon-7B（340M 数据）——检索增强让小数据模型胜出。检索是关键：同 7B 模型从 0→1→2 检索文档，FID 由 10.82→5.78→4.88，证明**检索为模型注入世界知识**对质量至关重要。

**消融**：CFG 最优权重在 350M/760M/7B 上一致；CD-K 与 CFG 单独都会随候选数增加而停滞，但 `1/2 TopP + 1/2 CD-K` 组合能持续降低 FID（解码方法互补性）。

**图→文（SFT 后 zero-shot，Table 2）：**

| 任务/指标 | OpenFlamingo-9B | Flamingo-9B | SFT-CM3Leon-7B |
|---|---|---|---|
| MS-COCO CIDEr (test) | 65.5 | 79.4 | 61.6 |
| VQA2 Acc (test-dev) | 43.5 | 51.8 | 47.6 |
| VizWiz Acc (test-dev) | – | 28.8 | **37.6** |
| OKVQA Acc (val) | – | 44.7 | 23.8 |
| Image Paragraph CIDEr | – | – | 10.5 |
| VisDial NDCG (val) | – | 48.4 | 22.6 |

> 注：Table 2 原文中 OpenFlamingo-9B 仅报告 MS-COCO/VQA2 两项（其余为 `-`）；VizWiz 28.8、OKVQA 44.7、VisDial 48.4 均为 **Flamingo-9B** 的值，CM3Leon 与 OpenFlamingo 的对比仅限 MS-COCO/VQA2。OpenFlamingo 数字基于 validation set。

要点：尽管 CM3Leon 只见过 **~3B 文本 token**（Flamingo 100B、OpenFlamingo 40B），却在 MS-COCO 字幕与 VQA2 上与 **OpenFlamingo** 同量级（VQA2 47.6 反超其 43.5、MS-COCO 61.6 略逊其 65.5），并在 **VizWiz 上比 Flamingo 高近 10 分**（37.6 vs 28.8）。

**定性能力**：复杂组合对象（戴草帽+霓虹墨镜的仙人掌）、长尾实体（Khachkar 亚美尼亚石刻十字）、历来难画的手与文字；以及单模型完成文本引导编辑、结构引导编辑、object-to-image、segmentation-to-image。**超分**：可外挂一个单独训练的 super-resolution 阶段把输出提到更高分辨率（博客有展示，论文图像本体仍为 256×256 原始输出）。

## 创新点与影响
**核心贡献**
1. **首次把纯文本 LLM 的整套配方（检索增强预训练 + 多任务指令微调）原样搬到 token-based 多模态生成**，证明 tokenizer-based transformer 能像扩散模型一样高效训练。
2. **打破"自回归图像模型太贵"的成见**：以 5× 更少算力达到 T2I SOTA（FID 4.88），并量化推理把延迟拉到与扩散同量级。
3. **自包含的对比解码 CD-K** 与免微调 CFG：单模型即可自我引导，提升图文生成质量。
4. **合规数据示范**：全程仅用 Shutterstock 授权数据仍达 SOTA，给"版权友好生成模型"提供了证据。
5. **真正的单模型双向多任务**：文→图、图→文、编辑、分割、grounded 生成统一在一个 decoder 里。

**影响**：CM3Leon 是 Meta **[[chameleon]]**（2024，早融合统一多模态 token 模型）路线的直接前身——把"图文统一进单一自回归 token 序列"的思路推向 SOTA，也呼应了后续 token-based 统一生成（如自回归 + VQ 的 unified omni 模型）的潮流，与 DiT/扩散主线形成长期的"自回归 vs 扩散"路线之争。

**已知局限**：(1) 自回归逐 token 解码延迟仍高于非自回归 MUSE（0.5s vs 9–12s）；(2) 强烈依赖检索 memory bank，无检索时 FID 明显变差（10.82）；(3) 图像分辨率仅 256×256，高清需外挂超分；(4) 图→文能力受限于仅 3B 文本 token，OKVQA/VisDial 等仍逊于 Flamingo；(5) 权重未开源，安全/偏见过滤细节未充分披露。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.02591
- arxiv_pdf: https://arxiv.org/pdf/2309.02591
- blog (Meta AI 官方): https://ai.meta.com/blog/generative-ai-text-images-cm3leon/

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2309.02591.pdf
- ../../../sources/omni/2023/chameleon-cm3leon--blog.md
