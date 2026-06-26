---
title: "AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning"
org: "CUHK / Shanghai AI Lab / Stanford"
country: China
date: "2023-07"
type: paper
category: video
tags: [video, t2v, motion-module, plug-and-play, diffusion, sd1.5, lora, motionlora, iclr2024]
url: "https://arxiv.org/abs/2307.04725"
arxiv: "https://arxiv.org/abs/2307.04725"
pdf_url: "https://arxiv.org/pdf/2307.04725"
github_url: "https://github.com/guoyww/AnimateDiff"
hf_url: "https://huggingface.co/guoyww/animatediff"
modelscope_url: ""
project_url: "https://animatediff.github.io/"
downloaded: [arxiv-2307.04725.pdf, animatediff--readme.md, animatediff--training-doc.md, animatediff--training-configs.md, animatediff--project-page.md, arxiv-2311.16933-sparsectrl.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
AnimateDiff 是一个**即插即用的运动模块（motion module）**：在 [[stable-diffusion-1]] / [[latent-diffusion-ldm]] 的冻结 U-Net 上插入一支"时序 Transformer"，只在视频数据上训练这支模块一次，就能把社区里**任意个性化 T2I 模型**（DreamBooth / LoRA、Civitai 上的 ToonYou / RealisticVision 等）**无需再训练**地变成动画生成器，同时保留其画风与画质。配套提出 **MotionLoRA**（仅约 20~50 段参考视频、~30M 存储即可学一种镜头运动），并在用户研究与 CLIP 指标上优于 Text2Video-Zero / Tune-a-Video。ICLR 2024 Spotlight，是开源文生视频/图生视频生态（ComfyUI、WebUI）影响最深远的工作之一。

## 背景与定位
2023 年中，T2I 扩散模型（[[stable-diffusion-1]]）加上 DreamBooth、LoRA、Textual Inversion 等轻量个性化方法，已经让普通人能在消费级显卡上把基座模型适配到任意画风/主体。Civitai、HuggingFace 上沉淀了海量个性化 T2I，但它们**只能出静态图**。

当时给个性化 T2I 加运动有两条路，都不理想：
- **整模型改造的视频生成**（Make-A-Video、Imagen Video、VideoLDM/Align-Your-Latents、MagicVideo 等）会**更新全部参数、改变原 T2I 的特征空间**，因而与现成的个性化权重不兼容——你没法把社区里某个二次元 LoRA 直接拿来出视频。
- **单视频/免训练法**（Tune-a-Video 在单条视频上微调、Text2Video-Zero 用预设仿射矩阵做 latent warping）要么逐个 case 微调、要么运动僵硬。

AnimateDiff 的核心定位是：**把"运动"与"外观/画风"解耦**。运动先验只训一次、与基座绑定（同一 base T2I 派生出来的所有个性化模型共享同一套 U-Net 权重空间），因此学到的运动模块可以**直接插进同源的任意个性化 T2I**，不动其图像层、不破坏其领域知识。这把"视频生成"从"重训大模型"降维成"给社区生态加一个通用插件"，是它影响力的根源。

## 模型架构
**Backbone**：Stable Diffusion v1.5 的 U-Net（4 个分辨率层级的 down/up block + middle block；每个 block = ResNet + 空间自注意力 + 文本交叉注意力），VAE 与 CLIP text encoder 沿用 SD，全程**冻结**。AnimateDiff 不替换 backbone，而是在其上做"网络膨胀（inflation）+ 插入运动模块"。

**网络膨胀（2D→3D）**：输入改为 5D 视频张量 `x ∈ R^{b×c×f×h×w}`（b 批、f 帧）。过图像层时把时间轴 f 折进 batch 轴，使每帧独立走原 2D 图像层（保住画质先验）；过运动模块时反过来把空间 h、w 折进 batch 轴，只在时间轴上交互。

**运动模块 = 时序 Transformer（temporal Transformer）**：
- 沿时间轴的若干自注意力块。把折叠后的特征看成长度 f 的向量序列 `{z_1,…,z_f}`，做标准自注意力 `Attention(Q,K,V)=Softmax(QK^T/√c)·V`，让当前帧能"看到"其它帧，从而学到内容随时间的变化（即运动）。
- **正弦位置编码（sinusoidal PE）**：在自注意力前加帧位置编码，论文强调这是必需的，否则模块感知不到帧序。配置中 `temporal_position_encoding_max_len=24`（最长 24 帧）。
- **零初始化 + 残差**：输出投影层 zero-init（借鉴 ControlNet），训练开始时运动模块是恒等映射，避免破坏原 T2I。
- 官方训练配置：插入在 U-Net 分辨率 `[1,2,4,8]` 各层；`num_attention_heads=8`、`num_transformer_block=1`、两个 `Temporal_Self` 注意力块（`motion_module_type: Vanilla`）。
- **消融**：作者把时序注意力换成 1D 时序卷积做对照，发现卷积版"把所有帧对齐成同一帧、几乎不产生运动"，证明 Transformer 时序自注意力对运动建模是关键。

**Domain Adapter（仅训练期）**：用 LoRA 形式插进基座 T2I 的自/交叉注意力投影里 `Q = W^Q z + α·AB^T z`（α=1 训练、推理可调到 0 移除），用来**吸收视频数据的画质缺陷**（见"数据/训练"）。推理时一般丢弃，或注入并用 scaler α 调节强度。

**MotionLoRA（可选第三阶段）**：在运动模块的自注意力层上加 LoRA，针对具体镜头运动（zoom/pan/tilt/rolling）微调。低秩特性带来**可组合性**——多个单独训练的 MotionLoRA 可在推理时线性叠加得到复合镜头运动。

**参数量与版本（来自官方 Model Zoo）**：
- v1 运动模块 `mm_sd_v14/v15.ckpt`：**417M**（约 1.6GB）。
- v2 运动模块 `mm_sd_v15_v2.ckpt`：**453M**（约 1.7GB），更大分辨率与 batch 训练；附带 8 个基础镜头 MotionLoRA，每个 **19M / ~74MB**。
- v3（2023.12）：domain adapter `v3_sd15_adapter`（97.4MB）+ 运动模块 `v3_sd15_mm`（1.56GB）+ 两个 **SparseCtrl** 编码器（RGB 1.85GB / scribble 1.86GB）。
- SDXL-Beta（2023.11）：`mm_sdxl_v10_beta.ckpt`（950MB），可在 SDXL 上出 1024×1024×16 帧，推理约 13GB 显存。

## 数据
- **运动模块训练集**：**WebVid-10M**（Bain et al. 2021，约 1000 万真实世界视频文本对）。
- **画质域差（核心数据洞察）**：WebVid 多为真实录像，画质显著低于训练基座 T2I 的图像集（如 LAION-Aesthetic 含艺术绘画/专业摄影）；逐帧看还带**运动模糊、压缩伪影、水印**（WebVid 的水印是典型例子）。直接在原始视频上训运动模块会把这种"低画质分布"学进去，污染输出。
- **Domain Adapter 的作用就是吸收这个域差**：在视频帧上单独训练 adapter 去拟合这些缺陷，让运动模块专注学"运动"而非"像素级画质/水印"。消融中把 adapter 的 α 从 1 调到 0，输出画质提升、水印消失，证明解耦成功。
- **MotionLoRA 数据**：每种镜头运动仅需 **20~50 段参考视频**；通过**规则化数据增强**获得（如沿时间轴逐渐缩小/放大裁剪区得到 zoom-in/zoom-out）。N=50 即可学好，N=5 会退化成"只学纹理不学运动"。
- 评测用的个性化 T2I 来自 **Civitai / HuggingFace** 社区模型（ToonYou、RealisticVision、RCNZ Cartoon 3d、MeinaMix、TUSUN、epiC Realism、MoXin 等），覆盖 2D 卡通到写实摄影多个域。具体配比/清洗细节、合成数据均未在论文中进一步披露。

## 训练方法
**目标函数**：标准 DDPM 噪声预测 MSE（ε-prediction），与 SD 相同，只是扩到视频维度——视频 batch `x_0^{1:f}` 先逐帧经 SD 的 VAE 编码成 latent，加同一前向扩散噪声，膨胀后的 U-Net 预测噪声：
`L = E[ ‖ε − ε_θ(z_t^{1:f}, t, τ_θ(y))‖_2^2 ]`。非 flow-matching、非 rectified flow，是纯 DDPM 风格 ε-loss。

**三阶段训练流程**（每阶段只训对应模块，其余冻结）：
1. **Domain Adapter（缓解负面影响）**：在从视频随机采样的**静态帧**上，用原 SD 目标只训 LoRA 形式的 domain adapter，拟合视频域的画质缺陷。
2. **Motion Module（学运动先验）**：插入新初始化的时序 Transformer，**冻结 base T2I 与 domain adapter**，只在视频上训运动模块，学到可迁移的通用运动先验。
3. **MotionLoRA（可选，适配新运动）**：在运动模块自注意力上加 LoRA，用 20~50 段参考视频、约 **2000 次迭代（~1~2 小时）** 学一种镜头运动，仅约 30M 额外存储。

**关键超参（v1 官方 config）**：base = SD v1.5；采样 **16 帧、256×256、stride 4**；motion module `learning_rate=1e-4`、`train_batch_size=4`；domain adapter / 图像层微调 `lr=1e-5`、`batch_size=50`；noise scheduler `num_train_timesteps=1000`、β 线性 0.00085→0.012；混合精度 + xformers 高效注意力。（注：repo 内 `max_train_steps:100` 是示例占位，非真实训练步数；论文称真实训练配置见补充材料，但 arXiv v2 PDF 未内联补充材料正文，故真实总步数/GPU 时**未在已抓取一手源中披露**。）

**v2 改进**：官方 README 明确说 v2 在**更大分辨率与更大 batch**上重训运动模块，"scale-up training 显著提升运动质量与多样性"——具体数值未公布。

**蒸馏/加速**：原始 AnimateDiff 论文未做步数蒸馏；推理默认 25 步 DDIM、guidance 8.0。（后续社区/作者另发的 AnimateLCM 等加速工作不在本论文范围。）

## Infra（训练 / 推理工程）
- **训练框架**：PyTorch + `torchrun`（DDP），混合精度，xformers memory-efficient attention。官方示例为单机单卡脚本（`--nnodes=1 --nproc_per_node=1`），真实大规模训练的卡数/GPU·时**未在已抓取一手源中披露**。
- **推理形态**：在冻结个性化 T2I 上同样做 inflation + 注入运动模块（+ 可选 MotionLoRA / domain adapter），从随机噪声做反向扩散后逐帧 VAE 解码出 16 帧动画。**无需 DDIM inversion**（区别于很多视频编辑法），因此可直接随机采样生成。
- **显存**：v1/v2（SD1.5，256~512 分辨率）属消费级可跑；SDXL-Beta 出 1024×1024×16 帧约需 **13GB VRAM**，并需调采样步数等超参。
- **可控生成零成本叠加**：因为内容与运动解耦，可直接叠加 [[controlnet]]（如深度图序列）或 T2I-Adapter 做可控动画，**无需额外训练**。
- **生态集成**：官方被 HuggingFace **Diffusers** 原生支持（`AnimateDiffPipeline`）；社区有 sd-webui-animatediff、ComfyUI-AnimateDiff-Evolved，使其成为开源视频管线的事实标准插件。

## 评测 benchmark（把效果讲清楚）
论文用**用户研究（AUR，平均用户排名，越高越好）**与 **CLIP 指标**三维度评估：text alignment（文本对齐）、domain similarity（与个性化域的相似度，对参考图算 CLIP）、motion smoothness（运动平滑度）。对照 Text2Video-Zero 与 Tune-a-Video（同一批个性化 T2I 上生成）：

| 方法 | UserStudy Text↑ | UserStudy Domain↑ | UserStudy Smooth↑ | CLIP Text↑ | CLIP Domain↑ | CLIP Smooth↑ |
|---|---|---|---|---|---|---|
| Text2Video-Zero | 1.620 | 2.620 | 1.560 | 32.04 | 84.84 | 96.57 |
| Tune-a-Video | 2.180 | 1.100 | 1.615 | 35.98 | 80.68 | 97.42 |
| **AnimateDiff (Ours)** | **2.210** | 2.280 | **2.825** | 31.39 | **87.29** | **98.00** |

要点：AnimateDiff 在**用户研究的文本对齐与运动平滑度**上最高，在 **CLIP 的 domain similarity（87.29）与 smoothness（98.00）** 上最高——即**最好地保住了个性化画风、运动最平滑**。Tune-a-Video 的 CLIP-Text 略高（35.98），但其 domain 相似度最差（用户研究 1.100），说明它牺牲了画风一致性。论文未报告 FID / FVD / VBench 等定量视频指标（当时 VBench 尚未流行），这些维度**未报告**。论文还与商用 Gen-2、Pika Labs 做了定性对比（Fig.5），无量化分数。

**关键消融结论**：
- **Domain Adapter α 1→0**：α 越小画质越高、水印越淡——验证 adapter 成功承接了视频域的画质缺陷。
- **运动模块设计**：时序 Transformer vs 1D 时序卷积，卷积版几乎不产生运动（所有帧趋同），Transformer 才能建模运动。
- **MotionLoRA 效率**：rank=2（~1M）即可学到 zoom-in 且运动质量可比 rank=128（~36M）；参考视频 N=50 足够、N=5 退化为只学纹理。

## 创新点与影响
**核心贡献**：
1. **运动/外观解耦的即插即用运动模块**——训一次、插入同源任意个性化 T2I，无需逐模型微调即可生成动画并保住画风；首次系统验证"个性化 T2I → 动画生成器"的通用通路。
2. 实证**时序 Transformer 足以建模运动先验**（优于时序卷积），为后续视频生成架构提供依据。
3. **Domain Adapter** 解法：用 LoRA 吸收视频训练集的画质域差（水印/模糊），让运动模块专注学运动——一个被后续大量沿用的"训练期净化"技巧。
4. **MotionLoRA**：极低数据（20~50 视频）与极低存储（~30M）就能定制镜头运动，且可组合。

**影响**：
- 成为**开源文生视频/图生视频生态的基础设施**：被 Diffusers 原生支持，ComfyUI / WebUI 插件围绕它构建，催生 AnimateLCM（蒸馏加速）、SparseCtrl（稀疏控制，作者团队 arXiv 2311.16933，即 v3 的 RGB/scribble 控制编码器，借 ControlNet 思路在 T2V 上加稀疏关键帧控制）、以及无数社区运动模块/MotionLoRA。
- 把"视频生成"从大厂闭源大模型的专利，变成普通创作者用一个插件 + 自己的 LoRA 就能玩的能力，**显著降低了动画/短视频创作门槛**。

**已知局限（官方明示）**：
1. 仍有**轻微闪烁（flickering）**；
2. 为兼容社区模型**未针对通用 T2V 做专门优化**，纯文生视频画质有限；
3. 风格对齐——图生视频/插帧时建议用同一社区模型生成的输入图，否则画风不齐；
4. 受限于 SD1.5 backbone 与 WebVid 画质，分辨率/时长/真实感不及后续 DiT 系视频大模型（Sora、可灵等）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2307.04725
- arxiv_pdf: https://arxiv.org/pdf/2307.04725
- github: https://github.com/guoyww/AnimateDiff
- project_page: https://animatediff.github.io/
- huggingface (weights): https://huggingface.co/guoyww/animatediff
- diffusers_doc: https://huggingface.co/docs/diffusers/api/pipelines/animatediff
- sparsectrl (v3 控制扩展, 同团队): https://arxiv.org/abs/2311.16933

## 一手源存档（sources/）
- [arxiv-2307.04725.pdf](https://arxiv.org/pdf/2307.04725)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/animatediff--readme.md)
- [training-doc.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/animatediff--training-doc.md)
- [training-configs.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/animatediff--training-configs.md)
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/animatediff--project-page.md)
- arxiv-2311.16933-sparsectrl.pdf  （PDF 不入 git，走 HF bucket）
