---
title: "Diffusion Transformers with Representation Autoencoders (RAE)"
org: "纽约大学 (NYU) / 谢赛宁组"
country: US
date: "2025-10"
type: paper
category: method
tags: [diffusion-transformer, representation-encoder, dinov2, autoencoder, latent-diffusion, imagenet, flow-matching, dit]
url: "https://arxiv.org/abs/2510.11690"
arxiv: "https://arxiv.org/abs/2510.11690"
pdf_url: "https://arxiv.org/pdf/2510.11690"
github_url: "https://github.com/bytetriper/RAE"
hf_url: "https://huggingface.co/collections/nyu-visionx/rae-68ecb57b8bfbf816c83cce15"
modelscope_url: ""
project_url: "https://rae-dit.github.io/"
downloaded: [arxiv-2510.11690.pdf, rae-diffusion-transformers-with-representation-autoencoders--readme.md, rae-diffusion-transformers-with-representation-autoencoders--projectpage.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
RAE 用**冻结的预训练表示编码器**（DINOv2 / SigLIP2 / MAE）+ **轻量 ViT 解码器**替换扩散 Transformer 长期沿用的 SD-VAE，把扩散过程搬到「语义丰富、不压缩」的高维隐空间里训练；配合三项针对高维隐空间的修正与一个 wide DDT head（DiT^DH），在 ImageNet 256×256 上无引导 **gFID 1.51**、有引导 **1.13**，512×512 有引导 **1.13**，且相对 SiT 提速 **47×**、相对 REPA 提速 **16×**。

## 背景与定位
潜空间生成（[[latent-diffusion-ldm]]、[[dit]] / [[sit]]）已成主流，但「自编码器」这一环几乎十年未变：绝大多数 DiT 仍依赖 [[latent-diffusion-ldm]] 的 **SD-VAE**——卷积骨干、强通道压缩（256² 图 → 32²×4 隐变量）、纯重建目标。论文指出 SD-VAE 三大问题：(1) 过时卷积骨干、计算低效（编码器约 6× / 解码器约 3× 于 RAE 的 GFLOPs）；(2) 低维隐空间限制信息容量；(3) 纯重建训练得到的隐空间缺乏全局语义结构，线性探测 ImageNet top-1 仅约 **8%**，制约生成上限。

与此同时表征学习突飞猛进（DINO/[[dinov2]]、[[mae]]、JEPA、CLIP/SigLIP），但潜扩散一直与之隔离。此前的弥合尝试走「对齐」路线——REPA（把 DiT 中间层特征对齐外部编码器）、VA-VAE、DDT、REG、ReDi——都引入额外训练阶段 / 辅助损失 / 调参复杂度。

RAE 推翻两个长期成见：① 「语义编码器不能用于忠实重建」；② 「扩散模型在高维隐空间表现差」。论文证明：冻结的语义编码器配一个轻量解码器，重建质量可**优于** SD-VAE；而且只要做对架构调整，扩散在高维语义隐空间里反而**收敛更快、生成更好**。关键洞察：高维隐空间几乎不增加计算/显存——token 数固定（由 patch size 决定），通道在 DiT 第一层即被投影到隐藏维度。本工作把「自编码」从压缩机制重新定义为表示基座。

## 模型架构
**两阶段管线**：Stage 1 训练 RAE（冻结编码器 + 训练解码器）；Stage 2 在 RAE 隐空间上训练扩散 Transformer。

**RAE（表示自编码器）**：
- 编码器 E：冻结的预训练 ViT 表示编码器，丢弃 [CLS]/[REG] token、只保留 patch token。三个代表性选择——**DINOv2-B**（pe=14, d=768，自蒸馏自监督）、**SigLIP2-B**（pe=16, d=768，语言监督）、**MAE-B**（pe=16, d=768，掩码自编码）；DINOv2 还研究 S/B/L（d=384/768/1024）。**不做通道压缩**，N = HW/pe² 个 token、每 token d 维。
- 编码器归一化：对每个 token 做 channel 方向的 LayerNorm（零均值单位方差）；因 ViT 末层已有 LN，只需取消其 affine 参数（线性变换不损表征）。实操用 **DINOv2-with-Registers**；由于 DINOv2 只有 pe=14，把输入插值到 224×224 但解码器 pd=16，保证产出 256 token 并重建 256×256。
- 解码器 D：标准 ViT（默认 **ViT-XL**，也试 ViT-B/L），patch size pd（默认 pd=pe），输入端 prepend 一个可学习 [CLS] token（解码后丢弃，沿用 MAE 设计）；将 token 映射回像素。
- **隐空间形状**：256×256 图 → 256 个 token，与 SD-VAE 系 DiT 的序列长度一致（latent_size `[768, 16, 16]`，即 16×16=256 token、768 通道）。隐空间用一个 BatchNorm-like 归一化层（按 [C,H,W] 计算训练集均值/方差）做标准化。

**Stage-2 扩散 Transformer**：backbone 用 **LightningDiT**（DiT 变体），**patch size = 1**（RAE token 已经是序列），256² 图序列长 256，故计算量与 VAE 系 DiT 几乎相同（patch 化 <1% GFLOPs）。三项关键修正（见「训练方法」）+ 一个新结构 **DiT^DH**：

- **DiT^DH（DiT with wide DDT Head）**：受 DDT（Decoupled Diffusion Transformer）启发但动机不同。在标准 DiT 主干 M 之后接一个**浅而宽**的 transformer head H 专做去噪：zt = M(xt | t, y)；vt = H(xt | zt, t)。默认 head 为 **2 层、宽 2048**。作用：在不引入二次方 FLOPs 的前提下「加宽」模型以满足高维隐空间对宽度的要求，同时过滤高维隐变量里的噪声信息。
- 其它细节：连续时间 flow-matching、时间步用 Gaussian Fourier embedding、token 同时加 APE 与 RoPE（有无 APE 差异不大）；DiT^DH 的 head 不重复加 APE。模型配置表（Dim/Heads/Depth）：S 384/6/12，B 768/12/12，L 1024/16/24，XL 1152/16/28，XXL 1280/16/32，H 1536/16/32，G 2048/16/40，T 2688/21/40。

## 数据
- **训练数据**：主要用 **ImageNet-1K**（类条件生成，1000 类）。Stage 1 解码器、Stage 2 扩散均在 ImageNet-1K 上训练；多数实验 256×256；512 分辨率（不走解码器上采样时）直接在 512×512 上训。
- **数据增强（解码器）**：先 resize 到 384×384 再随机裁剪到 256×256；判别器前用 differentiable augmentation（DiffAug 默认超参）。
- 本工作是**类条件 ImageNet 生成的方法学研究**，不涉及大规模图文对、re-captioning、美学/安全过滤等 T2I 数据工程（未涉及，故未披露）。

## 训练方法
**Stage 1 — RAE 解码器训练**（编码器冻结）：
- 损失 Lrec = ωL·LPIPS + L1 + ωG·λ·GAN，ωL=1.0、ωG=0.75；GAN 自适应权重 λ = ‖∇_x̂ Lrec‖ / (‖∇_x̂ GAN‖+ε)（沿用 VQGAN）。
- 判别器：基于 StyleGAN-T，但用冻结 **DINO-S/8**（而非 S/16）做判别器骨干——更稳、避免解码器生成对抗 patch；去掉 virtual BN 改用标准 BN；输入统一插值到 224×224。
- 超参（Table 12）：Adam，max lr 2e-4 → min 2e-5 余弦衰减，betas (0.5,0.9)，weight decay 0，batch size 512，warmup 1 epoch；解码器训 16 epoch（adv. loss 第 8 epoch 起），判别器训 10 epoch（disc. 第 6 epoch 起）。

**Stage 2 — 扩散训练**：
- 目标：**flow matching / rectified flow**，线性插值 xt=(1−t)x+tε，预测速度 v=ε−x。ODE 采样（Euler，默认 50 步）。
- 三项「驯服高维隐空间」的关键修正（论文核心方法贡献）：
  1. **DiT 宽度需 ≥ token 维度**：发现标准配方在 RAE 上直接失败（DiT-S 完全崩，DiT-XL 也显著差于 VAE 版）。理论（Theorem 1）+ 单图过拟合实验证明：扩散训练向数据注入全维高斯噪声，把低维流形「扩散」成满秩，故模型宽度 d 必须 ≥ 表示编码器 token 维 n，否则连一张图都无法过拟合（损失下界 (n−d)/n）；加深度无济于事。据此为 DINOv2-B（n=768）配 DiT-XL（宽 1152）。
  2. **维度相关的 noise-schedule shift**：以往按「分辨率」做 schedule shift 的工作只考虑空间维（C≤16）。本文主张应按**有效数据维 = token数 × token维**来 shift。采用 Esser(2024) 的 shift（基维 n=4096，α=√(m/n)）。消融：w/o shift gFID 23.08 → w/ shift **4.81**（巨大提升）。
  3. **Noise-augmented decoding（噪声增强解码）**：RAE 解码器只见过干净隐变量（离散支撑），而扩散采样会产出含噪/略偏分布的隐变量，造成 OOD。对解码器训练加噪声 n~N(0,σ²I)，并让 σ 从 |N(0,τ²)| 采样。消融：gFID 4.81 → **4.28**（rFID 0.49→0.57 略升，符合「平滑隐分布」直觉）；τ 越大 gFID 越好（τ=1.0 → 4.20）。
- 优化（DiT）：严格沿用 LightningDiT——AdamW，**恒定 lr 2e-4**，batch size **1024**，EMA 0.9999；DiT 无不稳定。
- 优化（DiT^DH）：发现 LightningDiT 配方会在后期 loss spike、早期 EMA 收敛慢；改用 lr 从 2e-4 线性衰减到 2e-5、恒定 warmup **40 epoch**、EMA 改 **0.9995**、梯度裁剪 1.0。默认训 80 epoch（也报 720/800 epoch）。仅报告 EMA 模型。
- **引导**：主用 **AutoGuidance**（用弱模型引导强模型）——比带 interval 的 CFG 更易调且更好。用最小的 **DiT^DH-S 早期 checkpoint** 当引导模型（默认 scale 1.5、20-epoch ckpt；最佳 1.13 用 scale 1.42 + 14-epoch ckpt）；训练这个引导模型仅需被引导模型约 **0.05%** 算力。CFG 无 interval 反而升 FID；带 interval 的 CFG 经网格搜索可竞争但仍逊于 AutoGuidance。
- **未涉及**蒸馏/一致性模型/步数蒸馏（本工作不做加速蒸馏，仅靠 50 步 Euler）。

## Infra（训练 / 推理工程）
- **硬件/框架**：RAE 全部训练与推理用 **PyTorch/XLA on TPU**；致谢 **Google TPU Research Cloud (TRC)**。评测用单台 **v6e-8** 生成 50K 样本；800-epoch DiT^DH-XL 的生成在 **4×A100** 机器上完成，FID 在 CPU 上算（缺 TF GPU 支持）。VAE baseline 用内部 **JAX** 代码库训练。
- **官方开源代码（bytetriper/RAE）**：同时提供 **PyTorch/GPU**（torchrun DDP，单/多卡）与 **TorchXLA/TPU** 实现；另有 JAX/TPU 实现 `willisma/diffuse_nnx`。建议 Stage-2 用 **fp32** 更稳（bf16 也支持）；支持 `torch.compile`、wandb、断点续训、在线评测、统计量计算。
- **计算量优势**：因 patch size=1 + token 数固定，DiT 在 RAE/VAE/pixel 上的主干计算量基本相同（差异仅在 patch 化，<1% GFLOPs）；高维隐变量「免费」。RAE 编/解码器 GFLOPs 远低于 SD-VAE（Table 1 实测，256² 单图）：编码器 SD-VAE 310.4 vs RAE DINOv2-B **84.5** / SigLIP2-B 79.1 / MAE-B 68.0；解码器 RAE ViT-B 22.2 / ViT-L 78.1 / ViT-XL 106.7。论文文字总结：SD-VAE 编码器/解码器分别约为 RAE 的 **6×/3×**（即 ViT-XL 解码器仅 SD-VAE 解码器约 1/3 算力；ViT-B 解码器 22.2 即超 SD-VAE 重建质量且 GFLOPs 省 **14×**）。
- **推理**：标准 ODE Euler 50 步（>50 步收益饱和）；FID-50K 评测用 class-balanced 采样（每类 50 图，比随机采样一致低约 0.1 FID）。
- **训练效率**：DiT^DH-XL 约 **5×10^11 GFLOPs** 即达最优 FID，比对手省 **40× 以上**算力。

## 评测 benchmark（把效果讲清楚）
**重建（rFID，ImageNet-1K val，越低越好）**——Table 1：
- RAE 全面优于 SD-VAE（rFID 0.62）：DINOv2-B **0.49**、SigLIP2-B 0.53、MAE-B **0.16**（最佳重建，但生成最差，说明低 rFID ≠ 好 tokenizer）。
- 解码器越大 rFID 越好：ViT-B 0.58 → ViT-XL 0.49；ViT-B 已超 SD-VAE 且 GFLOPs 省 **14×**，ViT-XL 仅 SD-VAE 1/3 算力。
- 编码器 S/B/L 的 rFID 稳定（0.52/0.49/0.52）。
- **表征质量**（线性探测 top-1）：RAE 继承编码器强表征（远高于 SD-VAE 的约 8%）。

**生成（gFID-50K，class-conditional，越低越好）**：
- ImageNet **256×256**（Table 8）：DiT^DH-XL (DINOv2-B, 839M)
  - 无引导：20 ep 3.71 → 80 ep 2.16 → **800 ep 1.51**（IS 242.9，Prec 0.79，Rec 0.63）；
  - 有引导（AutoGuidance）：**1.13**（IS 262.6，Prec 0.78，Rec 0.67）。
  - 超越全部先前扩散方法：VAE 系 SiT-XL 8.61→2.06(g)、REPA 5.78→1.42(g)、DDT 6.27→1.26(g)、REPA-E 1.70→1.15(g)、VA-VAE 2.17→1.35(g)、MDTv2 1.58(g)；AR 系 VAR 1.73(g)、MAR 1.55(g)、xAR 1.24(g)。RAE 1.13 优于所有。
  - 论文还指出 FID 评测协议不一致（class-balanced vs random 采样差约 0.1），重跑了若干 baseline（数字因此略高于原报告）。
- ImageNet **512×512**（Table 7，400 ep + AutoGuidance）：DiT^DH-XL (DINOv2-B) **gFID 1.13**（IS 259.6，Prec 0.80，Rec 0.63），超越前最佳 EDM-2 的 1.25、SiD2 1.50、DDT 1.28。
- **收敛/缩放**：DiT^DH-XL 在约 5×10^10 GFLOPs 即超过 REPA-XL/MDTv2-XL/SiT-XL；相对 SiT 提速 **47×**、相对 REPA-XL 提速 **16×**。DiT^DH-S gFID 6.07 已胜更大的 REPA-XL；S→B 降到 3.38。DiT^DH-B 仅约 40% 训练 FLOPs 即超 DiT-XL。

**关键消融**：
- **DiT^DH 对 RAE 的依赖**（80 ep、无引导 gFID）：在 SD-VAE 隐空间上 DiT^DH 反而更差（Table 10：DiT-XL 7.13 vs DiT^DH-XL 11.70），在 pixel 上虽优于 DiT（Table 11：DiT^DH-XL 30.56 < DiT-XL 51.09）但二者都远逊 RAE 版（同 DiT^DH-XL：pixel 30.56 vs RAE/DINOv2-B **2.16**）。说明 wide head 的价值只在高维隐空间体现，且**结构化表征不可或缺**（高维度本身不够）。
- **不同编码器生成**（Table 15a，w/o vs w/ 噪声增强）：DINOv2-B 4.81/4.28 最佳，SigLIP2-B 6.69/4.93，MAE-B 16.14/8.38（重建最好但生成最差）→ 默认选 DINOv2-B。
- **编码器规模**（Table 6）：DiT^DH 始终胜 DiT 且差距随编码器增大而拉大（DINOv2-L 下 6.09→2.73）。
- **DDT head 形状**（Table 16，gFID 越低越好）：宽而浅最佳——2 层/2048(G) **2.16** < 4 层/2048(G) 2.31 < 6 层/1152(XL) 2.36（2 层与 4 层 GFLOPs 26.78 vs 53.14，加深无收益）；更大 RAE 需更宽 head（Table 17：DINOv2-L 在 2688-T 仍获益）。
- **高分辨率高效合成**（Table 9）：让解码器 pd=2pe，用 256² 的 256 token 直接重建 512²——复用 256 训练的扩散模型、换上采样解码器即可，gFID 1.61 / rFID 0.97（vs 直接 1024 token 训练 1.13/0.53），算力省 **4×**。

## 创新点与影响
**核心贡献**：
1. 提出 **RAE**——用冻结预训练表示编码器 + 轻量训练解码器构成自编码器，直接在「不压缩、语义丰富」的高维隐空间训扩散，重建优于 SD-VAE 且表征强（线性探测远高于 ~8%），**无需 REPA 式辅助对齐损失**。
2. 系统性「驯服高维隐空间」的三件套：**DiT 宽度 ≥ token 维**（含 Theorem 1 理论下界）、**有效数据维相关的 noise-schedule shift**、**噪声增强解码**。
3. 提出 **DiT^DH**（wide & shallow DDT head），在不增二次方算力下满足宽度需求并过滤噪声，缩放性显著优于普通 DiT。
4. SOTA 数字：ImageNet 256 无引导 1.51 / 有引导 1.13、512 有引导 1.13，并带来 16–47× 训练提速。

**影响**：把「表征 × 生成」从「对齐」范式推进到「直接复用语义隐空间」范式，主张 **RAE 应成为扩散 Transformer 训练的新默认**；为统一理解/生成（共享语义隐空间）提供了一条干净路径。属 2025 年「表示×生成」方向代表作（谢赛宁组，承 [[dit]]/[[sit]]/REPA 脉络）。

**已知局限**：
- 实验局限于 **ImageNet 类条件生成**，未验证大规模文本到图像（T2I）/视频；无 text encoder、无图文数据工程。
- 仍需 50 步 ODE 采样，未做步数蒸馏/一致性加速。
- 依赖外部预训练编码器质量（DINOv2-B 最优，但 SigLIP2/MAE 明显更弱），编码器选择敏感。
- FID 在低值区绝对意义减弱（论文自陈），且评测协议差异（balanced/random 采样）需社区统一。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2510.11690
- arxiv_pdf: https://arxiv.org/pdf/2510.11690
- github (官方代码，正确仓库): https://github.com/bytetriper/RAE  （worklist 里的 github.com/bytedance/RAE 为 404，已校正）
- jax/tpu 实现: https://github.com/willisma/diffuse_nnx
- project_page: https://rae-dit.github.io/
- hf_models: https://huggingface.co/collections/nyu-visionx/rae-68ecb57b8bfbf816c83cce15

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2510.11690.pdf  （论文全文 PDF，已精读正文+附录 A-J）
- ../../../sources/omni/2025/rae-diffusion-transformers-with-representation-autoencoders--readme.md  （官方 GitHub README）
- ../../../sources/omni/2025/rae-diffusion-transformers-with-representation-autoencoders--projectpage.md  （项目页 markdown 快照）
