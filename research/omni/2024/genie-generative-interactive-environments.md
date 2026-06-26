---
title: "Genie: Generative Interactive Environments"
org: "Google DeepMind"
country: US
date: "2024-02"
type: paper
category: video
tags: [world-model, video, latent-action, unsupervised, maskgit, st-transformer, vq-vae, foundation-model, playable, agents]
url: "https://arxiv.org/abs/2402.15391"
arxiv: "https://arxiv.org/abs/2402.15391"
pdf_url: "https://arxiv.org/pdf/2402.15391"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://sites.google.com/view/genie-2024/home"
downloaded: [arxiv-2402.15391.pdf, genie--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Genie 是 Google DeepMind 提出的**第一个"生成式可交互环境"**——一个完全从无标注互联网视频以**无监督**方式学到的、可逐帧用动作控制的**可玩世界模型（playable world model）**。它由三件套组成（**时空视频 tokenizer + 无监督潜动作模型 LAM + MaskGIT 自回归动力学模型**），全部基于内存高效的 **ST-transformer**，最终模型 **10.7B 参数**（其中动力学模型 10.1B），在 **3 万小时 2D 平台跳跃游戏视频**上训练，可被任意一张图（文生图结果、手绘草图、真实照片）prompt 成一个能"走进去玩"的虚拟世界。ICML 2024 最佳论文，开创了 Genie 2/3 与"世界模型视频生成"路线。

## 背景与定位
当时（2024 初）生成式 AI 在语言、图像、视频上都已有 ChatGPT、[[latent-diffusion-ldm]]/[[imagen-3]]、[[sora]] 这类成果，但**视频生成模型的"可交互性"与语言模型差距巨大**：视频模型只能在 video-level 用文本/首帧条件化，无法**逐帧响应用户动作**。传统 World Model（Ha & Schmidhuber 的 World Models、Dreamer、GameGAN、DriveGAN、GAIA-1、UniSim）虽然支持动作条件的 next-frame 预测，但**都需要"视频 + 动作标签"配对数据**（甚至加文本），而动作标注昂贵、难规模化、跨域不通用。

Genie 的核心命题：**能不能只用海量无标注互联网视频，学出一个既能生成新世界、又能逐帧交互的基础世界模型？** 论文用一张表把自己和前作区分开：

| Model Class | 训练数据 | 可控性 |
|---|---|---|
| World Models | Video + Actions | Frame-level |
| Video Models | Video + Text | Video-level |
| **Genie** | **Video（仅视频）** | **Frame-level** |

它也是对 Playable Video Generation（PVG, Menapace 2021/2022）的泛化：PVG 在领域特定的静态例子上学潜动作，Genie 则丢掉这些归纳偏置、换成可规模化的通用方法，从而支持"用任意 prompt 生成全新环境"。

## 模型架构
三大组件全部采用 **ST-transformer（spatiotemporal transformer）**，灵感来自 Xu et al. 2020。关键点是把全时空注意力拆成**交错的空间层 + 时间层**：空间层只在单帧的 `H×W` token 内做自注意力，时间层只在 `T` 个时间步的同一 token 上做（带因果掩码）。这样**主导计算量的空间注意力随帧数线性增长而非平方增长**，使长序列视频可承受。每个 ST block 只保留**一个 FFW（放在空间+时间层之后），刻意省掉 post-spatial FFW**——论文发现这能把省下的容量挪去 scale 其它组件、显著提升效果。

**1. 潜动作模型 LAM（Latent Action Model，300M）** — 无监督学动作。编码器吃进 `x₁:t` 全部历史帧 **加上下一帧 `x_{t+1}`**，输出连续潜动作 `ã₁:t`；解码器只看历史帧 + 潜动作去重建 `x̂_{t+1}`。用 **VQ-VAE 目标**把动作量化成**极小的离散码本**：`|A|=8`（8 个潜动作），patch_size=16，codebook embedding 32 维。码本刻意做小是为了**保证人类可玩性 + 强制可控性**——因为解码器只能拿到历史和潜动作，`ã_t` 必须编码"过去到未来最有意义的变化"。LAM 编码器/解码器各 20 层、d_model=1024、16 头。**注意：除 VQ 码本外，整个 LAM 在推理时被丢弃**，由用户输入的动作（0~7 整数）替代，"像学一个新手柄上的按键"。

**2. 视频 tokenizer（ST-ViViT，200M）** — VQ-VAE 把 `T` 帧视频压成离散 token `z₁:T`。与只做空间压缩的前作（MAGVIT/CogVideo/NÜWA）不同，Genie 在**编码器和解码器都用 ST-transformer**，让每个 `z_t` 因果地包含 `x₁:t` 的时序信息，提升生成质量。相比 Phenaki 的 C-ViViT（全时空注意力、随帧数平方增长、易过拟合），ST-ViViT **计算随帧数线性增长**。patch_size=4，codebook=1024 codes、embedding 32 维。编码器 12 层 d_model=512；**解码器更大（20 层 d_model=1024）**——论文发现 scale 解码器比 scale 编码器更划算。

**3. 动力学模型（Dynamics Model，10.1B）** — decoder-only **MaskGIT** transformer（Chang et al. 2022）。在每个时刻 `t`，吃 tokenized 视频 `z₁:t-1` + **stop-grad 的潜动作 `ã₁:t-1`**，预测下一帧 token `ẑ_t`，用交叉熵损失对齐 ground-truth token。一个**重要 trick**：动作不是常见做法那样"拼接到对应帧"，而是作为**加性 embedding（additive embedding）**注入 LAM 和动力学模型——论文实测这显著提升了生成的可控性。最终动力学模型 **48 层、d_model=5120、36 头**。

**推理（动作可控视频生成）**：玩家给一张首帧图 `x₁` → tokenizer 编成 `z₁` → 玩家选一个离散动作 `a₁∈[0,8)` → 查 VQ 码本得 `ã₁` → 动力学模型预测 `z₂` → 解码回像素 → 不断重复自回归生成。每帧采样跑 **25 步 MaskGIT，temperature=2，random sampling**。

**训练流程**：两阶段——**先单独训 video tokenizer**，再用其 token **联合训 LAM（直接从像素）+ 动力学模型（在 token 上）**。用 **bfloat16 + QK-norm** 稳定大规模训练。

## 数据
- **Platformers 数据集（主模型）**：从公开互联网视频按规则过滤——标题含 2D 平台跳跃游戏关键词、含动作词（如 "speedrun"/"playthrough"）、不含否定词（如 "movie"/"unboxing"）。切成 **16 秒、10 FPS、160 帧** 的片段、**160×90 分辨率**。初始 **5500 万条 16 秒视频片段**（论文摘要/引言把整体语料量级表述为"逾 20 万小时互联网游戏视频"；55M×16s≈24.4 万小时为据此换算的近似上界，论文正文未单列原始集小时数）。
- **质量过滤管线**：发现大量低质视频拖累效果，采用类似 VPT（Baker 2022）的**学习型分类器**：① 团队手标 1 万条视频（约 10 人时），打 1–5 分；② 删掉 2–4 分的模糊样本，把 5 分当 good、1 分当 bad，训一个 **11M 参数 ResNet18 二分类器**；③ 按预测+置信度的决策规则决定保留。**最终精选集 680 万条视频、超 3 万小时**（仅原始量的 ~10%）。
- **数据质量 > 数量**的实证：精选集虽只有原始 10%，但训出的模型 FVD 更好（580M 模型：原始集 61.4 → 精选集 54.8）。
- **Robotics 数据集（验证通用性）**：复用 RT-1 的数据——约 13 万条机器人演示 + 一批仿真数据 + 20.9 万条真实机器人 episode（来自 QT-Opt）。**不使用任何动作标签，纯当视频处理**。
- **不发布**训练数据、数据样例与模型权重（出于安全与版权审慎考量）。

## 训练方法
- **目标函数**：tokenizer 用标准 VQ-VAE 重建目标；LAM 用 VQ-VAE 式重建 `x̂_{t+1}`；动力学模型用 **MaskGIT 的掩码 token 交叉熵**——训练时按 Bernoulli 掩码率（**在 0.5~1 间均匀采样**）随机掩盖输入 token `z₂:T-1`，让模型学填补。整体是"标准自回归视频生成 pipeline"，**不是 diffusion / flow matching**，而是**离散 token 的掩码生成 + 自回归**。
- **多阶段**：① 训 video tokenizer（300k steps，AdamW + cosine decay，max_lr=min_lr=3e-4，warmup 10k）；② 联合训 LAM + 动力学模型。**无 RLHF / DPO / 偏好对齐**（这是世界模型，不是对齐的对话/图像生成模型）。
- **关键超参/trick**：bfloat16、QK-norm（稳大规模训练）；动作用加性 embedding 而非拼接；潜动作对动力学模型 stop-grad；动力学模型优化器 max_lr=3e-5/min_lr=3e-6、weight_decay=1e-4、warmup 5k。
- **未涉及**蒸馏 / consistency / LCM / 步数蒸馏等扩散加速（架构本身就是离散 MaskGIT，25 步采样）。

## Infra（训练 / 推理工程）
- **最终 Genie 模型**：10.1B 动力学模型，**batch size 512、训练 125k steps、256 块 TPUv5p**；总参数 10.7B，**训练 token 数 942B**，单次前向 FLOPs ≈ **6.6×10²²**。给网站演示另训了一个把 token 映射到 **360p** 的更大 decoder。
- **并行/分布式**：scaling 实验用 **batch 并行 + ZeRO stage-3 分片**（Rajbhandari 2020），大模型再叠 **tensor 并行**（Megatron, Shoeybi 2019）。
- **硬件与耗时（scaling 系列，均 200k steps / batch 256 / 750B token）**：41M 用 64×TPUv2 跑 3 天；2.7B 用 256×TPUv3 跑 16 天（6.91×10²¹ FLOPs）。batch-size 实验里 448 batch 用了 **TPUv5p**。tokenizer 在 64×TPUv2/v3 上训。
- **推理形态**：约 **1 FPS**（论文明确这是局限，需后续提速到可交互帧率）；每帧 25 步 MaskGIT 采样；只能用 **16 帧记忆窗口**。无量化/缓存等部署优化披露。
- **可复现性**：附录 F 给了 CoinRun（Procgen）上的**单卡（16G TPU/GPU）可复现 case study**——10M transition 数据、tokenizer 训 3 天 300k steps、LAM+动力学并行训 200k steps（动作码本缩到 6）。

## 评测 benchmark（把效果讲清楚）
论文用两类指标：**视频保真度 FVD（↓，video-level）** 和自创的**可控性指标 Δ_t PSNR（↑）**——衡量"用 ground-truth 推断的潜动作"vs"随机采样的潜动作"生成帧的 PSNR 差，差越大说明动作影响越大、可控性越强（统一报 t=4）。

**Scaling 结论**：动力学模型从 **40M scale 到 2.7B**，最终训练损失随参数单调下降、"优雅 scale"；batch size 从 128→256→448（1.9M→3.8M→6.6M token）也单调获益——据此外推到 10.1B 主模型。

**LAM 输入消融（Table 2，核心方法验证）**——证明 LAM 该吃像素而非 token：

| Dataset | 输入 | #Params | FVD ↓ | Δ_t PSNR ↑ |
|---|---|---|---|---|
| Platformers | Token-input | 2.3B | **38.8** | 1.33 |
| Platformers | **Pixel-input (Genie)** | 2.5B | 40.1 | **1.91** |
| Robotics | Token-input | 1B | 257.8 | 1.65 |
| Robotics | **Pixel-input (Genie)** | 1B | **136.4** | **2.07** |

像素输入虽在 Platformers FVD 略逊（40.1 vs 38.8），但**可控性显著更高**（1.91 vs 1.33），且在 Robotics 上 FVD 大幅领先（136.4 vs 257.8）——说明 tokenization 会丢失运动/动态信息。

**Tokenizer 架构消融（Table 3，~同参数量）**——ST-ViViT 全面胜出：

| Tokenizer | #Params | 显存 | FVD ↓ | Δ_t PSNR ↑ |
|---|---|---|---|---|
| ViT（仅空间） | 230M | 0.3GB | 114.5 | 1.39 |
| C-ViViT（Phenaki，全时空） | 225M | 1.6GB | 272.7 | 1.37 |
| **ST-ViViT（ours）** | 205M | 0.9GB | **81.4** | **1.66** |

C-ViViT 全时空注意力显存最高却最差（易过拟合需强正则）；ST-ViViT 用 0.9GB 显存拿到最佳保真+可控。

**Robotics 模型**：2.5B 参数，测试集 **FVD 82.7**；能学到一致的离散动作（如 down/up/left）、还能学物体形变（薯片袋等可变形物体）。

**训练 agent（行为克隆 BC）**：在 Procgen **CoinRun** 上，用冻结的 LAM 给专家视频打潜动作标签训策略，再用极少量带真动作的专家数据建"潜→真"映射。结果：**仅需 200 条专家样本适配，LAM-based 策略就达到 oracle BC（有真动作上界）的同等水平**——尽管几乎肯定从没见过 CoinRun，证明学到的潜动作一致、可跨域迁移。

**数据过滤消融**：见上文，580M 模型精选集 FVD 54.8 优于原始集 61.4。

> 注：Genie 是世界模型而非 t2i/t2v 美学生成模型，故**没有也不适用** GenEval / T2I-CompBench / DPG / HPSv2 / ImageReward / PickScore / VBench 这类指标；其评测体系是 FVD + 自定义 Δ_t PSNR + 下游 BC。

## 创新点与影响
**核心贡献**：① 提出"生成式可交互环境（generative interactive environment）"新范式，**第一个仅靠无标注互联网视频、无监督学出可逐帧动作控制的可玩世界模型**；② **无监督潜动作模型（LAM）**——用极小 VQ 码本（|A|=8）从无动作视频里学出一致、可迁移、人类可玩的潜动作空间，是整篇工作的灵魂；③ **内存高效的 ST-transformer + ST-ViViT tokenizer**，让长视频世界模型可规模化；④ 给出 40M→2.7B 的严格 scaling 分析，外推到 10.7B 的"基础世界模型"。

**影响**：开创了 **"playable world model" 路线**——直接催生 Genie 2（2024.12，3D 可玩世界）、Genie 3（2025，实时可交互世界）以及业界一大批"世界模型 / 可交互视频生成"工作；其"无监督潜动作 + 用世界模型给 agent 造无穷训练环境"的思路，被广泛视为通向**通用智能体（generalist agents）**的一条潜在路径（用生成世界做永不枯竭的课程）。ICML 2024 最佳论文。

**已知局限（论文自陈）**：① 继承自回归 transformer 的通病，**会幻觉出不真实的未来**；② 仅 **16 帧记忆窗口**，长时程一致性差；③ 推理仅约 **1 FPS**，离可交互帧率尚远；④ 不发布权重/数据，复现门槛高（仅给单卡 CoinRun toy 例）；⑤ 分辨率低（主训 160×90，网站 demo 才 360p）。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2402.15391
- paper (PDF): https://arxiv.org/pdf/2402.15391
- project page / blog: https://sites.google.com/view/genie-2024/home

## 一手源存档（sources/）
- [arxiv-2402.15391.pdf](https://arxiv.org/pdf/2402.15391)  （arXiv 原文 PDF，不入 git）
- [genie--project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/genie--project-page.md)
