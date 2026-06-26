---
title: "PixArt-δ: Fast and Controllable Image Generation with Latent Consistency Models"
org: "Huawei Noah's Ark Lab"
country: China
date: "2024-01"
type: tech-report
category: t2i
tags: [pixart, dit, lcm, consistency-distillation, controlnet, transformer, text-to-image, few-step, huawei]
url: "https://arxiv.org/abs/2401.05252"
arxiv: "https://arxiv.org/abs/2401.05252"
pdf_url: "https://arxiv.org/pdf/2401.05252"
github_url: "https://github.com/PixArt-alpha/PixArt-alpha"
hf_url: "https://huggingface.co/PixArt-alpha/PixArt-LCM-XL-2-1024-MS"
modelscope_url: ""
project_url: "https://pixart-alpha.github.io/"
downloaded: [arxiv-2401.05252.pdf, pixart-delta-lcm-controlnet--readme.md, pixart-delta-lcm-controlnet--hf-lcm-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
PixArt-δ 在 [[pixart-alpha]]（0.6B DiT 文生图）之上叠加两件加速 / 可控套件：用**潜在一致性蒸馏（LCD/LCM）**把推理压到 **2~4 步、A100 上 1024×1024 仅 0.5s（相对 PixArt-α 提速 7×）**，并提出专为 Transformer 设计的 **ControlNet-Transformer** 实现细粒度结构控制。整套蒸馏可在单张 32GB V100 上一天内完成，8-bit 推理下仅需 <8GB 显存。

## 背景与定位
属于 PixArt 三部曲里"快 + 可控"的一环：α 解决**低成本训练**（753 A100 天，FID-30K 7.32）、δ 解决**少步快推理 + 结构可控**、Σ（后续）解决 4K 与弱到强。δ 不重训基模，而是把两条当时已被验证在 U-Net/LDM 上的技术——[[latent-consistency-models]]（LCM，把反向扩散看成解增广 PF-ODE，2~4 步出图）和 [[controlnet]]（冻结主干 + 可训练拷贝 + zero-conv 注入条件）——**移植到 DiT 架构**。

关键矛盾在于：两项技术原本都是为 U-Net 量身定做。LCM 的 noise schedule 默认贴合 Stable Diffusion；ControlNet 依赖 U-Net 显式的 encoder/decoder + skip-connection。直接照搬到没有这种层级结构的纯 Transformer 上效果会打折，δ 的贡献就是把两者"翻译"到 DiT 上并做必要改造。报告自我定位为"Stable Diffusion 家族的开源替代品"。

## 模型架构
**基模（teacher）**：完全沿用 PixArt-α 的 DiT——
- **Backbone**：基于 DiT 的 Transformer，共 **28 个 Transformer block**，约 **0.6B** 参数；在 DiT 基础上加入 cross-attention 注入文本条件，并精简了 class-condition 分支（PixArt-α 设计）。
- **Text encoder**：冻结的 **T5-v1.1-XXL（4.3B）**，长文本 caption。
- **VAE**：SD 的 `sd-vae-ft-ema`（约 **80M**），把图像编码进潜空间，δ 在潜空间做蒸馏。
- **分辨率**：支持 512px / 1024px 多尺度（multi-scale），δ 在两种分辨率上分别蒸馏。

**LCM 改造**：把基模当 teacher，蒸出一个结构、可训练参数与 teacher **完全一致**的 consistency 函数 fθ(ẑ, ω_fix, c, tn)，因此学生可直接用 teacher 权重初始化、无损起步。与原版 LCM 不同的是 δ **去掉了 guidance-scale embedding**——原 LCM 把 CFG scale ω 从区间 [ω_min, ω_max] 采样并做 Fourier 嵌入，δ 改用**固定常数 ω_fix = 4.5**（α 的最优值），省掉嵌入操作、简化实现且效果更好。同时支持 **LCM-LoRA**（用 LoRA 训蒸馏模块，便于快速适配）。

**ControlNet-Transformer 改造**（核心架构创新）：
- 先把 zero-convolution 换成 **zero linear**（weight、bias 都初始化为 0 的线性层）。
- 对比了两种接法：
  - **ControlNet-UNet（朴素移植）**：把前 14 个 block 当作"encoder"、后 14 个当"decoder"，对前 14 个做可训练拷贝，输出用加法经 14 条"skip-connection"接到后 14 个 block。问题：Transformer 本无显式 encoder/decoder 与 skip，这种接法偏离 Transformer 原生数据流，**效果差**。
  - **ControlNet-Transformer（最终方案）**：只对**前 N 个 base block**做可训练拷贝；第 i 个可训练 block 的输出经 zero linear 后，加到第 i 个**冻结** block 的输出上，作为第 (i+1) 个冻结 block 的输入。**严格沿着 PixArt 原本的逐层数据流**，因此收敛更快、效果显著更好。
  - 消融选 **N = 13** 为最终模型（28 个 block 取前 13 个做拷贝）。ControlNet checkpoint（512/1024）参数量约 **0.9B**（README 权重表口径；= 0.6B 冻结基模 + 13 个 base block 的可训练拷贝），独立的 **ControlNet-HED-Encoder 约 30M**（README 权重表）。

## 数据
- **LCM 蒸馏**：在 **120K 条内部高质量图文对**上做潜在一致性蒸馏；512px、1024px 两档分辨率共用这批数据。报告强调数据量极小（对比 SDXL LCM-LoRA 用 650K、SD-V1.5-LCM 用 650K）。
- **ControlNet 训练**：训练集为 **3M 对 HED 边缘图 + 图像**；HED 在内部数据上提取。当前条件只做了 **HED 边缘**，canny 等其它条件列为未来工作。
- 数据**来源、清洗 / 过滤、re-captioning、美学 / 安全过滤等细节均未在本报告披露**（基模 PixArt-α 用的是 25M 图、含 SAM 数据与 LLaVA 自动标注的密集 caption，但那是 α 报告的内容，δ 报告未重复展开）。

## 训练方法
**训练目标 = 潜在一致性蒸馏（LCD）**，带 CFG 的伪代码见报告 Algorithm 1：
- 三个模型协同——**Teacher**（ODE solver Ψ 的去噪器，即 PixArt-α）、**Student** fθ、**EMA Model** fθ⁻。
- 在 t_{n+k} 采噪，Teacher 去噪得 ẑ^T；用 ODE solver Ψ（**DDIM-Solver**）从 z_{t_{n+k}} 与 ẑ^T 算出带 CFG 的 ẑ^{Ψ,ω_fix}；EMA Model 进一步去噪到 ẑ^E；Student 直接从 z_{t_{n+k}} 去噪到 ẑ^S；**优化目标 = 最小化 d(ẑ^S, ẑ^E)**（一致性蒸馏损失）。EMA 更新 θ⁻ ← μθ⁻ + (1−μ)θ。
- **CFG 处理**：固定 ω_fix（去掉 ω embedding），ẑ^{Ψ,ω_fix} = z + (1+ω_fix)·Ψ(…,c) − ω_fix·Ψ(…,∅)。
- **Skipping-step**：跳步间隔 **k = 20**（沿用 LCM-LoRA），加速收敛。

**Noise schedule 适配**（关键 trick）：原 LCM 的 schedule 贴合 SD，δ 把扩散过程的 βt 从 *scaled-linear* 改成 *linear*，β_{t0} 0.00085→0.0001、β_{tT} 0.012→0.02，使蒸馏阶段 **logSNR 更高**、贴合 PixArt-α 的噪声分布；δ 可参数化更宽的噪声分布，有利于高分辨率生成（参考 Hoogeboom simple-diffusion、Ting Chen noise-scheduling）。

**关键超参 / 消融结论**：
- 蒸馏在 **2 张 V100** 上、总 batch size **24**、学习率 **2e-5**、EMA rate **μ = 0.95**、**AdamW**。
- **CFG scale 消融**：常数 3.5 / 4.5 vs LCM 的 ω-embed，结论是**常数 guidance 比复杂 CFG 嵌入更好**。
- **Batch size 消融**：2 V100（每卡 12 图）vs 32 V100，更大 batch 改善 FID / CLIP；但小 batch 也能快速收敛、画质相当。
- **收敛**：约 **5000 iteration** 即收敛，之后提升微弱。
- **ControlNet 训练**：gradient accumulation = 4；16 张 32GB V100；除 N=27（batch 2）外每卡 batch 12；**~1000 步内"sudden converge"**（与原 ControlNet 一致的突变收敛现象，简单边缘更早收敛），之后细节随步数缓慢精修。

## Infra（训练 / 推理工程）
- **蒸馏训练**：可在 **单张 32GB V100、一天内**完成；论文实际用 2 张 V100（总 batch 24），完整 finetune 显存 <24GB，消费级 GPU 可跑。对比 SDXL LCM-LoRA 需 ~80GB、SD-V1.5-LCM 需 ~80GB。
- **ControlNet 训练**：16 张 32GB V100。
- **推理加速**：核心是 **4 步采样**（vs PixArt-α 14 步 DPM-Solver、SDXL 25 步）；**8-bit 推理**（diffusers 方案）把 1024px 生成压到 **<8GB VRAM**，甚至可跑 CPU；torch.compile 再提 20~30%。
- **推理速度**（1024×1024、batch 1，4 步）：A100 **0.5s**（HF card 记 0.51s）、V100 **0.8s**、T4 **3.3s**。同条件对照：SDXL LCM-LoRA(4 步) A100 1.2s / T4 8.4s；PixArt-α(14 步) A100 2.2s / T4 16.0s；SDXL 标准(25 步) A100 3.8s / T4 26.5s。
- 部署：开源 diffusers `PixArtAlphaPipeline`（LCM 版 `num_inference_steps=4, guidance_scale=0.`），HF / OpenXLab 在线 demo。

## 评测 benchmark（把效果讲清楚）
本报告是技术报告，**以速度对照表 + 大量定性图（消融、收敛过程）为主，未给出系统的 FID/CLIP/GenEval 横向数字表**：
- **速度**（最核心硬指标，见上 Infra 表）：A100 1024px 0.5s，较 PixArt-α 提速 **7×**，4 步对 25 步。
- **训练收敛**：LCD ~5000 iter 收敛；ControlNet ~1000 步 sudden-converge。
- **LCM 消融**（图 2，用 **FID / CLIP score** 作指标，仅以曲线呈现、无表格数值）：常数 ω 优于 ω-embed；更大 batch 改善 FID / CLIP。
- **ControlNet 消融**（图 5，定性）：ControlNet-Transformer 全面优于 ControlNet-UNet，收敛更快、可控性随拷贝块数 N 增大而增强；多数场景 N=1 已足够，人脸 / 人体轮廓等难边缘随 N 增大更好，**最终 N=13**。
- **画质对照**（定性，图 7）：δ(4 步) vs SDXL-LCM(4 步)、vs teacher PixArt-α(14 步 DPM-Solver)，δ 在 4 步下保持高质量。
- **基模锚点**（来自 README，PixArt-α 数据）：PixArt-α 0.6B、25M 图、**FID-30K 7.32（zero-shot）/ 5.51（COCO FT）**、753 A100 天——δ 不改变这些画质指标，只做加速与可控。
- 报告**未报告** GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / 人评 ELO 等，**严禁据此编造**。

**已知局限**（HF card）：非完美写实；难以渲染清晰文字；compositionality（如"红立方体在蓝球上方"）较弱；手指等细节可能不正确。

## 创新点与影响
- **核心贡献 1——LCM-on-DiT**：首批把潜在一致性蒸馏成功落到 DiT/Transformer 文生图上的工作，并给出适配 trick（去 ω-embed 用固定 ω_fix、noise schedule 从 scaled-linear 改 linear 抬高 logSNR），证明少步加速不限于 U-Net。
- **核心贡献 2——ControlNet-Transformer**：指出 ControlNet 的 U-Net encoder/decoder + skip 假设不适配 Transformer，提出"对前 N 个 block 做可训练拷贝、zero-linear 残差注入、严格顺着原数据流"的新接法，为后续 DiT 系（含 MMDiT、SD3、FLUX 时代）的结构控制提供了范式参考。
- **工程影响**：把高质量 1024px 文生图的**蒸馏门槛降到单卡 32GB / 一天**、**推理降到 <8GB / 0.5s**，显著提升开源可及性，是 PixArt 三部曲"快 + 可控"支柱。
- **局限**：ControlNet 仅实现了 HED 条件（canny/depth/pose/seg 留作未来）；继承基模在文字、compositionality、手部上的弱点；报告缺系统化定量 benchmark 表（速度强、画质指标偏定性）。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2401.05252
- paper (PDF): https://arxiv.org/pdf/2401.05252
- code (GitHub): https://github.com/PixArt-alpha/PixArt-alpha
- project homepage: https://pixart-alpha.github.io/
- HF LCM weights: https://huggingface.co/PixArt-alpha/PixArt-LCM-XL-2-1024-MS
- HF ControlNet weights: https://huggingface.co/PixArt-alpha/PixArt-ControlNet/tree/main
- HF LCM demo: https://huggingface.co/spaces/PixArt-alpha/PixArt-LCM

## 一手源存档（sources/）
- [arxiv-2401.05252.pdf](https://arxiv.org/pdf/2401.05252)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/pixart-delta-lcm-controlnet--readme.md)
- [hf-lcm-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/pixart-delta-lcm-controlnet--hf-lcm-card.md)
