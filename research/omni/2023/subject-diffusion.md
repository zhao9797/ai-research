---
title: "Subject-Diffusion: Open Domain Personalized Text-to-Image Generation without Test-time Fine-tuning"
org: "OPPO AI Center"
country: China
date: "2023-07"
type: paper
category: edit
tags: [subject-driven, personalization, tuning-free, multi-subject, diffusion, sdd-dataset, cross-attention-control, siggraph2024]
url: "https://arxiv.org/abs/2307.11410"
arxiv: "https://arxiv.org/abs/2307.11410"
pdf_url: "https://arxiv.org/pdf/2307.11410"
github_url: "https://github.com/OPPO-Mente-Lab/Subject-Diffusion"
hf_url: ""
modelscope_url: ""
project_url: "https://oppo-mente-lab.github.io/subject_diffusion/"
downloaded: [arxiv-2307.11410.pdf, arxiv-2307.11410.txt, subject-diffusion--readme.md, subject-diffusion--train-sh.txt]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Subject-Diffusion 是 OPPO AI Center 提出的**开放域、免测试时微调、单张参考图即可单/双主体个性化生成**框架（SIGGRAPH 2024）：靠自建的 **7600 万图、2.22 亿实体**的结构化数据集 SDD（含 bbox + 分割掩码 + 重写 caption），把"文本+主体图像语义"在文本编码器前融合、再用 adapter 注入密集 patch 特征 + 位置掩码、并用 cross-attention map 控制实现双主体，单主体在 DreamBench 上 DINO=0.711（超过需 5 张图微调的 DreamBooth 0.668）、人像 ID 保真 0.605（超 FastComposer 0.514）。

> 说明：worklist 元数据将机构标为 "Alibaba"，但论文四位作者（Jian Ma / Junhao Liang / Chen Chen / Haonan Lu）与代码仓库 OPPO-Mente-Lab 均明确归属 **OPPO AI Center（深圳）**，本页以一手论文为准记为 OPPO。

## 背景与定位
个性化 / 主体驱动 T2I 当时有两条主线：
- **测试时微调（test-time fine-tuning）**：[[textual-inversion]] 调 token embedding、[[dreambooth]] 调整个 UNet、Custom Diffusion 只调 cross-attn 的 K/V，需要每个主体 3–5 张图 + 单独训练，难以实际部署。
- **免微调（tuning-free）**：在大规模或域内数据上重训基座，推理零样本。但此前要么只能**单概念**（UMM-Diffusion、[[blip-diffusion]]、ELITE），要么**限定域**（人脸 / 猫 / 狗，如 FastComposer、InstantBooth、Taming Encoder），要么 fidelity 与文本对齐做不好。

Subject-Diffusion 的定位：**第一个同时满足"开放域 + 免微调 + 单参考图 + 支持双主体"四项能力**的框架。它建立在 [[latent-diffusion-ldm]] / Stable Diffusion 之上（因其可扩展性与开源），并大量借鉴 [[gligen]] 的 grounded 注入方式、FastComposer 的局部注意力思路、以及作者团队自己的 GlyphDraw。关键洞察来自前作观察：参考图信息容易"压过"用户文本输入而损害创造性编辑，故需在 fidelity（保真）与 editability（可编辑）之间显式做平衡。

## 模型架构
基座为 **Stable Diffusion（latent diffusion, U-Net + VAE）**，代码中基座路径为 `model_base`。三大设计支柱：

**1) 融合文本编码器（Fusion text encoder）**
- 设计专用 prompt 模板：`"[text prompt], the [subject label 0] is [PH_0], the [subject label 1] is [PH_1], ..."`，PH_* 为主体图占位符。
- 与 FastComposer / ELITE（**冻结**文本编码器）不同，本文选择**在文本编码器之前**就把文本与图像信息融合，并**重训整个 CLIP 文本编码器**——把文本编码器第一层 embedding 中的实体 token，替换为对应位置的图像主体 **CLIP "CLS" embedding**，然后端到端重训。作者实验证明"先融合再整体重训"比"后融合"自洽性更强。

**2) 密集图像 + 物体位置控制（Dense image and object location control）**
- 把**分割后的主体图**喂入 **CLIP 图像编码器**得到 **256 个 patch feature token**（只保留主体、丢背景）。
- 把 patch embedding 与主体 bbox 坐标的 **Fourier 变换位置编码**融合：`h_e = MLP([v, Fourier(l)])`，v 是 256 个 patch token，l 是坐标。
- 仿 [[gligen]]，在 U-Net **每个 Transformer block 的 self-attention 与 cross-attention 之间**插入一个**可学习 adapter 层**：`L_a := L_a + β·tanh(γ)·S([L_a, h_e])`，其中 β 为常数权衡因子，γ 为初始化为 0 的可学习标量（gated 残差，保证训练初期不破坏基座），S 为 self-attention 算子。
- **位置-区域控制（location-area control）**：为单主体生成一张二值掩码特征图，与原始 image latent **拼接**；多主体则叠加各主体二值图再拼接。推理时该二值图可由用户指定 / 自动检测 / 随机生成。这步用于解耦前景/背景分布、防止训练坍塌。

**3) Cross-attention map 控制（多主体）**
- 基于 Prompt-to-Prompt 的结论：cross-attention map 反映各 text token 对应物体的空间位置。
- 训练期加正则：让实体 token（如 "dog"、"[cls_0]"、"cat"、"[cls_1]"）的 cross-attention map 逼近该实体的分割掩码，在 h_l = w_l ∈ {32,16,8} 的层上施加 **L1 偏差惩罚**：`L_attn = (1/N) Σ_k Σ_l |CA_l(z_t, y_k) − M_k|`，M_k 是第 k 个物体的分割掩码。目的是防止双主体相互"串扰/泄漏"。

**可训练范围**（据 train.py 默认参数）：`train_unet=True`、`train_clip_text=True`、`train_transformer=True`，而 **`train_clip_visual=False`（CLIP 图像编码器冻结）**。论文进一步说明：训练 U-Net 时只激活 cross-attention 的 **K/V 层**和 **adapter 层**，冻结其余，以让模型聚焦学习 adapter。

**条件注入总览**：text encoder 融合"分割图全局 embedding v_g + 文本 token embedding t_y"产出 C；adapter 接收"局部 patch 特征 v + bbox 坐标 l"；二值掩码 l_m 在 latent 维度拼接（经一个 conv_in 调维）。

## 数据
核心贡献之一：自建 **Subject-Diffusion Dataset (SDD)**，基于 LAION-5B（具体取 LAION-Aesthetics 子集），三步自动标注流水线：

- **(a) 重写 caption + 抽实体标签**：LAION 原 caption 质量差（含无关/无意义文本），用 **BLIP-2** 对每张图重新生成 caption；再用 **spaCy** 做词性分析，把名词当作实体 tag（re-captioning + POS 抽取）。
- **(b) 检测 + 分割**：把实体 tag 作为 prompt 喂 **Grounding DINO** 做开集检测得到各物体 bbox；bbox 再作为 prompt 喂 **SAM** 得到对应分割掩码。
- **(c) 结构化**：把 图文对 + 检测框 + 分割掩码 + 标签 组合成多模态结构化数据，再经过精细过滤策略。

**规模**：**76M 图像、222M 实体、162K 常见物体类别**——远超 OpenImages（约 1M 图）。覆盖广泛的场景、实体类别与拍摄条件（分辨率、光照等）。

代码 `train.sh` 显示训练实际消费的是 webdataset tar 分片 `aesthetics_tar_sam/{00000..44487}.tar`（约 4.4 万分片，"_sam" 即带 SAM 掩码标注）。

**安全/美学过滤**：未在论文中单独披露具体安全/NSFW 过滤细节（仅说基于 LAION-Aesthetics 并"应用精细过滤策略"）。训练数据当时**未公开**（README TODO 中"Release training data"未勾选）。

## 训练方法
- **训练目标**：标准 LDM ε-prediction（DDPM 噪声预测）+ attention 正则项：
  `L = E[‖ε − ε_θ(z_t, t, y, x_s, l, l_m)‖²₂] + λ_attn · L_attn`，
  其中 x_s 为分割主体图、l 为 bbox 坐标、l_m 为掩码、λ_attn 为权重超参。**无 flow matching / 无蒸馏 / 无 RLHF / DPO**——是单阶段端到端监督训练，非多阶段对齐。
- **可训练模块**：U-Net（仅 cross-attn 的 K/V + 新增 adapter）、整个 CLIP 文本编码器、MLP/proj 融合模块；CLIP 图像编码器冻结。
- **关键超参（来自 train.sh / train.py，一手代码）**：
  - 学习率 **3e-5**，weight decay 0，**warmup 1000 步**，**max_epoch 10**。
  - 分辨率 **512×512**（hr_size 512）。
  - 优化器：PyTorch-Lightning 默认（代码用 LearningRateMonitor），未显式标注 AdamW 但为 diffusers/Lightning 常规配置。
  - 推理：图像编码器输出 256 patch token；推理 attention map 分辨率 resolution=32。
- **trick**：adapter 的 gated 残差（γ 初始为 0）保证不破坏 SD 先验；location-area 二值掩码防坍塌；cross-attn map 正则解多主体串扰。
- **文本-图像插值（推理技巧）**：用 `"[text prompt], the [subject] is [PH]"` 模板，在扩散步数 t > αT 时用带图像条件的 ε_θ(...,x_s,...)，之后只用纯文本条件 ε_θ(...,y)；调 α 即可在 fidelity 与 editability 间平滑插值（说明主体高层信息在反向扩散早期就被注入）。

## Infra（训练 / 推理工程）
来自一手训练脚本 `train.sh`（论文正文未披露算力）：
- **集群规模**：SLURM，`NNODES=4` × `GPUS_PER_NODE=8` = **32 张 GPU**（脚本里 `#SBATCH --gres=gpu:8`、排除节点 dgx050，推测为 DGX/A100 级别，但**具体卡型未明确披露**）。
- **并行 / 显存**：**DeepSpeed ZeRO Stage 1**（PL `deepspeed_stage_1`），**fp16（precision 16）**混合精度。
- **批大小**：micro batch 8/GPU → 全局 batch **256**（32 GPU × 8）。
- **数据加载**：WebDataset tar 分片流式读取，num_workers 2，shard_width 5，resample_train。
- **通信**：NCCL（`NCCL_P2P_LEVEL=NVL`、`NCCL_IB_DISABLE=1`），torch.distributed.run 启动。
- **GPU·时 / 训练总时长 / 吞吐 / 量化部署**：**未披露**。推理无步数蒸馏/缓存/量化等专门加速（沿用 SD 标准采样）。

## 评测 benchmark（把效果讲清楚）
评测协议：DreamBench（30 类）+ 自建 OpenImages 测试集（296 类、每类两张实体图，约 10× DreamBench 主体数）。指标：图像对齐 **DINO**、**CLIP-I**；文本对齐 **CLIP-T**。每个 prompt 生成 6 图，共 4500 图。

**单主体（DreamBench，Table 1，ZS=零样本免微调）**：

| 方法 | 类型 | DINO | CLIP-I | CLIP-T |
|---|---|---|---|---|
| Real Images | - | 0.774 | 0.885 | - |
| Textual Inversion | FT | 0.569 | 0.780 | 0.255 |
| DreamBooth | FT | 0.668 | 0.803 | 0.305 |
| Custom Diffusion | FT | 0.643 | 0.790 | 0.305 |
| ELITE | ZS | 0.621 | 0.771 | 0.293 |
| BLIP-Diffusion | ZS | 0.594 | 0.779 | 0.300 |
| IP-Adapter | ZS | 0.667 | **0.813** | 0.289 |
| **Subject-Diffusion** | ZS | **0.711** | 0.787 | 0.293 |

- **DINO=0.711 为全表最高**，甚至超过需 5 张图微调的 DreamBooth（0.668）。CLIP-I（0.787）略低于 IP-Adapter（0.813），CLIP-T 与其它免微调法持平/略高。
- **OpenImages 测试集**（主体数约 10×）：DINO 0.668 / CLIP-I 0.782 / CLIP-T 0.303，证明开放域泛化。

**双主体（DreamBench，30 组双主体，Table 2）**：

| 方法 | 类型 | DINO | CLIP-I | CLIP-T |
|---|---|---|---|---|
| DreamBooth | FT | 0.430 | 0.695 | 0.308 |
| Custom Diffusion | FT | 0.464 | 0.698 | 0.300 |
| **Subject-Diffusion** | ZS | **0.506** | 0.696 | **0.310** |

- 在 DINO 与 CLIP-T 上**显著超过**两种微调法，CLIP-I 持平；对比方法常"漏掉一个主体"或"两主体外观泄漏混淆"。

**人像生成（Table 4，FastComposer 协议）**：

| 方法 | 参考图数 | ID Preser.↑ | Prompt Consis.↑ |
|---|---|---|---|
| FastComposer | 1 | 0.514 | 0.243 |
| IP-Adapter | 1 | 0.520 | 0.201 |
| **Subject-Diffusion** | 1 | **0.605** | 0.228 |

- ID 保真 **0.605**，比在专门人像数据上训练的 FastComposer 高 **0.091**；但 prompt 一致性略低 0.015（作者承认模型在难 prompt 时偏向保真）。

**用户研究（Table 5，1–5 分，对比开源可比方法）**：Subject-Diffusion ID 保真 **3.4748**（远超 ELITE 1.79 / IP-Adapter 2.22 / BLIP-Diffusion 1.93），prompt 一致性 2.2689（与 BLIP-Diffusion 相当，但 ELITE 在文本一致性上更强 2.53）。作者指出客观指标无法完全反映人类偏好，且 fidelity 与 prompt 一致性互相制约。

**消融（Table 3，关键结论）**：
- **去 adapter 的 256 patch 特征**：单主体 DINO 暴跌 0.711→0.534——高保真主要靠它。
- **去 location 控制（物体掩码）**：全指标下降。
- **去 image "CLS" 特征**：DINO 0.711→0.637，保真大降。
- **去 attention map 控制**：双主体 DINO 0.506→0.500（对双主体提升明显），单主体小幅受益——主要作用是防双主体混淆。
- **去 bbox 坐标（(d) w/o box coordinates）**：**双主体显著变差**（DINO 0.506→0.464、CLIP-I 0.696→0.687），说明 **bbox 坐标利于多主体**（论文：引入 bbox 使双主体 DINO +0.042、CLIP-I +0.09、CLIP-T +0.005）；但**单主体反而变好**（DINO 0.711→**0.732↑**、CLIP-I 0.787→0.810），即对单主体而言 bbox 信息冗余、掩盖关键细节，去掉后更好。
- **数据消融**：仅用 OpenImages（600 类）重训，DINO 0.711→0.664，但仍超 ELITE/BLIP-Diffusion——证明大规模数据 + 结构本身都重要。

## 创新点与影响
**核心贡献**：
1. **自动化结构化数据流水线 + SDD 数据集**：BLIP-2 重写 caption + spaCy 抽实体 + Grounding DINO 检测 + SAM 分割，产出 76M 图 / 222M 实体 / 162K 类的开放域主体数据集——把"基础视觉大模型组合做自动标注"用到极致，为后续 tuning-free 主体生成提供数据范式。
2. **首个**同时实现"开放域 + 免测试时微调 + 单参考图 + 单/双主体"四合一的框架。
3. **多层次条件注入**：文本编码器前融合 + 整体重训、adapter 注入密集 patch + Fourier 位置、二值掩码 latent 拼接、cross-attn map 掩码正则——这套"粗位置 + 细 patch + attention 约束"组合是它在保真与多主体上领先的关键。

**影响**：把"用现成检测/分割/captioning 大模型自动构建带 grounding 的海量主体数据，再做免微调个性化"这条路线推到大规模，与同期 IP-Adapter、BLIP-Diffusion 共同奠定 tuning-free subject-driven 生成范式，被后续大量个性化/可控生成工作引用对比；SIGGRAPH 2024 收录。

**已知局限**（作者自述）：
- 难以编辑用户输入图中的**属性与配饰**（applicability 受限）。
- **超过两个主体**时大概率无法生成和谐图像。
- fidelity 与 prompt 一致性互相制约，难同时拉满（偏向保真）。
- 训练数据未开源；推理无加速优化。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2307.11410
- arxiv_pdf: https://arxiv.org/pdf/2307.11410
- github: https://github.com/OPPO-Mente-Lab/Subject-Diffusion
- project_page: https://oppo-mente-lab.github.io/subject_diffusion/ （JS 图廊，无额外文本，未抓取正文）
- doi (SIGGRAPH 2024): https://doi.org/10.1145/3641519.3657469

## 一手源存档（sources/）
- [arxiv-2307.11410.pdf](https://arxiv.org/pdf/2307.11410)  （arXiv 原文 PDF，不入 git）
- [arxiv-2307.11410.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/arxiv-2307.11410.txt)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/subject-diffusion--readme.md)
- [train-sh.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/subject-diffusion--train-sh.txt)
