---
title: "NÜWA: Visual Synthesis Pre-training for Neural visUal World creAtion"
org: "Microsoft Research Asia / Peking University"
country: China
date: "2021-11"
type: paper
category: unified
tags: [unified-generation, autoregressive, vq-gan, 3d-transformer, sparse-attention, text-to-image, text-to-video, image-editing, any-to-vision]
url: "https://arxiv.org/abs/2111.12417"
arxiv: "https://arxiv.org/abs/2111.12417"
pdf_url: "https://arxiv.org/pdf/2111.12417"
github_url: "https://github.com/microsoft/NUWA"
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2111.12417.pdf, nuwa--readme.md, nuwa--nuwa-detail.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
NÜWA 是微软亚研院 2021 年提出的**统一自回归视觉生成预训练模型**：用一个 3D Transformer encoder-decoder + VQ-GAN 离散化，把文本(1D)/图像(2D)/视频(3D)统一成 3D token 表示，**单个解码器支撑 8 类视觉合成任务**（文→图、文→视频、草图→图/视频、图像补全、视频预测、文引导图/视频编辑）；核心创新是 **3D Nearby Attention(3DNA) 局部稀疏注意力**，把全注意力复杂度从 O((hws)²) 降到 O((hws)·eʰeʷeˢ)，并在 MSCOCO T2I 取得 **FID-0 12.9 / CLIPSIM 0.3429**（优于 DALL-E、CogView）、在 BAIR 视频预测把 SOTA FVD **从 94±2 推到 86.9**（仅给 1 帧条件），是早期 any-to-vision 统一生成框架的代表作。870M 参数。

## 背景与定位
2021 年视觉生成的主流是**自回归离散 token 路线**：[[vq-vae]] 把图像离散化为 codebook token，再用 Transformer 逐 token 生成，代表作 DALL-E、CogView(文→图)、GODIVA(文→视频)、VideoGPT/LVT(视频预测)。相比 GAN，自回归路线有显式密度建模、训练稳定的优势，且 VQ 离散化让大规模预训练成为可能。

但当时的痛点是**图像与视频被割裂处理**：每个模型只生成图像或只生成视频，无法从两类视觉数据中互相获益。NÜWA 的定位就是**用单一框架同时覆盖语言、图像、视频**，让多任务多模态联合预训练带来跨任务增益（论文证明 T2I 帮助 T2V 的语义一致性，V2V 帮助 T2V 的视觉质量）。

此外，高维视觉数据的自注意力是平方复杂度瓶颈。此前的稀疏方案有两类：block-sparse（[[video-transformer]]/LVT，分块独立处理但忽略块间关系）和 axial-sparse（[[axial-attention]]/DALL-E/CogView/GODIVA，沿单轴注意但上下文受限、损害质量）。NÜWA 提出 3D nearby-sparse，证明"局部邻域注意"在视觉生成上优于"沿轴注意"。这条统一 + 局部注意的思路，是后续 unified any-to-vision 工作（如 NUWA 系列续作 NUWA-Infinity/NUWA-XL，以及更广义的统一生成研究）的早期源头之一。

## 模型架构
**整体 = 3D Transformer encoder-decoder**，由「自适应编码器（接受文本或视觉草图条件）」+「8 任务共享的预训练解码器」构成。对补全/预测/编辑类任务，输入的部分图像或视频直接喂给解码器。

**统一 3D 数据表示**：把一切都看成 token，统一记为 X ∈ ℝ^(h×w×s×d)，h,w 为空间高宽 token 数，s 为时间轴 token 数，d 为 token 维度。
- **文本**：BPE（小写）分词嵌入为 ℝ^(1×1×s×d)，空间维占位为 1。
- **图像**：用 **VQ-GAN**（而非 VQ-VAE）离散化为 ℝ^(h×w×1×d)，时间维占位 1。论文明确：VQ-GAN 在 VQ-VAE 的逐像素重建损失外加了**感知损失 + GAN 损失**，从"严格像素匹配"放宽到"高层语义匹配"，实验证明生成质量显著更好（见消融）。
- **视频**：**不**像 VideoGPT/VideoGen 那样把 VQ-VAE 卷积从 2D 扩到 3D，而是**直接用同一个 2D VQ-GAN 逐帧编码**，得到 ℝ^(h×w×s×d)（s=帧数）。这样图像和视频可**共享同一 codebook**，从而同时受益于图像与视频数据，且仍能生成时序一致的视频。
- **草图（sketch）**：视为带特殊通道的图像。把分割矩阵 ℝ^(H×W)（每像素一个类别）按 one-hot 展为 ℝ^(H×W×C)（C=分割类别数），单独训一个 **VQ-GAN-Seg** 得到 ℝ^(h×w×1×d)（图像草图）或 ℝ^(h×w×s×d)（视频草图）。

**3D Nearby Self-Attention(3DNA)** 是核心模块（同时支持 self/cross attention）：对目标 X 的每个坐标 (i,j,k)，先线性投影到条件 C 中的对应坐标 (i',j',k')=(⌊i·h'/h⌋,…)，再只在以它为中心、宽高时间范围为 (eʷ,eʰ,eˢ) 的**局部邻域 N^(i,j,k)** 内做注意（Q 来自 X，K/V 来自该邻域）。C=X 时是自注意，C≠X 时是以 C 为条件的交叉注意。复杂度从全注意 O((hws)²) 降为 **O((hws)·eʰeʷeˢ)**，且因"同时考虑空间与时间的真实邻域交互"，质量也优于 axial-sparse。

**3D Encoder-Decoder**：位置编码用**三套独立的可学习词表**（高/宽/时间轴各一）分别加到 Y 和 C 上。编码器堆 L 层 3DNA 建模条件 C 的自注意；解码器每层做两件事——生成结果的因果自注意（Y_{<i,<j,<k}）+ 生成结果对编码器输出 C^(L) 的交叉注意；初始 token 是可学习的特殊 `<bos>`。

**参数与分辨率**（论文 Tab.8 给出两套配置）：
- 隐藏维 1280，注意力头 20，每头 64 维；编码器 12 层，解码器 24 层；**总参数 870M**。
- 文本 3D 尺寸 1×1×77×1280；图像 21×21×1×1280；视频 21×21×10×1280（从视频按 2.5 fps 采 10 帧）。默认分辨率 336×336。
- **NÜWA-256**：图像 256×256，离散 token 32×32，压缩比 F8，codebook 维 256 → 用更多 token 换更高图像质量，但视频只能生成 4 帧。
- **NÜWA-336**（默认）：图像 336×336，离散 token 21×21，压缩比 F16 → token 更少、可生成 10 帧视频，兼顾图像与视频。
- 共享 VQ-GAN 的 grid feature 尺寸 441×256，**codebook 大小 12,288**。
- 不同模态用不同稀疏 extent：文本 (eʷ,eʰ,eˢ)=(1,1,∞)（全文本始终可见）；图像/图像草图 (3,3,1)；视频/视频草图 (3,3,3)。

## 数据
**预训练用三个数据集，对应三个预训练任务**（论文 4.1 + Tab.8）：
- **Conceptual Captions** → 文→图(T2I)，**2.9M 文-图对**。
- **Moments in Time** → 视频预测(V2V)，**727K 视频**。
- **VATEX** → 文→视频(T2V)，**241K 文-视频对**。

**VQ-GAN tokenizer 的训练数据**：图像 VQ-GAN 在 ImageNet 和 Open Images 上训练；草图 VQ-GAN-Seg 在 MSCOCO（图像草图/S2I）和 VSPW（视频草图/S2V）上训练。

下游微调/评测数据集：MSCOCO（T2I/S2I/I2I）、Kinetics(T2V)、BAIR Robot Pushing(V2V)、MSR-VTT(多任务消融)、MSCOCO-stuff(S2I)。

**未披露/未涉及**：没有美学过滤、re-captioning、合成数据、安全过滤等近代 T2I 常见的数据工程环节——2021 年的工作主要直接用公开学术数据集，数据清洗细节论文未展开。

## 训练方法
**训练目标 = 自回归 next-token 交叉熵**（非 diffusion / 非 flow matching；这是早期离散自回归路线）。同时在三个任务上联合训练，损失是三项 token-level 交叉熵之和（论文 Eq.16）：
- T2I：∑_{t=1}^{h×w} log p_θ(y_t | y_{<t}, C^text)
- V2V：∑_{t=1}^{h×w×s} log p_θ(y_t | y_{<t}, c)（无文本输入，用特殊词 "None" 的常量 3D 表示 c 作条件）
- T2V：∑_{t=1}^{h×w×s} log p_θ(y_t | y_{<t}, C^text)

**两阶段范式**：第一阶段训 VQ-GAN/VQ-GAN-Seg 把视觉数据离散化；第二阶段训 3D Transformer 在离散 token 上做自回归生成。下游任务（T2I/T2V/V2V/S2I/S2V）通过**微调**适配；图像补全(I2I)、文引导图像编辑(TI2I)、文引导视频编辑(TV2V)则是**zero-shot**（直接复用预训练解码器，无需额外训练）。

**关键超参**（论文 4.1 + Tab.8）：Adam 优化器，学习率 **1e-3**，batch size **128**，warm-up 占总步数 5%，总 **50M 步**。两套配置都用同一学习率和步数，论文强调"没有过度调参"。

**未涉及**：没有 SFT/RLHF/DPO/reward model 等偏好对齐阶段，也没有 consistency/LCM/步数蒸馏等加速（自回归路线天然没有 diffusion 的多步去噪问题，但逐 token 解码本身慢）。

## Infra（训练 / 推理工程）
- **算力**：在 **64 张 A100 上训练约 2 周**（论文 4.1 原文 "We pre-train on 64 A100 GPUs for two weeks"）。
- **推理速度**：文引导图像编辑(TI2I) 单图约 **50 秒**生成；论文以此对比 Paint By Word（需推理时额外训练、约 300 秒收敛），凸显 NÜWA 的预训练 zero-shot 编辑在速度上的优势。
- **3DNA 的工程意义**：局部稀疏注意是其能 scale 到视频（时间轴 s 较大时 eʰeʷeˢ < h+w+s）的关键——对长视频/高分辨率帧，nearby-sparse 比 axial-sparse 更省算力（论文 Tab.7 复杂度对比：3D full O((hws)²)、block O((hws)²/b)、axial O((hws)(h+w+s))、nearby O((hws)·eʰeʷeˢ)）。
- **未披露**：并行/分布式策略、混合精度、吞吐(tokens/s)、量化、部署形态等工程细节论文未报告。

## 评测 benchmark（把效果讲清楚）
所有数字来自已落盘的 arXiv PDF（arxiv-2111.12417.pdf）。

**Text-to-Image (T2I) — MSCOCO 256×256**（Tab.1，每条文本生成 60 图用 CLIP 选最佳）：

| 模型 | FID-0↓ | CLIPSIM↑ | IS↑ |
|---|---|---|---|
| AttnGAN | 35.2 | 0.2772 | 23.3 |
| DM-GAN | 26.0 | 0.2838 | 32.2 |
| DF-GAN | 26.0 | 0.2928 | 18.7 |
| DALL-E | 27.5 | — | 17.9 |
| CogView | 27.1 | 0.3325 | 18.2 |
| XMC-GAN | 9.3 | — | 30.5 |
| **NÜWA** | **12.9** | **0.3429** | 27.2 |

NÜWA 的 FID-0=12.9、CLIPSIM=0.3429 显著优于 DALL-E/CogView；XMC-GAN 的 FID 9.3 更低，但论文论证在相同样本上 NÜWA 视觉更真实（如人脸更清晰、气球生成正确）。

**Text-to-Video (T2V) — Kinetics**（Tab.2）：NÜWA(128×128) 在所有指标取得最佳——Acc **77.9**、FID-img **28.46**、FID-vid **7.05**、CLIPSIM **0.3012**，优于 T2V(64×64)/SC/TFGAN。还展示了对未见文本（"playing golf at swimming pool"、"running on the sea"）的强 zero-shot 能力。

**Video Prediction (V2V) — BAIR 64×64**（Tab.3）：**仅给 1 帧条件**，NÜWA 把 SOTA FVD **从 94±2(Video Transformer-L) 推到 86.9**，优于 MoCoGAN(503)/SVG-FP(315)/VideoFlow(131)/CCVS(99±2) 等。

**人评（Appendix C）**：
- T2I vs CogView（MSCOCO，2000 文本）：视觉质量 NÜWA **62%** vs CogView 23%（15% 不确定）；语义一致性 NÜWA 21% vs CogView 12%（67% 不确定）。NÜWA 在更少文-图对下仍靠多任务预训练胜出。
- I2I 图像补全 vs VQ-GAN：NÜWA **89%** 胜，验证强 zero-shot 补全能力。

**关键消融结论**：
1. **VQ-GAN vs VQ-VAE**（Tab.4，ImageNet 256²→16²/F16 同一设置对比）：FID **13.3→6.04**、SSIM **0.7026→0.7105**，VQ-GAN 显著更好。论文进一步论证**离散 token 数比压缩率更关键**——同为 F16，21×21 token（336²→21²，FID 4.79）优于 16×16 token（256²→16²，FID 6.04）；而 256²→32² 的 F8 配置 FID 最低（2.03，SSIM 0.8285）但 token 更多更耗算力，最终折中用 21×21（在 Open Images 上进一步把 FID 4.79→4.31）。VQ-GAN-Seg 草图重建：MSCOCO PA 96.82 / FWIoU 93.91，VSPW PA 95.36 / FWIoU 91.82。
2. **多任务预训练**（Tab.5，MSR-VTT 的 T2V）：仅 T2V → CLIPSIM 0.2314；+T2I → 0.2379（T2I 帮语义一致）；+V2V → FVD/视觉质量提升（V2V 帮无条件视频模式）；**三任务全开最佳**（FID-vid 47.68 / CLIPSIM 0.2439）。
3. **3D nearby attention**（Tab.6，VSPW 的 S2V）：编码器+解码器都用 nearby（FID-vid 27.79 / Detected PA 0.6085）优于全用 full（FF: 35.21/0.5220）和全用 axial（AA: 29.18/0.5957）。证明局部邻域注意在质量和复杂度上都优于 axial-sparse。

**首次提出的任务**：开放域 Sketch-to-Video(S2V) 和 Text-Guided Video Manipulation(TV2V) 是本文首次提出（无对比基线，放在消融中评估）。

## 创新点与影响
**核心贡献**（论文自述三点 + 实质）：
1. **统一 3D Transformer encoder-decoder 框架**：用 ℝ^(h×w×s×d) 统一表示文本(1D)/图像(2D)/视频(3D)，自适应编码器 + 8 任务共享解码器，是早期 **any-to-vision 统一生成**的代表，证明图像与视频联合预训练能跨任务互相增益。
2. **3D Nearby Attention(3DNA) 局部稀疏注意**：把局部注意从图像扩展到视频，复杂度 O((hws)·eʰeʷeˢ)，同时在质量上优于 block-sparse 和 axial-sparse，是其能 scale 到视频的关键。
3. **统一 codebook 处理图像与视频**：用单个 2D VQ-GAN 逐帧编码视频（而非 3D 卷积 VQ-VAE），让图像/视频共享 codebook、共享解码器。

**影响**：NÜWA 是统一多模态生成的早期里程碑，开创了 Microsoft 的 NUWA 系列（README 记录续作：NUWA-Infinity 无限视觉合成、NUWA-LIP 语言引导图像补全、NUWA-XL diffusion-over-diffusion 超长视频生成）。其"一个模型多任务、文/图/视频统一 token 化、局部稀疏注意"的思路，预示了后来 unified generation 的方向。同时它也是"预训练 → zero-shot 编辑/补全"范式的早期实践（编辑无需推理时训练，比 Paint By Word 快 6 倍）。

**已知局限**：
- 走的是**离散自回归路线**，逐 token 解码慢、易累积误差，质量受 VQ-GAN 重建上限制约；随后两年被 [[latent-diffusion-ldm]]/[[stable-diffusion]] 等扩散路线在图像质量上反超。
- 分辨率与视频长度受限（默认 336×336、10 帧 2.5fps；NÜWA-256 仅 4 帧），是 token 数与模型容量的折中。
- 数据规模较小（T2I 仅 2.9M 对，远小于同期 CogView/DALL-E），靠多任务预训练弥补；无现代数据工程（re-caption、美学/安全过滤）。
- 无偏好对齐(RLHF/DPO)、无蒸馏加速。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2111.12417
- arxiv_pdf: https://arxiv.org/pdf/2111.12417
- github: https://github.com/microsoft/NUWA
- github_readme: https://raw.githubusercontent.com/microsoft/NUWA/main/README.md
- github_nuwa_detail: https://raw.githubusercontent.com/microsoft/NUWA/main/NUWA.md

## 本地落盘文件
- ../../../sources/omni/2021/arxiv-2111.12417.pdf
- ../../../sources/omni/2021/nuwa--readme.md
- ../../../sources/omni/2021/nuwa--nuwa-detail.md
