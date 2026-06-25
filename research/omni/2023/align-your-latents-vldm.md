---
title: "Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models (Video LDM)"
org: "NVIDIA / LMU Munich"
country: US
date: "2023-04"
type: paper
category: video
tags: [video-generation, latent-diffusion, text-to-video, temporal-layers, super-resolution, driving-simulation, cvpr2023]
url: "https://arxiv.org/abs/2304.08818"
arxiv: "https://arxiv.org/abs/2304.08818"
pdf_url: "https://arxiv.org/pdf/2304.08818"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://research.nvidia.com/labs/toronto-ai/VideoLDM/"
downloaded: [arxiv-2304.08818.pdf, align-your-latents-vldm--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Video LDM 把图像潜空间扩散模型（[[latent-diffusion-ldm]] / Stable Diffusion）升级为视频生成器——**冻结空间层、只插入并训练时间对齐层（temporal layers）**，从而以极小代价复用预训练图像模型。在真实驾驶场景视频（512×1024）上达到 SOTA（FVD 356 vs LVG 478），并把公开的 Stable Diffusion 变成可生成 **1280×2048、113 帧**的文生视频模型，且时间层可迁移到 DreamBooth 个性化 checkpoint，首次实现个性化文生视频。

## 背景与定位
2023 年初，图像生成已被扩散模型攻克，但视频生成滞后：训练算力昂贵、缺乏大规模公开视频数据集。此前的视频扩散模型（Video Diffusion Models [Ho 2022]、Imagen Video、[[make-a-video]]）几乎都在**像素空间**端到端训练，计算开销巨大，且仅做文生视频。

本文核心思路：站在 [[latent-diffusion-ldm]] 的肩膀上，把"在压缩潜空间里建模"这一降本利器搬到视频领域。相对前置工作的关键改进：
- **复用预训练图像 LDM**：先在图像上预训练（或直接拿现成的 Stable Diffusion），再"长出"时间维度——使得海量图像数据可用于空间层预训练，稀缺的视频数据只用于训练时间层。
- **像素空间 → 潜空间**：相对 Imagen Video（11.6B 参数）/ CogVideo（~9B），本文文生视频模型总参数约 4.1B（含上采样器）但仅训练子集，显著更小更高效。
- 同期工作 MagicVideo（同样用 LDM）、Phenaki（离散 token + 双向 transformer）、GEN-1（depth 条件视频编辑）、Make-A-Video（并发，像素空间）。作者在 UCF-101/MSR-VTT 上超越除 Make-A-Video 外的全部基线。

定位：**"Video LDM" 范式的奠基之作**——温度计式的"在图像模型上加时间层做视频"成为后续大量视频生成工作（如 [[stable-video-diffusion]]，本文一二作 Blattmann/Rombach 即 SVD 作者）的标准做法。CVPR 2023。

## 模型架构
**backbone：U-Net（图像 LDM，基于 Rombach LDM + Dhariwal U-Net），非 DiT。** 核心是"空间层 + 时间层交错"的视频感知主干。

- **空间层 lθ**：来自预训练图像 LDM，**训练时冻结**。把视频当作 B·T 帧独立图像（时间轴塞进 batch 维度）处理。
- **时间层 lϕ**：新插入的可学习层，把 batch 重排回视频维度 `(b t) c h w → b c t h w`（einops），让模型沿时间维对齐帧。两种时间混合层：
  1. **temporal attention**（时间注意力）
  2. **基于 3D 卷积的 residual block**（时间核大小 3,1,1）——消融显示 3D 卷积版优于 attention-only 版（FVD/FID 双降），且 3D 卷积便于把上下文帧 cS 在空间上喂入网络。
  - 用**正弦位置编码**为时间提供位置信息；文生视频版用**相对正弦位置编码**，使其可"卷积式"地外推到更长序列。
- **可学习融合系数 α**：每个时间层输出 z′ 与空间输出 z 按 `α·z + (1−α)·z′` 融合，α∈[0,1] 可学习。**推理时令 α=1 即跳过时间层，退化回原图像模型**。文生视频版的 α 用标量（保证 convolutional-in-time），驾驶版 α 沿时间维变化。
- **VAE / 压缩模型**：复用图像 LDM 的正则化自编码器（patch 判别器对抗训练）。**编码器保持图像版不变**（保证图像 DM 可直接在编码后的视频帧上复用），但**对 decoder 做视频微调**——加入基于 3D 卷积的 (patch-wise) 时间判别器，强制跨帧时间一致的重建，消除闪烁。此步对效果至关重要（见 benchmark）。
- **text encoder**：文生视频版直接用 Stable Diffusion 自带——SD 1.4 用 CLIP ViT-L/14（123M），SD 2.0/2.1 用 OpenCLIP-ViT/H（354M），**不训练**。文本条件也注入到时间层（cross-attention，序列长 77）。
- **生成栈（Video LDM Stack，4–5 级）**：① 关键帧 LDM 生稀疏低帧率关键帧（可选叠加 prediction model）→ ② 同一插值 LDM 做两轮时间插值（T→4T→16T）拉高帧率 → ③ decoder 解码到像素 → ④ 视频上采样器 DM 做 4× 空间超分。关键帧/插值模型**共享同一图像 backbone**。
- **分辨率策略**：驾驶版关键帧 LDM 在 128×256 潜空间训练（z-shape 16×32×4，f=8），像素空间上采样器 4× 到 512×1024。文生视频版关键帧在 320×512 训练（z-shape 40×64×4），潜空间上采样器（SD x4-upscaler，自身是 LDM）4× 到 **1280×2048**。

**参数量（文生视频 SD 2.0/2.1 版，附录 H.2.1 精确披露）**：
- autoencoder 84M（仅 decoder 微调）
- 图像 backbone 空间层 865M（不训练，860M for SD 1.4）
- **时间层 656M（训练，649M for SD 1.4）**
- text encoder 354M（不训练）
- 插值 LDM 1,509M（训练，SD 1.4/2.0/2.1 共用）
- 低分辨率文生视频 LDM 合计 **~3.1B（不含 CLIP），其中仅 ~2.2B 实际被训练**。
- 潜空间上采样器：autoencoder 55M（不训练）+ 图像 backbone 473M（不训练）+ 时间层 449M（训练）+ OpenCLIP 354M（不训练）= 977M，仅 449M 训练。
- 项目页给出的口径："总计 4.1B 参数（含上采样器、不含 CLIP），其中 2.7B 在视频上训练"。

## 数据
两套数据集对应两个应用：

- **真实驾驶场景 RDS（NVIDIA in-house，非公开）**：683,060 段 8 秒视频，分辨率 512×1024，帧率最高 30 fps（其中 85,841 段为 30 fps，其余 10 fps）。标注：二值昼/夜标签、车辆数（"crowdedness"拥挤度）；另有 100k 张独立的带车辆 bounding box 标注帧（仅用于训练 bbox 条件图像 LDM 做场景初始化）。多数为车少的高速公路场景。
- **WebVid-10M（公开）**：10.7M 视频-字幕对，总计 52K 视频小时，来自库存素材网站，内容多样。用于把 Stable Diffusion 变成文生视频模型。训练时 resize 到 320×512（center-crop）。作者明确指出 WebVid 视觉质量低于训练 SD 的图像，导致微调后图像质量略降。
- **Mountain Biking（公开，来自 Long Video GAN）**：1,202 段≥5 秒、30 fps 第一人称山地骑行视频，最高 576×1024；附录额外实验用，降采到 256×128。

数据处理/清洗、字幕重写（re-captioning）、美学/安全过滤：论文**未披露**（WebVid 字幕为数据集自带）。

## 训练方法
- **训练目标**：denoising score matching（标准扩散）。参数化用 **v-prediction**（`v = ατ·ε − στ·x`，progressive distillation 提出）和 ε-prediction 两种并用——驾驶 LDM 与上采样器用 v，文生视频 LDM 用 ε。方差保持（variance-preserving）噪声调度，**线性 noise schedule**，离散时间步 t∈{0,1000}。
- **核心两阶段训练范式**：
  1. 先训/拿到图像 LDM 空间层（驾驶版自己在视频帧上独立训练空间层；文生视频版直接用 SD，但**先在 WebVid 帧上微调 SD 空间层**以消除分辨率/分布失配，代价是略损图像质量）。
  2. **冻结空间层，只训练插入的时间层**（关键帧模型）。目标函数 Eq.(2) 只对 ϕ 优化。
  3. 同样对 decoder 做视频微调（3D 卷积时间判别器）。
- **长视频 prediction model（驾驶版）**：引入二值掩码 mS，给定 S 个上下文帧预测剩余 T−S 帧。训练时条件于 0/1/2 个上下文帧（支持 CFG）。推理时自回归地把最新预测当新上下文，可生成**数分钟**（验证到 5 分钟）的长视频。用 **context guidance**（对上下文条件做 classifier-free guidance）稳定长程生成。
- **时间插值 model**：用掩码机制，预测两关键帧之间的 3 帧（T→4T 插值），并同时训练 T→4T 与 4T→16T 两档（由二值条件指定）。文生视频插值器把 1.875 fps→7.5 fps→30 fps，且**训练全部参数**（含空间层），用 conditioning augmentation（随机 t∈{0,250} 给条件帧加噪）。
- **超分上采样器视频微调**：受 cascaded DM 启发，4× 超分。同样用 noise augmentation + 噪声等级条件。**patch-wise 训练**（驾驶版 80×80 patch，文生视频版 320×320 裁剪→80×80 潜空间），推理时卷积式应用到全分辨率——大幅省算力，且上采样器只需局部、无需捕捉长程时间相关，故不需 prediction/interpolation 框架。
- **采样**：全部用 **DDIM** 采样器；CFG / context guidance。
- **个性化（[[dreambooth]]）**：在 WebVid 微调后的 SD 1.4 空间层上，用 256 张正则图、800 步、lr 1e-6 做 DreamBooth（同时训练 U-Net 与 CLIP text encoder），把 token "sks" 绑定主体。然后**把此前在普通 SD 上训好的时间层直接插入 DreamBooth 版 SD**——时间层无需重训即生成个性化连贯视频。空间层用 DreamBooth 微调的 CLIP，时间层用标准 CLIP。
- 蒸馏/步数蒸馏/consistency/LCM：**本文未涉及**（仅提到 v-prediction 源自 progressive distillation 论文）。

## Infra（训练 / 推理工程）
论文附录 Table 6/8 披露了较细的训练配置（**全程 A100**）：
- **驾驶关键帧 (Video) LDM**：73K 步，lr 1e-4，per-GPU batch 40，**16× A100-40GB**，pdrop 0.1，v-prediction。
- **驾驶像素上采样器**：84K 步，lr 1e-5，per-GPU batch 4，**8× A100-80GB**。
- **文生视频 (SD-based) LDM**：14K 步，lr 1e-4，per-GPU batch 300，**1× A100-80GB**（注：因只训时间层，单卡即可）。
- **prediction 模型**：402K 步，per-GPU batch 3，**256× A100-80GB**。
- **interpolation 模型**：95K 步，per-GPU batch 8，**128× A100-80GB**。
- 总 GPU-时 / 训练总算力：论文**未汇总报告**。
- **推理加速**：DDIM；上采样器 patch-wise 训练后卷积式应用、潜空间建模降低显存；convolutional-in-time/space 免费外推到更长（30 秒）/更大（512×512）分辨率（但作者注明 conv-in-time 对长视频较脆弱，更推荐 prediction model）。量化、缓存等部署优化：未披露。无开源代码/权重发布（NVIDIA 研究项目，数据仅供研究）。

## 评测 benchmark（把效果讲清楚）
**驾驶场景 RDS（128×256，无上采样器）—— 表 1 左 + 表 2 人评：**
- FVD：LVG 478 → Ours 389 → **Ours(条件) 356**；FID：LVG 53.5 → Ours 31.6（条件版 FID 51.9）。
- 人评：Ours(uncond) vs LVG 偏好 54.02% vs 40.23%；Ours(cond) vs LVG **62.03% vs 31.65%**。

**消融（RDS，表 1 右）：**
- Pixel-baseline FVD 639.56 / FID 59.70；End-to-end LDM（不用图像预训练）FVD **1155.10** / FID 71.26（最差，证明图像预训练关键）；Attention-only FVD 704.41 / FID 50.01；**Ours（3D 卷积）FVD 534.17 / FID 48.26**；Ours + context-guided FVD 进一步降到 **508.82**（FID 略升到 54.16，质量换一致性）。
- 上采样器时间对齐（表 3 左）：image upsampler FVD 165.98 → **video upsampler FVD 45.39**（FID 基本不变 ~19.8，因独立超分单帧质量没掉，掉的是时间一致性）。
- **decoder 视频微调（表 3 右）极其关键**：RDS 重建 FVD 390.88→**7.61**（数量级提升），FID 32.94→9.17；WebVid 重建 FVD 35.82→18.66；Mountain Biking FVD 73.78→25.55（表 11）。decoder 微调消融（表 14）：仅用视频判别器 FVD 32.94 优于"额外加图像判别器"的 51.01——故只用视频判别器。

**零样本文生视频（SD 2.1 版，与 Make-A-Video 对齐用 10k 样本）：**
- **UCF-101（表 4/9）**：IS 越高越好、FVD 越低越好。CogVideo(EN) IS 25.27/FVD 701.59；MagicVideo FVD 699.00；Make-A-Video IS 33.00/FVD 367.23。**Video LDM(SD 2.1) IS 33.45 / FVD 550.61**（SD 1.4 版 IS 29.49/FVD 656.49）。→ IS 上**略超 Make-A-Video**，FVD 仍逊于 Make-A-Video（但后者是并发工作、额外用了 HD-VILA-100M、模型更大）。
- **MSR-VTT（表 5/10）**：CLIPSIM 越高越好。NÜWA 0.2439、CogVideo(EN) 0.2631、Make-A-Video 0.3049。**Video LDM(SD 2.1) 0.2929**（SD 1.4 版 0.2848）——超 CogVideo，逊于 Make-A-Video。

**Mountain Biking（表 13）**：Ours vs LVG，FID **7.73 vs 21.1**（大幅领先单帧质量）、人评偏好 **54.2% vs 42.2%**；但 FVD 118 vs 85.3 略逊（作者解释：第一人称背景细节剧变，本文单帧更真实但短程一致性略弱，而 FVD 偏好"平滑"——并援引 LVG 论文 §5.3 论证 FVD 不可靠，故同时做人评）。

**图像质量退化消融（附录 I.3.2）**：时间微调后图像级 FID 仅从 α=1 时的 47.00 微升到 48.26——证明训练时间层对图像质量影响极小。

评测局限：未报告 GenEval/T2I-CompBench/VBench（这些 benchmark 当时尚未流行或不适用于视频）；FVD 在两处都被作者主动质疑可靠性。

## 创新点与影响
**核心贡献**：
1. 提出 **Video LDM 范式**——把图像 LDM 转为视频生成器的高效路径：**冻结空间层 + 插入并仅训练时间对齐层（temporal attention + 3D conv）**，海量图像数据训空间、稀缺视频数据训时间。
2. 同样对**超分上采样器**做时间对齐，patch-wise 训练 + 卷积式推理，把视频推到 1280×2048 兆像素级。
3. 把公开的 **Stable Diffusion 直接变成文生视频模型**，无需重训巨型基座，模型比 Imagen Video(11.6B)/CogVideo(9B) 小得多。
4. **时间层可迁移**到不同图像 checkpoint（如 DreamBooth），首次实现**个性化文生视频**。
5. 驾驶场景达 SOTA，可生成数分钟长视频，验证作为自动驾驶仿真引擎的潜力。

**影响**：这是"在预训练图像扩散上加时间层做视频"这一主流范式的奠基性论文之一；一二作 Blattmann/Rombach 随后在 Stability AI 把同思路工程化为 **[[stable-video-diffusion]] (SVD)**。该解耦空间/时间、复用图像先验、潜空间降本的设计被后续大量 T2V 工作沿用。

**已知局限**：
- 文生视频质量受限于 WebVid-10M 的低视觉质量（微调反伤图像质量），作者预期更高质数据可解。
- convolutional-in-time 长视频生成"较脆弱"，长程更推荐 prediction model；而文生视频侧未训 prediction model（长样本留作 future work）。
- RDS 数据闭源、模型与代码未开源（NVIDIA 研究项目，数据仅供研究）。
- FVD 指标本身不可靠，依赖人评佐证。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2304.08818
- arxiv_pdf: https://arxiv.org/pdf/2304.08818
- project_page: https://research.nvidia.com/labs/toronto-ai/VideoLDM/

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2304.08818.pdf
- ../../../sources/omni/2023/align-your-latents-vldm--project-page.md
