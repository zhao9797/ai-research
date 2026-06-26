---
title: "Lumiere: A Space-Time Diffusion Model for Video Generation"
org: "Google Research / Weizmann Institute / Tel-Aviv University / Technion"
country: "US / Israel"
date: "2024-01"
type: paper
category: video
tags: [text-to-video, diffusion, space-time-unet, t2i-inflation, pixel-diffusion, image-to-video, video-inpainting]
url: "https://arxiv.org/abs/2401.12945"
arxiv: "https://arxiv.org/abs/2401.12945"
pdf_url: "https://arxiv.org/pdf/2401.12945"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://lumiere-video.github.io/"
downloaded: [arxiv-2401.12945.pdf, lumiere-space-time-video-diffusion--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Lumiere 是 Google Research 的文生视频扩散模型，核心创新是 **Space-Time U-Net（STUNet）**——在空间与时间两个维度同时下/上采样，从而**一次前向就生成整段 80 帧 5 秒视频**，彻底取消了主流方案里"先生成稀疏关键帧、再用一串时间超分（TSR）补帧"的级联，换来更全局连贯的运动；在 UCF101 zero-shot 上 FVD=332.49，用户研究中 T2V/I2V 对所有 baseline（含 Pika、Gen-2、SVD、ImagenVideo）均胜出。

## 背景与定位
2023 年末主流 T2V 扩散模型（[[imagen-video]]、Make-A-Video、Video LDM、SVD、Show-1、Emu Video）几乎都走**级联**路线：base 模型生成时间上**稀疏的关键帧**（如 3fps），再叠多级 **TSR（temporal super-resolution）** 把帧率补满，最后空间超分（SSR）——典型如 ImagenVideo 整条流水线是 **7 个模型（1 base + 3 TSR + 3 SSR）**。Lumiere 指出这条路线对"全局连贯运动"有结构性缺陷：

1. base 只生成激进下采样的关键帧，快速运动被**时间走样（temporal aliasing）**，变得歧义；
2. TSR 模块上下文窗口固定且小，无法在整段视频上一致地消解走样歧义（论文 Fig.2 用周期性运动如"走路"演示：ImagenVideo 的 X-T slice 出现不连贯）；
3. 级联训练有 **domain gap**——TSR 训练时喂真实下采样帧，推理时却插值生成帧，误差累积。

Lumiere 的回应是：**别再固定时间分辨率**。它在网络里同时做时间维的下/上采样，把绝大部分计算放在一个**时空压缩**的紧凑表示上，于是单个 base 模型就能一次产出 80 帧（16fps，5s——超过多数影视镜头的平均时长）。论文强调这个设计被此前所有 inflation 方案"集体忽视"了（它们只做空间下/上采样、时间分辨率全程不变）。技术脉络上它建立在 [[ddpm]] 像素空间扩散 + [[imagen]] 的级联 T2I 之上，并把 MultiDiffusion（Bar-Tal et al. 2023，原本用于全景图拼接）扩展到时间轴。

## 模型架构
**总体两段式（非级联补帧）**：base 模型一次生成全片低分辨率 128×128×80 帧 → 时间感知的 SSR 把每帧空间超分到 1024×1024。注意这里**没有 TSR**，SSR 只做空间放大。

**STUNet（核心）**：把一个**预训练、像素空间**的 Imagen T2I U-Net "inflate" 成时空 U-Net：
- 在 T2I 架构里**交错插入时间模块**，并在每个预训练空间 resize 模块之后插入**时间下/上采样模块**——这是它区别于一切前作的关键（前作时间分辨率全程不变）。
- **除最粗一级外的所有层级**用**分解式（factorized）时空卷积**（先空间 2D conv，再 1D 时间 conv）：比 full-3D conv 计算省、非线性更多，比纯 1D conv 表达力更强（参考 Tran et al. 2018 的 (2+1)D 思想）。
- **仅在最粗分辨率**用**时间注意力**：时间注意力计算量随帧数二次增长，而最粗层已是时空压缩表示，因此可在此**堆叠多层时间注意力**而开销有限。
- 灵感来自 3D U-Net（Çiçek 2016，医学体数据），把 U-Net 的池化泛化到 3D。
- 每个 inflation block 是**残差结构**：时间分量后接一个线性投影，加回预训练 T2I 空间层输出。

**SSR + 时间 MultiDiffusion**：SSR 网络也是 inflate 的，但因为工作在高分辨率，内存上只能处理短片段。为避免片段边界的外观跳变，Lumiere 把 **MultiDiffusion 用到时间轴**：把噪声视频切成**重叠片段（重叠 2 帧）**，每个去噪步对重叠像素做预测平均（等价于求解一个最小二乘最优化，解就是重叠窗口预测的线性组合），从而消除时间边界伪影（论文 Fig.14 用 frame-diff 证明：不用 MultiDiffusion 时每个非重叠段交界处误差出现尖峰）。

**条件注入（统一接口）**：把额外条件做成"masked conditioning video C + 二值 mask M"，与噪声视频 J 在通道维拼接成 ⟨J, C, M⟩ ∈ R^{T×H×W×7}，把 base T2V 第一层卷积输入通道**从 3 扩到 7** 再微调。这套接口统一覆盖 image-to-video（C=首帧+空白帧，M 首帧为 1 其余为 0）、inpainting/outpainting（用户给 C 和待补区域 M）、cinemagraphs（C=整段复制同一图，M 只在指定区域为待动）。

**参数量未披露**；分辨率策略为 base 128×128 → SSR 1024×1024，固定 80 帧/16fps。底层 T2I 用的是**像素空间** Imagen（非 latent），作者明确指出其设计原则同样适用于 latent 视频扩散，只是本工作没做。

## 数据
- 训练集：**30M 视频 + 对应文本 caption**（论文 §5 明确给出）。
- 视频规格：**80 帧、16fps（即 5 秒）**。
- 来源 / 配比 / 清洗过滤 / re-captioning / 合成数据 / 美学与安全过滤：**论文与项目页均未披露**（典型 Google 内部数据集，细节缺失）。
- 评测 prompt 集：109 条文本 prompt（91 条取自 Make-A-Video / ImagenVideo / Video LDM 等前作，其余 18 条自建，附录 D.3 列全），覆盖多样物体与动作。

## 训练方法
- **生成范式**：标准 **DDPM 扩散概率模型**（像素空间去噪），非 flow matching、非 latent。文本/空间条件以 guiding signal 注入。
- **inflation 式训练**：**冻结预训练 T2I 权重，只训练新加的时间层**（与 Video LDM、AnimateDiff 同思路），可与个性化 T2I 权重组合。
- **初始化 trick（关键）**：常规 inflation 在初始化时 T2V 等价于 T2I（生成独立图像帧），但 Lumiere 因为多了时间下/上采样模块，**无法**在初始化时严格等价于 T2I。作者发现把时间下/上采样模块初始化成**最近邻下/上采样（时间 striding / 帧复制）**比标准随机初始化好得多——下采样=identity 初始化的 1D 时间 conv + stride，上采样=帧复制 + identity 初始化的 1D 时间 conv；这保证初始化时每第 N 帧（N=网络总时间下采样因子）与预训练 T2I 输出一致，从而继承 T2I 先验。inflation block 里的线性投影按惯例零初始化。附录 B 在 UCF-101 上做了 loss 消融，证明 identity 初始化优于标准初始化（Fig.12-13）。
- **条件微调**：把首层卷积扩到 7 通道后微调 base T2V，使其学会"把 C 中未遮挡内容复制到输出、只在 mask 区域生成运动"。
- **风格化（stylized generation）**：保持 T2I 冻结，把空间层权重在"微调风格权重 W_style 与原始 W_orig"之间**线性插值** W = α·W_style + (1−α)·W_orig，α∈[0.5,1] 手动选，以在风格保真与运动合理之间平衡（直接 plug-and-play 换风格权重会导致画面僵死/扭曲）。
- **蒸馏 / 步数加速 / consistency / LCM / 量化**：**未涉及/未报告**。
- 其余训练超参（batch、步数、优化器、学习率、噪声调度细节）：**未披露**。

## Infra（训练 / 推理工程）
- 算力规模 / GPU 数 / GPU·时 / 并行分布式 / 混合精度 / 吞吐：**论文与项目页完全未披露**。
- 推理工程仅可推断出的点：SSR 因高分辨率内存受限，必须切重叠片段 + 时间 MultiDiffusion 拼接（一种以多次前向换全局一致性的推理策略）；base 一次出全片（80 帧）。
- 部署形态：**未开源**，无公开权重 / 代码 / API（项目页只提供 demo 画廊，无 GitHub 代码仓、无 HuggingFace 模型）。
> Infra 维度整体为"未披露"，不做任何推测性数字。

## 评测 benchmark（把效果讲清楚）
**1) UCF101 zero-shot（Table 1）**——生成 10,235 个视频（按 UCF101 类别分布、用 Ge et al. 2023 的 prompt 集），取前 16 帧 244×244 算 I3D embedding 后计 FVD，C3D embedding 计 IS：

| 方法 | FVD ↓ | IS ↑ |
|---|---|---|
| MagicVideo | 655.00 | — |
| Emu Video | 606.20 | 42.70 |
| Video LDM | 550.61 | 33.45 |
| Show-1 | 394.46 | 35.42 |
| Make-A-Video | 367.23 | 33.00 |
| PYoCo | 355.19 | 47.76 |
| SVD | 242.02 | — |
| **Lumiere (Ours)** | **332.49** | 37.54 |

Lumiere FVD=332.49、IS=37.54，**优于 Make-A-Video/PYoCo/Show-1/Emu/Video LDM/MagicVideo，但不及 SVD（242.02）**。作者强调（引 Emu Video / ImagenVideo / Parmar 等）FVD/IS 与人类感知不一致、易受低层细节与 UCF101 分布漂移影响、且协议只用 16 帧无法反映长时运动——所以更看重用户研究。

**2) 用户研究（2AFC，Fig.10）**——AMT 平台，每个 baseline×每个问题约 **400 条判断**，含 vigilance test（真实视频 vs 纯噪声、静图 vs 真实视频）。空间统一中心裁剪 resize 到 512×512，时长对齐最短的一方（每名被试看 10 组并排对比）。T2V baseline 共 6 个：ImagenVideo / AnimateDiff / SVD / ZeroScope / Pika / Gen-2（前四为公开模型，Pika/Gen-2 走商用 API；SVD 只发了 I2V 模型、出 25 帧且不吃文本，故仅比视频质量）。结论：**Lumiere 在 T2V（视觉质量+运动、文本对齐两项）对全部 6 个 baseline 都更受偏好**；**I2V 对 Pika / SVD / Gen-2 也全部胜出**（论文只给胜率柱状图 Fig.10，未给精确数值表）。

**3) 定性观察（§5.1）**：Gen-2 与 Pika 单帧质量高但**运动极少、近乎静止**；ImagenVideo 运动尚可但整体画质偏低；AnimateDiff/ZeroScope 有运动但有伪影且时长短（2s / 3.6s）。Lumiere 出 5s 视频、运动幅度更大且保持时间一致性。

**4) 消融**：
- 时间下/上采样**初始化消融**（identity vs standard，UCF-101 loss，Fig.12-13）：identity 显著更优。
- **MultiDiffusion 消融**（Fig.14）：去掉后时间边界出现伪影、frame-diff 在段交界处出现误差尖峰。

> 注：CLIPScore / GenEval / VBench / T2I-CompBench / HPSv2 / PickScore 等指标**论文未报告**（Lumiere 早于 VBench 等成为标配的时代，主要用 FVD+IS+用户研究）。

## 创新点与影响
**核心贡献**：
1. **Space-Time U-Net**：首个在 T2V inflation 中**同时做时间下/上采样**、把主计算放在时空压缩表示上的架构，使**单模型一次生成全片**成为可能，取消 TSR 级联——直击全局运动连贯性的结构性病根。
2. **时间轴 MultiDiffusion**：把全景图的 MultiDiffusion 思想搬到时间维，用重叠片段 + 预测平均消除 SSR 时间边界伪影。
3. **统一条件接口**（7 通道 ⟨J,C,M⟩）：一套微调覆盖 I2V、inpainting/outpainting、cinemagraphs；因 base 直接出全帧率视频，可即插即用 SDEdit 做一致的视频风格化、用权重插值做风格化生成。

**影响**：Lumiere 成为 Sora（2024-02）同期最具代表性的"**非级联、整段一次生成**"视频扩散范式标杆，是大量后续 T2V 工作和 Sora 类对比中**高引基线**；其"取消固定时间分辨率、在时空压缩域计算"的主张影响了后续视频生成架构对级联式 TSR 的反思。

**已知局限（作者自述）**：
- **不支持多镜头 / 转场**——只生成单镜头 5s 片段，多 shot 与场景切换仍是开放问题。
- 基于**像素空间** T2I，因此需要空间超分模块；作者承认设计原则同样适用 latent 视频扩散，但本工作未实现（这也是后续 latent DiT 路线如 Sora 的方向）。
- **指标偏弱**：自承 FVD/IS 不可靠、未上当时尚未流行的更强自动评测。
- 数据/算力/参数量等工程细节全部未公开，**不可复现**（闭源、无权重无代码）。
- 社会影响：作者提示有被滥用于伪造/有害内容的风险，呼吁配套检测工具。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2401.12945
- paper PDF: https://arxiv.org/pdf/2401.12945
- project page / demo gallery: https://lumiere-video.github.io/

## 一手源存档（sources/）
- [arxiv-2401.12945.pdf](https://arxiv.org/pdf/2401.12945)  （arXiv 原文 PDF，不入 git）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/lumiere-space-time-video-diffusion--blog.md)
