---
title: "LTX-Video: Realtime Video Latent Diffusion"
org: Lightricks
country: EU
date: "2024-11"
type: paper
category: video
tags: [video, t2v, i2v, dit, latent-diffusion, rectified-flow, video-vae, realtime, open-source]
url: "https://arxiv.org/abs/2501.00103"
arxiv: "https://arxiv.org/abs/2501.00103"
pdf_url: "https://arxiv.org/pdf/2501.00103"
github_url: "https://github.com/Lightricks/LTX-Video"
hf_url: "https://huggingface.co/Lightricks/LTX-Video"
modelscope_url: ""
project_url: "https://ltx.video"
downloaded: [arxiv-2501.00103.pdf, ltx-video--github-readme.md, ltx-video--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
LTX-Video 是 Lightricks（以色列/EU）开源的 **首个能实时生成的 DiT 视频潜扩散模型**：通过一个 **1:192 超高压缩比 Video-VAE**（32×32×8 时空下采样、128 通道）把"块化(patchify)"操作从 transformer 入口前移到 VAE，使 2B 参数的扩散 transformer 能在极少 token 上做全时空自注意力——在 H100 上 **2 秒生成 5 秒/121 帧 768×512 视频（20 步）**，比观看还快，且在同规模开源模型人评中 text-to-video 胜率 85%、image-to-video 91%，远超 CogVideoX-2B / PyramidFlow / Open-Sora Plan。

## 背景与定位
2024 年的开源/闭源文生视频（Sora、MovieGen、CogVideoX、Open-Sora Plan、PyramidFlow、HunyuanVideo）共识是：**时空 transformer + 全局自注意力 + 3D VAE**。但这些工作普遍沿用"温和压缩"的 VAE（8×8×4 或 8×8×8，16 通道，总压缩 1:48~1:96），再在 transformer 入口用 2×2×1 patchifier 把 latent 拼成 token，得到 1:1024~1:2048 的像素-token 比。token 数决定训练/推理成本（注意力对 token 数平方复杂度），因此这条路线在高分辨率/长时长下成本陡增。

LTX-Video 的核心论点是 **"holistic（整体化）"latent diffusion**：不把 Video-VAE 和去噪 transformer 当作两个独立组件分别优化，而是优化它们的协同。两个关键决策：

1. **把压缩做到极致**（受同期 DC-VAE 启发——高空间压缩+高维 latent 对 transformer 扩散更有利），用 1:192 总压缩 + 1:8192 像素-token 比（是同类的 2 倍压缩、4 倍 token 比），让 transformer 在极小 token 集上跑全时空注意力。
2. **把"最后一步去噪"交给 VAE 解码器**，在 latent→pixel 解码的同时补回高压缩丢失的高频细节，省掉 Sora/MovieGen 那种额外的二级 upsampling/超分模型。

相对前置工作：架构 backbone 基于 [[pixart-alpha]]（把 [[dit]] 扩展为开放文本条件），训练范式用 [[rectified-flow]]（同 [[stable-diffusion-3]] / [[flux-1]]），定位是"效率优先 + 消费级 GPU 可跑 + 全开源"的视频生成，对标的是 [[cogvideox]] / [[hunyuanvideo]] / [[open-sora]] 这条开源线。

## 模型架构

### 整体：holistic latent diffusion
两阶段去噪流水线（论文 Fig 2）：transformer 在 latent 空间做 latent→latent 的多步去噪，**最后一步 latent→pixel 的去噪由 VAE 解码器完成**。

### Video-VAE（最核心创新）
- **压缩规格**：时空压缩 32×32×8（首帧单独编码为一个 latent 帧），**128 通道**，总压缩 **1:192**；因为把 patchify 放进 VAE，transformer 入口不再需要 patchifier（patch=1×1×1），像素-token 比达 **1:8192**。对比表（论文 Table 1）：MovieGen/PyramidFlow=1:96、HunyuanVideo/CogVideoX=1:48；LTX-Video=1:192。
- **因果 vs 非因果**：用 **因果(causal) VAE**（3D 因果卷积）——虽然非因果更易训出好重建，但因果 VAE 便于图像/视频联合训练，也支持首帧条件生成。3D 卷积略优于"2D 空间 + 1D 时间"的可分离卷积。
- **去噪解码器(Denoising Decoder)**：解码器被训练成一个扩散模型 `x0 = D((1−t)z0 + t·ε, t)`，把"带噪 latent"在不同噪声水平下映射到"干净像素"；由于输入输出维度不同它不能像标准扩散那样迭代，但能执行**最后一步去噪** `D(z_{t1}, t1)`。解码器直接在像素空间输出、用像素空间损失训练，训练噪声水平范围 **[0, 0.2]**（对应常见调度器的最后一段）；时间步通过 AdaLN 注入。
- **VAE 训练损失组合**：像素重建(MSE) + **Video-DWT(L1)**（8 个 3D 离散小波变换的 L1 距离，专补高频细节）+ 感知损失(LPIPS) + **Reconstruction-GAN**。
  - **Reconstruction GAN（rGAN）**：把判别器从"看单张图判真假"改为"同时看输入与重建版本（拼接），判断哪张是原图哪张是重建"。这个相对比较大幅简化判别器任务、提升 GAN 稳定性，并让判别器既匹配真实分布又充当稳健的重建损失。
  - **多层噪声注入**：仿 StyleGAN，不只在 latent 加噪，还在解码器多个层注入噪声生成多样高频细节，噪声水平按通道学习。
  - **Uniform log-variance**：宽 latent（多通道）下标准 KL 损失会让部分通道"被牺牲"以满足 KL；改用所有通道共享一个预测 logvar，把 KL 的影响均匀分摊到各通道。

### Video Transformer（基于 PixArt-α 的改进 DiT）
- 规模：**1.9B 参数**，hidden dim 2048，28 个 transformer block，FFN 倍率 4。注意力为 **Self + Cross attention**（对比 HunyuanVideo/CogVideoX 的 self-only）。
- **RoPE + 归一化分数坐标**：用旋转位置编码替代绝对位置编码；坐标用"归一化分数坐标"（空间按像素、时间按秒，相对预设最大分辨率/时长归一化），把原始 FPS 纳入时间嵌入以生成更自然运动。频率间距用**指数递增**（而非常见的逆指数），消融显示训练损失持续更低。
- **QK Normalization**：注意力点积前对 Q/K 做归一化，避免 attention logits 出现极大值导致注意力权重熵接近零；用 **RMSNorm**（优于 LayerNorm），同时整体把 PixArt-α 的 LayerNorm 换成 RMSNorm。

### 文本条件
- text encoder：**T5-XXL**（同 Imagen / DALL·E 3 / PixArt-α），加可学习投影层。
- 注入方式：**cross-attention**（实验发现优于 SD3/FLUX 的 MM-DiT）。

### 图像条件（image-to-video，零额外参数）
基于并扩展 Open-Sora 的"用扩散时间步作为条件指示"思路：放松"所有 token 同一时间步/同一噪声水平"的限制，**允许每个 token 有不同的时间步与噪声水平**。训练首帧条件时，偶尔把首帧 token 的时间步设为一个小随机值并按该水平加噪，模型很快学会把它当条件信号。推理时把条件图编码成时间维=1 的 latent，与噪声 latent 拼接展平：条件 token 时间步设小值 `tc`、其余设 `t=1`。t2v 与 i2v **同时训练**，无需特殊 token 或额外模型。

## 数据
- **来源**：公开可得数据 + 授权(licensed)素材；论文未披露具体规模/条数/配比数字（"未披露"具体量级）。
- **质量控制与过滤**：训练并使用一个**美学模型**——先用多标签网络给数百万样本打标，仅采样"共享 top-3 标签之一"的样本对做人工标注（数万对图像对，人工标哪张更美），以减少按美学过滤时的分布漂移；用这些对训练一个 **Siamese 网络**预测保序的美学分数，过滤掉低于阈值的样本。
- **运动与长宽比过滤**：移除运动量过小的视频（聚焦动态内容）；裁掉黑边以标准化长宽比。
- **微调用高美学子集**：fine-tune 阶段只用过滤出的最高美学内容。
- **重新打标(re-captioning)**：用内部自动图像/视频 captioner **对全部训练集重新生成描述**，提升图文对齐；论文给出 caption 词数分布、词云、片段时长分布的统计图。

## 训练方法
- **目标**：**Rectified Flow**（同 SD3）。前向 `zt=(1−t)z0+t·ε`，网络预测速度 `v=ε−z0`（而非预测噪声）；推理 `z_{t−Δt}=zt−Δt·v_t`。
- **时间步调度**：采纳 SD3 的对数正态采样思路并向高噪声区域 shift，**shift 幅度依 token 数（分辨率）自适应**（高分辨率需要更高噪声以维持 SNR，呼应 SimpleDiffusion）；为防尾部饥饿在 0.5 / 99.9 百分位 clamp pdf。
- **多分辨率/多时长联合训练**：同时在多种(宽×高×时长)组合上训，模型能泛化到未见过的配置。为统一序列 token 数，把视频 resize 到相近 token 量，并用 **0%~20% 随机 token dropping** 固定各序列 token 数——以此省掉复杂的 token-packing/padding。
- **图像联合训练**：把图像当作一种"分辨率-时长组合"一起训，引入视频数据里少见的概念。
- **两阶段**：预训练后，在**高美学视频子集**上微调。优化器 **ADAM-W**。论文未披露 batch size、学习率、训练步数、训练算力等具体超参（"未披露"）。
- **VAE 去噪解码器**专门用 [0,0.2] 噪声区间训练，承担最后一步去噪。

### 加速与蒸馏（来自官方 GitHub/HF 发布说明，非论文）
论文版是 2B 基座（蒸馏前），后续版本引入步数蒸馏，使"实时"进一步落到消费级/更少步数：
- **v0.9.6 蒸馏(2B)**：比非蒸馏快 **15×**，**不需要 CFG 与时空引导(STG)**，支持 **8 步（推荐）或更少**采样。
- **v0.9.7（13B dev + 13B 蒸馏）**：13B 蒸馏在 H100 上 ~10 秒出 HD 视频、3 秒出低分辨率预览；不需 CFG/STG；8 步采样；另有 LoRA 蒸馏版（仅需 1GB VRAM，可与全 13B 配合）；FP8 蒸馏版做"实时"生成。引入空间/时间 upscaler 与多尺度渲染管线。
- **v0.9.8**：13B-dev / 13B-distilled / 2B-distilled，含 FP8 权重；distilled 与 dev 可在同一多尺度管线里混用(13b-mix)；支持长达 **60 秒**长镜头；新增 IC-LoRA detailer。
- 训练-free 加速：**TeaCache**（时间步差缓存，官方称最高 ~2× 提速、无明显质量损失）。

## Infra（训练 / 推理工程）
- **训练算力**：论文未披露 GPU 数量/GPU·时/并行策略/混合精度等（"未报告"）。
- **推理（论文版基座，2B 蒸馏前）**：H100 上 **2 秒生成 121 帧 768×512 / 20 步**（faster-than-real-time）。
- **推理工程（官方发布说明）**：
  - **量化**：FP8 权重 + 专用 **FP8 kernels**（[LTXVideo-Q8-Kernels](https://github.com/Lightricks/LTXVideo-Q8-Kernels)，Ada 及以后架构提速）；社区 **LTX-VideoQ8** 8-bit 版宣称最高 3× 提速、无精度损失，RTX 4060(8GB) 一分钟内出 720×480×121。
  - **缓存**：TeaCache 训练-free 缓存，官方称最高 ~2× 提速。
  - **部署形态**：ComfyUI 集成、Diffusers 集成（`LTXConditionPipeline` + `LTXLatentUpsamplePipeline` 多尺度上采样管线，VAE tiling）、在线 demo（LTX-Studio / Fal.ai / Replicate）。
  - 约束：分辨率需被 32 整除、帧数为 8 的倍数+1（如 257），最佳工作区 <720×1280 且帧数 <257；推荐 guidance scale 3~3.5，40+ 步求质量、20~30 步求速度。
- 平台：Python 3.10、CUDA 12.2、PyTorch≥2.1.2；macOS MPS（PyTorch 2.3）支持。

## 评测 benchmark（把效果讲清楚）

### 人评（论文主结果，对标同规模模型）
仿 MovieGen 做盲评人评：1000 个 t2v prompt + 1000 个 i2v(图+prompt) 对（图由 [[flux-1]] 生成），全部生成 5 秒 768×512 视频、**40 步**，20 名评测者两两对比（含不带 LTX-Video 的对照对），按视觉质量/运动保真/prompt 遵循综合排序；为验证评测者数量充分，把 20 人分成两组各 10 人，组间胜率差 <2%。胜率(wins/(wins+losses))（论文 Table 2）：

| 任务 | Open-Sora Plan | CogVideoX-2B | PyramidFlow | **LTX-Video** |
|---|---|---|---|---|
| Text-to-video | 20% | 38% | 51% | **85%** |
| Image-to-video | 20% | 47% | 35% | **91%** |

两两胜率矩阵（论文 Fig 15）中，LTX-Video 对各模型几乎全面占优，例如 t2v 对 Open-Sora-Plan 0.96、对 CogVideoX-2B 0.85、对 PyramidFlow 0.72；i2v 对 Open-Sora-Plan 0.95、对 CogVideoX-2B 0.88、对 PyramidFlow 0.91。论文强调：在拥有显著速度优势的同时仍大幅领先质量。

> 注：论文**未报告** FID / FVD / VBench / CLIPScore 等自动化指标的具体数字，主结果以人评胜率为主。

### 关键消融
- **Reconstruction GAN vs 传统 GAN**：在 1:192 高压缩下，传统"重建+GAN"组合无法稳定重建（快动作+精细纹理处出现帧间不一致/伪影），rGAN 显著减少可见伪影（论文 Fig 16）。
- **RoPE 频率间距**：指数 vs 逆指数——指数间距训练损失始终更低（论文 Fig 17）。
- **去噪 VAE 解码器**：内部用户研究显示"VAE 解码器条件在 t=0.05 做最后一步去噪"明显优于"t=0.0 不去噪"，在高运动视频上改善最明显（缓解强压缩伪影）。

## 创新点与影响
**核心贡献**：
1. **整体化(holistic)潜扩散范式**——把 Video-VAE 与去噪 transformer 协同优化，共享去噪目标，把最后一步去噪与 latent→pixel 解码融合，省掉独立超分模块。
2. **1:192 高压缩 Video-VAE**——通过把 patchify 前移到 VAE + 一组新损失（Reconstruction GAN、Video-DWT、多层噪声注入、uniform log-variance、去噪解码器），在 2 倍压缩下保住质量，是"前所未有速度"的主要使能者。
3. **快、可及、高质量的开源视频模型**——<2B 参数、消费级 GPU 可跑、t2v+i2v 同模型、全开源（代码+权重）。

**影响**：开启了"效率优先的开源视频生成"路线，证明高压缩 VAE + 极少 token 的全时空注意力在 2B 量级即可超越同规模模型；后续快速迭代出 13B / 蒸馏 / FP8 / 多尺度上采样 / IC-LoRA 控制(depth/pose/canny) / 60 秒长镜头，并演进为 **LTX-2**（2025-10 发布预告：首个 DiT 音视频基础模型，原生 4K、最高 50 FPS、音视频同步、最长 10 秒、多 GPU 推理栈、号称比竞品低至多 50% 算力成本——权重/代码/benchmark 计划 2025 年晚些时候放出）。生态层面被 ComfyUI / Diffusers / Fal.ai / Replicate 广泛集成，社区贡献 RF-Inversion/FlowEdit/STG/Q8 等。

**已知局限**（论文）：对 prompt 表述敏感（措辞差则输出不连贯）；仅支持短视频（基座约 ≤10 秒，长时长时序一致性是开放问题）；领域特定任务（多视角合成、细粒度编辑）未充分验证；HF 卡补充：不提供事实信息、可能放大社会偏见、prompt 遵循受提示风格影响大。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2501.00103
- arxiv_pdf: https://arxiv.org/pdf/2501.00103
- github: https://github.com/Lightricks/LTX-Video
- hf: https://huggingface.co/Lightricks/LTX-Video
- project: https://ltx.video
- LTX-2 后续(blog，README 指向): https://github.com/Lightricks/LTX-2 ・ https://website.ltx.video/blog/introducing-ltx-2

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2501.00103.pdf
- ../../../sources/omni/2024/ltx-video--github-readme.md
- ../../../sources/omni/2024/ltx-video--hf-modelcard.md
