---
title: "GILL: Generating Images with Multimodal Language Models"
org: "Carnegie Mellon University (CMU)"
country: US
date: "2023-05"
type: paper
category: unified
tags: [unified, frozen-llm, interleaved, retrieval, image-generation, mapping-network, opt, stable-diffusion, neurips-2023]
url: "https://arxiv.org/abs/2305.17216"
arxiv: "https://arxiv.org/abs/2305.17216"
pdf_url: "https://arxiv.org/pdf/2305.17216"
github_url: "https://github.com/kohjingyu/gill"
hf_url: "https://huggingface.co/spaces/jykoh/gill"
modelscope_url: ""
project_url: "https://jykoh.com/gill"
downloaded: [arxiv-2305.17216.pdf, gill--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
GILL（论文题为 *Generating Images with Multimodal Language Models*，但正文将缩写定义为 "Generating Images with **Large** Language Models"，CMU，NeurIPS 2023）把一个**完全冻结**的文本 LLM（OPT-6.7B）同时桥接到 CLIP 图像编码器（输入侧）和 Stable Diffusion 文生图模型（输出侧），只训练约 **50M 参数**（约占 ~8B 总冻结参数的 0.6%），便在 **2 块 A6000、2 天**内得到首个能在任意图文交错输入下「生成文本 / 检索图像 / 生成新图像」并自行决定检索还是生成的多模态模型；其关键创新是轻量映射网络 **GILLMapper**（4 层 encoder-decoder Transformer），通过蒸馏把 LLM 的 `[IMG]` 隐状态对齐到 SD 文本编码器的输入空间。在 VIST（5 图文上下文）上 CLIP 相似度 0.641，显著超过同 backbone 的 Stable Diffusion（0.598）。

## 背景与定位
2022–2023 年「冻结 LLM + 视觉适配」一脉（[[frozen]] / Flamingo / [[blip-2]] / LLaVA）证明了只训练少量翻译参数就能让文本 LLM **读图**（图→文 embedding）。但这些模型只能**输出文本**。同期作者自己的前作 **FROMAGe**（Koh et al., ICML 2023）首次让冻结 LLM 在图文交错输入下**输出检索图像**，但只能从候选库里**检索**，无法生成库外的新图，且只用单个 `[RET]` token。

GILL 的定位就是补上「生成」这一环：它是**第一个**能在任意交错图文输入下同时产出「检索图 + 新生成图 + 文本」并交织成连贯多模态对话的模型。相对前置工作的核心改进有三点：
1. **生成而非只检索**——把冻结 LLM 接到现成的文生图扩散模型（[[stable-diffusion-1]] / [[latent-diffusion-ldm]]），突破检索候选集的天花板；
2. **高效**——训练时**不需要跑图像生成模型**（蒸馏目标是 SD 文本编码器的输出，可预计算），也**不需要交错图文数据**（仅用图文对 CC3M），对比 Flamingo（1535 TPU×15 天）/ RA-CM3（256 GPU×5 天）只需 2 GPU×2 天；
3. **检索 vs 生成的自动决策**——学一个决策分类器，按 prompt 决定该检索还是生成。

它代表了 2023 年「桥接式统一模型」的典型路线（embedding-space mapping），与后来走「原生统一 token / 自回归生成图像」的 [[chameleon]] / [[transfusion]] / [[emu]] 形成对照——GILL 不改动也不微调任何 backbone 权重，模块化、可即插即换更强的 LLM/视觉/生成模型。

## 模型架构
GILL 由一个**冻结的文本 LLM**居中，左右各接一个轻量桥接，再加一个生成网络和决策器组成。**所有预训练权重（LLM、CLIP、SD）全程冻结**，只训练桥接参数。

**Backbone（全部冻结）：**
- LLM：**OPT-6.7B**（[[opt]]），隐藏/输入 embedding 维度 e = 4096，自回归 decoder-only Transformer。
- 输入侧视觉编码器：**CLIP ViT-L**，提取图像特征 v_φ(x) 用于 captioning 与检索。
- 输出侧生成 backbone：**Stable Diffusion v1.5**，其文本编码器 T_ψ 输入序列长 L = 77、维度 768；推理时用 SD 的图像 decoder G_ψ 合成图。

**输入侧（读图，Learning to Process Images）：** 学一个**线性映射 W_cap ∈ R^{d×ke}**，把 CLIP 视觉特征映射成 k 个落在 LLM token embedding 空间的向量（论文用 **k = 4 个视觉 token** 表示一张输入图），直接当作 LLM 的输入 token，使 LLM 能消费任意交错的图文序列。

**输出侧（产图的触发，Learning to Produce Images）：** 在 LLM 词表中加入 **r 个特殊 `[IMG1]…[IMG{r}]` token**（可训练嵌入矩阵 E_img ∈ R^{r×e}，正文用 **r = 8**，消融显示 r≈4 即收敛）。FROMAGe 只用 1 个 token，作者发现**图像生成需要更细粒度的文本信息**，故推广到多 token。当 LLM 生成首个 `[IMG1]` 时，后续 `[IMG2]…[IMG{r}]` 强制连续生成；这 r 个 token 的**最后一层隐状态**就是后续检索/生成的条件。

**生成映射网络 GILLMapper（核心创新，可训练）：** 一个**轻量 4 层 encoder-decoder Transformer**，参数 ω。它以 r 个 `[IMG]` 隐状态 + **L 个可学习 query embedding**（q_1…q_L ∈ R^{L×m}，query 维 m = 512）为条件，输出 L×768 的序列去对齐 SD 文本编码器输出。可学 query 的作用是从 `[IMG]` 隐状态里抽取出长度恰为 L 的特征序列（思路类似 DETR 的 object query 和 BLIP-2 Q-Former 的 query）。论文消融表明：简单线性层 / 3 层 MLP / 单纯双向 Transformer encoder 都**显著差于** GILLMapper（尤其在 OOD 的 VIST 上无法泛化到含多图多文的长序列）。

**检索映射（可训练）：** 两个线性层 W_t2i ∈ R^{e×p}（把首个 `[IMG1]` 隐状态映到 p 维）与 W_i2t ∈ R^{d×p}（把池化视觉特征映到 p 维），检索 embedding 维 **p = 256**，用 InfoNCE 做图文对比检索。

**决策器（独立训练）：** 在 LLM 的 `[IMG]` 隐状态（+ 最大检索余弦相似度）上训一个**线性分类器**，推理时判定该「检索」还是「生成」。

**可训练参数总量约 50M**（W_cap、W_i2t、W_t2i、E_img、GILLMapper 的 ω 与 query），对比冻结的 ~8B；发布的 checkpoint（线性层 + `[IMG]` 嵌入）仅约 **96MB**。

## 数据
- **训练集：Conceptual Captions（CC3M）**，约 **3.3M 图文对**——这是 GILL 唯一的训练数据，**不需要交错图文数据**（这是相对 Flamingo/CM3 的关键效率优势）。
- **交错模拟：** 沿用 FROMAGe 的做法，训练时以 **0.5 的概率把两条随机样本拼接**（50% 单图文、50% 两段交错图文序列），让模型学会在图文序列中关注相关图像；并把 caption 拼接以鼓励跨样本注意力。
- **决策器标注数据：** 在 **PartiPrompts（P2，1,632 条）** 上自采人工标注。对每条 prompt，用 SD 生成一张图、用 CLIP ViT-L 从 CC3M 检索 top-1 图，**5 名标注者**各自判定哪张更贴合 prompt；取高一致性（≥4/5 一致，约 900 条）样本，按 67%/33% 划 600 训练 / 300 测试。标注（文本对齐版 + 真实感版）随代码开源（`data/PartiPromptsAllDecisions.tsv`）。
- **预计算加速：** SD 文本编码器对 CC3M caption 的 embedding **离线预计算**（`preprocess_sd_embeddings.py`），既是训练目标又省去训练时跑 SD。
- 清洗/配比/合成数据/美学过滤：**未披露**（直接用 CC3M 原集，未做额外重标注 re-captioning 或美学筛选）。论文在 Limitations（附录 A）坦承 CC3M 相对现代大规模图文数据集（引用 LAION-400M）偏小，是部分 prompt 生成不相关图的原因之一。

## 训练方法
**多任务联合目标（端到端一次训练，不分多阶段预训练）**，对一个 batch 求和：

`min  Σ_i [ l_c(x_i,y_i) + l_p(y_i) + l_g(y_i) + l_r(x_i,y_i) ]`

四项损失各司其职：
1. **l_c 字幕损失（学读图）：** 给定映射后的视觉 token，对 caption 做标准 next-token 负对数似然，训练 W_cap，把图映进 LLM token 空间。
2. **l_p `[IMG]` 触发损失：** 最大化在文本后生成首个 `[IMG1]` token 的似然，只更新 E_img，让模型学会**何时**该出图。
3. **l_g 生成蒸馏损失（核心）：** GILLMapper 输出与 SD 文本编码器输出 T_ψ(y) 的 **MSE（l2 距离）**——本质是从 SD 文本编码器**蒸馏**出一个「LLM 隐状态 → SD 输入空间」的映射。因目标可预计算、**训练时无需运行扩散模型 G_ψ**，训练极高效。
4. **l_r 检索损失：** 图文双向 **InfoNCE 对比损失**（温度 τ），训练 W_t2i / W_i2t。

**决策分类器**在主体收敛后**单独训练**（二元交叉熵）。生成目标本质是**蒸馏/回归对齐**，不是 diffusion/flow-matching/next-token 直接建图像像素——GILL 不学扩散过程本身，只学把文本表示「翻译」到现成扩散模型的条件空间。**无 RLHF/DPO、无一致性/步数蒸馏**（推理时直接用 SD 原生采样）。消融发现去掉检索损失 l_r 后生成几乎不掉点（CLIP 0.641→0.636），说明检索目标不构成瓶颈、模型容量足以兼顾两者。

**关键超参：** OPT-6.7B backbone；k=4 视觉 token；r=8 `[IMG]` token；GILLMapper query 维 m=512、检索维 p=256；bfloat16 精度；Adam（β1=0.9, β2=0.95），学习率 **1e-3**；**batch size 200、20K 迭代**。

## Infra（训练 / 推理工程）
- **训练算力：仅 2 块 NVIDIA A6000 GPU、约 48 小时（2 天）。** 这是论文反复强调的卖点——对比 Flamingo（1535 TPU×15 天）、RA-CM3（256 GPU×5 天），GILL 因「冻结 backbone + 仅 50M 可训练参数 + 训练不跑扩散模型 + 仅图文对数据」而极度省算力。
- **混合精度：** bfloat16。
- **分布式：** 代码用 PyTorch DDP（`--multiprocessing-distributed`，NCCL backend，world-size 1），并提示在某些机器需 `NCCL_P2P_DISABLE=1`。
- **预计算吞吐优化：** 离线预计算 SD 文本 embedding 与 CC3M 图像检索 embedding（约 3GB），训练/推理时直接查表。
- **推理形态：** LLM 自回归生成文本与 `[IMG]` token → 决策器判定检索/生成 → 检索走 CLIP 余弦最近邻，生成走 GILLMapper + SD decoder（标准 SD 采样步数，论文未报告具体步数/缓存/量化加速）。已发布 Gradio demo 与 HuggingFace Space（`jykoh/gill`），checkpoint 仅 96MB 便于分发。
- 推理量化/步数蒸馏/部署延迟：**未报告**。

## 评测 benchmark（把效果讲清楚）
评测核心是「能否利用更长 / 多模态上下文生成更贴合的图」，主指标 **CLIP 相似度（↑，生成图 vs 真值图的 CLIP ViT-L 余弦）** 与 **LPIPS（↓，感知距离）**。

**VIST（视觉故事，生成序列最后一张图，5 个随机种子均值，Table 1）：**

| 模型 | CLIP↑ 1 caption | 5 captions | 5 caps+4 imgs | LPIPS↓ 1 cap | 5 caps | 5 caps+4 imgs |
|---|---|---|---|---|---|---|
| GLIDE | 0.582 | 0.591 | — | 0.753 | 0.745 | — |
| Stable Diffusion（同 backbone） | 0.592 | 0.598 | — | 0.703 | 0.704 | — |
| **GILL（ours）** | 0.581 | **0.612** | **0.641** | 0.702 | **0.696** | **0.693** |

结论：单 caption 下 GILL 与 SD 持平（SD 略高）；**给全 5 caption 时 GILL 反超**（0.598→0.612）；**再加 4 张交错图像上下文时大幅提升到 0.641**——而 SD 根本无法处理交错图文输入。两者共用同一 SD 生成 backbone，差异来自 GILL 更强的 LLM 文本编码 + GILLMapper。

**VisDial（视觉对话，按对话轮数递增，Table 2）：**

| 模型 | CLIP↑ 1 round | 5 rounds | 10 rounds | LPIPS↓ 10 rounds |
|---|---|---|---|---|
| GLIDE | 0.562 | 0.595 | 0.587 | 0.799 |
| Stable Diffusion | 0.552 | 0.629 | 0.622 | 0.723 |
| **GILL** | 0.528 | 0.621 | **0.645** | **0.714** |

结论：短输入 SD 占优；**到完整 10 轮对话时 GILL 显著反超**（CLIP 0.622→0.645，LPIPS 0.723→0.714），印证其处理长对话文本的优势。

**上下文增益（Fig. 6）：** VIST 上 GILL 性能随上下文增加而提升；尤其「2 caption + 1 图」就显著超过「5 个纯文本 caption」，证明**多模态上下文 > 单模态上下文**。

**消融——映射网络（Table 3，CC3M FID↓ / VIST CLIP↑）：**

| 映射 | CC3M FID↓ | VIST CLIP↑ |
|---|---|---|
| SD（参考） | 13.94 | 0.598 |
| 线性层 | 15.50 | 0.500 |
| 3 层 MLP | 15.33 | 0.502 |
| Transformer encoder | 16.30 | 0.605 |
| **GILLMapper** | **15.31** | **0.641** |

GILLMapper 在 OOD 的 VIST 上 CLIP 远超线性/MLP（后者 ~0.50，几乎不可用），证明结构设计是生成能力的关键。

**消融——`[IMG]` token 数 r（Table 4）：** r=1/2/4/8 的 CC3M FID = 15.93 / 15.32 / 15.32 / 15.31、VIST CLIP = 0.631 / 0.629 / 0.642 / 0.641——两指标在 **r=4 处即基本饱和**（论文原文 "plateauing around r = 4"），r 太小因 GILLMapper 输入序列过短、表达力不足而变差。

**上下文图像检索（VIST，5 caps+4 imgs，Table 5）：** GILL R@1/R@5/R@10 = **20.3 / 45.0 / 53.7**，优于 FROMAGe（18.2 / 42.7 / 51.8）和 CLIP ViT-L（8.8 / 22.3 / 29.8）——说明加生成目标后检索能力**不退化反升**。

**检索 vs 生成决策器（附录 C，PartiPrompts，F1，类不均 201 gen/110 ret）：** 总是检索/总是生成/随机 = 0.267 / 0.389 / 0.451；启发式阈值 0.261–0.559；最终采用的**线性分类器 F1 0.547**（阈值 0.5），调参更省故被选用。

> 注：论文**未报告** GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / 人评 ELO 等现代 T2I 指标（2023-05 这些 benchmark 多数尚未流行）；其评测刻意聚焦「上下文依赖」而非纯美学/绝对图像质量，绝对 FID 略逊于直接 SD（15.31 vs 13.94）也属预期。

## 创新点与影响
**核心贡献：**
1. **embedding-space 桥接的统一生成范式**——首次证明可用极少参数把**两个文本编码器完全不同**的冻结模型（OPT vs SD 的 CLIP-style 文本编码器）的 embedding 空间对齐，从而让文本 LLM「驱动」现成扩散模型出图，无需端到端重训、训练时甚至不跑扩散模型。
2. **GILLMapper**——可学 query + 轻量 encoder-decoder Transformer 做隐状态到生成条件空间的蒸馏映射，远胜简单线性/MLP，且能泛化到 OOD 长交错序列。
3. **首个「检索 + 生成 + 文本」三合一交错多模态对话模型**，并用学习式决策器在推理时自动选检索或生成，突破检索候选集上限。
4. **极致效率与模块化**——2 GPU×2 天、50M 可训练参数、96MB checkpoint；backbone 即插即换，可随更强 LLM/视觉/生成模型升级。

**影响：** GILL 是 2023 年「冻结 LLM 桥接扩散模型」路线（FROMAGe → GILL → 后续 Emu/SEED/Mini-GPT5/DreamLLM 等「LLM 输出连续视觉条件再交给扩散 decoder」工作）的代表性奠基之一，把「多模态 LLM 能输出图像」从检索推进到生成，且确立了「用可学 query/mapper 把 LLM 隐状态对齐到扩散条件空间」这一被广泛沿用的接口设计。它与同期走「原生离散 token 自回归出图」的 Chameleon/SEED-LLaMA 路线并立，是统一多模态生成的两条主线之一。

**已知局限（作者明示）：** 继承 LLM 的幻觉与文本退化/重复（OPT-6.7B 对话连贯性不稳）；输入端**仅用 k=4 个视觉向量**表示一张图、信息受限，可能漏掉细节；训练数据 CC3M 偏小导致部分 prompt 生成不相关图；规模仅 6.7B，缺大模型能力；绝对图像真实感受限于 SD v1.5 backbone。作者指出扩大 LLM/视觉/生成 backbone、或微调生成 backbone（而非只训 GILLMapper）、加 RLHF 是明确的后续方向。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2305.17216
- arxiv_pdf: https://arxiv.org/pdf/2305.17216
- github: https://github.com/kohjingyu/gill
- project: https://jykoh.com/gill
- hf_space: https://huggingface.co/spaces/jykoh/gill
- hf_paper: https://huggingface.co/papers/2305.17216

## 一手源存档（sources/）
- [arxiv-2305.17216.pdf](https://arxiv.org/pdf/2305.17216)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/gill--readme.md)
