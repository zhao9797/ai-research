---
title: "VQ-Diffusion：用于文生图的向量量化扩散模型"
org: "Microsoft Research / 中国科学技术大学 (USTC)"
country: China
date: "2021-11"
type: paper
category: method
tags: [discrete-diffusion, mask-and-replace, vq-vae, text-to-image, non-autoregressive, masked-generation]
url: "https://arxiv.org/abs/2111.14822"
arxiv: "https://arxiv.org/abs/2111.14822"
pdf_url: "https://arxiv.org/pdf/2111.14822"
github_url: "https://github.com/microsoft/VQ-Diffusion"
hf_url: "https://huggingface.co/microsoft/vq-diffusion-ithq"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2111.14822.pdf, vq-diffusion--readme.md, vq-diffusion--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
VQ-Diffusion 在 VQ-VAE 的离散图像 token 上做条件**离散扩散**（DDPM 的离散变体）来生成图像，提出 **mask-and-replace（掩码+替换）** 前向加噪策略，是**首个把离散/掩码扩散用于文生图**的工作；其 VQ-Diffusion-F 模型在 MSCOCO 上 FID=**13.86**，以约 1/10 的参数量（Base 370M）超过 DALL-E（27.50）与 CogView（27.10），且 fast-inference 配置（25 步）比同结构自回归模型快 **15 倍**。（CVPR 2022 Oral）

## 背景与定位
2021 年文生图主流是两条路线：GAN（StackGAN/AttnGAN/DM-GAN/DF-GAN，在鸟/花等单域上 FID 不错，但因卷积局部性归纳偏置难以应对 MSCOCO 这类多物体复杂场景）和**自回归（AR）token 模型**（[[dall-e-1]]、CogView、M6——把图像离散成 token，用大 Transformer 按光栅扫描顺序逐 token 建模联合分布）。

论文指出 AR 路线有两大固有缺陷：
1. **单向偏置（unidirectional bias）**：token 按从左上到右下的固定顺序预测，只能看到前缀，忽略了 2D 图像结构——某位置的关键上下文可能来自图像任意方向，而非仅左/上。
2. **误差累积（accumulated prediction error）**：训练用 teacher-forcing 喂 ground truth，推理却基于自己先前采样的 token；token 一旦预测就不可更正，错误会传播到后续所有 token（exposure bias）。此外 AR 每个 token 需一次前向，推理时间随分辨率线性增长，即使在 32×32 隐空间也很慢。

VQ-Diffusion 用**非自回归**的离散扩散替换 AR 解码器来同时消除这两个缺陷：双向全局注意力消除单向偏置；每步重采样全部 token、可修正错误 token，避免误差累积。它沿着 VQ-VAE→[[taming-transformers-vqgan]] 的离散隐空间路线，把 [[ddpm]] 从连续像素扩散推广到**离散类别**扩散（前置工作为 D3PM、Multinomial Diffusion/Argmax Flow、ImageBART——但这些只在像素或无条件/语言上做，VQ-Diffusion 首次用于条件文生图）。它的"掩码 token + 双向重采样"范式与 [[maskgit]]（同期/稍后）一脉相承，启发了后续大量离散/掩码生成路线（如 Paella、MUSE 等）。

## 模型架构
**两阶段框架（图像表示 + 隐空间生成）：**

- **第一阶段（图像 tokenizer，冻结复用）**：VQ-VAE。文生图实验**直接采用 VQGAN 公开发布、在 OpenImages 上训练的模型**（不自训），把 256×256 图像下采样为 **32×32 = 1024 个 token**；去掉无用码后**码本大小 K=2886**。类条件 ImageNet 实验改用 VQGAN 在 ImageNet 上训练的 VQ-VAE，下采样为 **16×16=256 token**；无条件 FFHQ 同为 16×16。VQ-VAE 用 EMA 更新码本（而非直接用 VQ loss 第二项），训练损失为 L1 重建 + codebook/commitment 项（β 权重）。
- **文本编码器（冻结）**：采用 **CLIP（ViT-B）的预训练分词器/编码器**，把一句话编码成长度 **77** 的条件特征序列。图像、文本编码器在扩散训练中**全部冻结**。
- **第二阶段（扩散图像解码器）**：一个 **encoder-decoder Transformer**，估计去噪分布 pθ(x̃₀|xₜ, y)。每个 Transformer block 含 **full self-attention（图像 token 之间，双向全局上下文）+ cross-attention（注入文本条件）+ FFN**。时间步 t 通过 **AdaLN（Adaptive Layer Normalization）** 注入：AdaLN(h,t)=aₜ·LayerNorm(h)+bₜ，其中 aₜ、bₜ 由 timestep embedding 线性投影得到。解码器末端接 softmax 输出每个位置在 K+1 个类别上的分布。
- **类条件变体**：去掉 text encoder 与 cross-attention，把类标签通过 AdaLN 注入；24 个 block、维度 512、FFN 用卷积、扩张率 4。

**参数量与设置（文生图）：**
- **VQ-Diffusion-S（Small）**：18 个 Transformer block，维度 192，FFN 用 kernel=3 卷积、扩张率 2，**约 34M** 参数（与 GAN 基线参数量相当，用于公平对比）。
- **VQ-Diffusion-B（Base）**：19 个 block，维度 1024，FFN 两个线性层中间扩到 4096，**约 370M** 参数。
- **VQ-Diffusion-F**：Base 结构先在 Conceptual Captions 上预训练，再在各目标数据集上 fine-tune（最优配置）。

## 数据
**训练 tokenizer 的数据非自建**（复用 VQGAN 公开模型，分别基于 OpenImages / ImageNet）。**文生图扩散训练数据：**
- **标准基准**：CUB-200（8855 训练 / 2933 测试，200 种鸟，每图 10 条文本描述）、Oxford-102（8189 张花，102 类，每图 10 条描述）、MSCOCO（82k 训练 / 40k 测试，每图 5 条描述）。
- **大规模可扩展性**：Conceptual Captions（CC3M+CC12M 共 ~15M 图，**按词频过滤出 7M 子集**以平衡文本与图像分布）；**LAION-400M**（4 亿图文对）——只训练 cartoon / icon / human 三个子集，分别约 **0.9M / 1.3M / 42M** 图，每个子集按文本做过滤。
- **类条件 / 无条件**：ImageNet（类条件）、FFHQ256（无条件，70k 高质量人脸）。

清洗/过滤层面仅披露"按词频过滤 CC 到 7M""按文本过滤 LAION 子集"，**未披露**美学打分、安全过滤、re-captioning 或合成数据细节（2021 年的工作，尚无这些工程）。

## 训练方法
**训练目标 = 离散扩散的变分下界（VLB）+ 重参数化辅助损失。**

- **离散前向过程（mask-and-replace 是核心创新）**：每个 token 状态扩展为 **K+1**（增加一个特殊 **[MASK] token**）。前向转移矩阵 Qₜ∈ℝ^((K+1)×(K+1)) 定义每个普通 token 在一步内：以 γₜ 概率被替换为 [MASK]、以 Kβₜ 概率被均匀重采样到任一类别、以 αₜ=1−Kβₜ−γₜ 概率保持不变；[MASK] token 一旦出现则永远保持。相比纯 mask（D3PM 的 absorbing）或纯 uniform replace：① 被破坏的位置（[MASK]）对网络显式可见，降低反向难度；② 论文证明必须掺入少量 uniform 噪声，否则 xₜ≠x₀ 时会得到平凡后验；③ 随机替换迫使网络理解全局上下文而非只盯 [MASK]；④ 累积矩阵 Q̄ₜ 与 q(xₜ|x₀) 可闭式计算（Q̄ₜv(x₀)=ᾱₜv(x₀)+(γ̄ₜ−β̄ₜ)v(K+1)+β̄ₜ），把单步采样成本从 O(tK²) 降到 **O(K)**（附录给出数学归纳法证明）。
- **反向网络与损失**：训练 Transformer 估计后验 q(xₜ₋₁|xₜ,x₀)，最小化 VLB = L₀+L₁+…+L_{T−1}+L_T（L_T 因 Qₜ 固定为常数可忽略）。**关键 trick：重参数化（reparameterization）**——不直接预测后验，而让网络预测**无噪原始 token 分布 pθ(x̃₀|xₜ,y)**，再据此组合出反向转移 pθ(xₜ₋₁|xₜ,y)=Σ q(xₜ₋₁|xₜ,x̃₀)pθ(x̃₀|xₜ,y)。在此基础上加辅助去噪损失 **L_{x₀}=−log pθ(x₀|xₜ,y)**，与 VLB 联合（loss 权重 **λ=0.0005**）显著提升画质。训练时**不用 teacher-forcing**——刻意同时注入掩码 token 与随机 token，让网络学会预测掩码并修正错误 token。
- **超参**：默认 **T=100** 个 timestep；转移矩阵 γ̄ₜ、β̄ₜ 在 [0,1] 区间线性从 0 增到 **0.9 / 0.1**（即最终掩码率 γ_T≈0.9 为最优，见消融）；优化器 **AdamW**（β₁=0.9, β₂=0.96），warmup 5000 步后学习率 **0.00045**。
- **快速推理（重参数化的红利）**：推理时按时间步幅 Δt 跳步采样（xT, xT−Δt, …, x₀），借助重参数化对画质损害很小；这正是相对 AR 提速 15 倍的来源。
- **采样 trick**：① **truncation sampling**（推理时只保留 pθ(x̃₀) 的 top-r token，避免从低概率 token 采样，CUB-200 上 r=0.86 最优）；② Improved 版（同 repo 的后续工作，见下）还引入 learnable classifier-free guidance、purity prior 采样等。

## Infra（训练 / 推理工程）
- **训练算力规模未披露**：论文与 README 均**未报告** GPU 型号/数量、GPU·时、并行策略、混合精度或训练吞吐——这是本工作的明确信息缺口。仅知扩散解码器为 34M / 370M 规模，VQ-VAE 与 CLIP 文本编码器冻结，故可训练参数集中在解码器。
- **推理工程**：吞吐评测在**单张 V100、batch size=32** 上完成（见 Table 3）。VQ-Diffusion-B 在 100/50/25 推理步分别为 **0.13 / 0.24 / 0.47 imgs/s**；对应同结构自回归 VQ-AR-B 仅 **0.03 imgs/s**——故"快 15 倍"指 fast-inference VQ-Diffusion（25 步，0.47 imgs/s）对 VQ-AR-B（0.03 imgs/s）。推理时间**与图像分辨率解耦**（每步预测全图所有 token 的分布，独立于分辨率），这是相对 AR（时间随分辨率线性增长）的结构性优势。
- **部署形态**：官方开源 PyTorch 实现（microsoft/VQ-Diffusion），并已集成进 🤗 Diffusers 的 `VQDiffusionPipeline`，HF 上提供 ITHQ checkpoint（`microsoft/vq-diffusion-ithq`，支持 fp16）。

## 评测 benchmark（把效果讲清楚）
**文生图 FID（30k 生成 vs 30k 真实，Table 1）：**

| 方法 | MSCOCO | CUB-200 | Oxford-102 |
|---|---|---|---|
| AttnGAN | 35.49 | 23.98 | — |
| DM-GAN | 32.64 | 16.09 | — |
| DF-GAN | 21.42 | 14.81 | — |
| DAE-GAN | 28.12 | 15.19 | — |
| DALL-E（~10× 参数） | 27.50 | 56.10 | — |
| CogView（~10× 参数） | 27.10 | — | — |
| **VQ-Diffusion-S（34M）** | 30.17 | 12.97 | 14.95 |
| **VQ-Diffusion-B（370M）** | 19.75 | 11.94 | 14.88 |
| **VQ-Diffusion-F** | **13.86** | **10.32** | **14.10** |

要点：① VQ-Diffusion-S 以 GAN 量级参数即在 CUB/Oxford 上达 SOTA 级；② VQ-Diffusion-F 在 MSCOCO 上 **13.86**，大幅超过参数量约 10 倍的 DALL-E（27.50）和 CogView（27.10）。

**VQ-Diffusion vs 同结构自回归 VQ-AR（CUB-200，V100/bs=32，Table 3）：**
- **Base 档**：VQ-AR-B FID **17.76** @ **0.03 imgs/s**；VQ-Diffusion-B 100 步 FID **11.94** @0.13、50 步 12.45 @0.24、25 步 14.03 @0.47 imgs/s。即 25 步 fast-inference 的 VQ-Diffusion-B 同时 FID 更好（14.03<17.76）且 throughput ≈15.7× VQ-AR-B（0.47/0.03）。
- **Small 档**：VQ-AR-S FID **18.12** @0.08；VQ-Diffusion-S 25 步 15.46 @1.25、50 步 13.62 @0.67、100 步 12.97 @0.37 imgs/s。同样 FID 全面优于 VQ-AR-S 且更快。
- 结论：在 -S 与 -B 两档上 VQ-Diffusion 均**大幅优于同结构 AR 的 FID**，配合跳步快速推理可比 VQ-AR **约 15× 提速**（论文摘要口径）。

**类条件 ImageNet / 无条件 FFHQ FID（50k 生成 vs 全部真实，Table 4）：**
- ImageNet：VQ-Diffusion **11.89**（不加 trick），加 acceptance-rate 0.05 后 **5.32**；对比 ADM-G(1.0 guid) 4.59、VQGAN(acc0.05) 5.88、ImageBART(acc0.05) 7.44、BigGAN-deep 6.84。
- FFHQ（无条件）：VQ-Diffusion **6.33**；对比 StyleGAN2 3.8、ImageBART 9.57、VQGAN 9.6。
- 结论：作为**统一框架**（同一方法跨文生图/类条件/无条件），表现在各任务都强；个别专用 GAN 的 FID 更低，但 VQ-Diffusion 的通用性是卖点。

**关键消融：**
- **训练/推理步数（Table 2，CUB-200）**：训练步从 10→100 持续变好，→200 饱和（故默认 T=100）；推理可砍掉 3/4 步（100 训练步模型用 25 步推理 FID 14.03 vs 100 步 11.94）仍保持良好画质，约省 3/4 推理时间。
- **mask-and-replace 最终掩码率 γ_T**：γ_T=1（纯 mask）与 γ_T=0（纯 replace）都是特例，**M=0.9 最优**；>0.9 误差累积加剧，<0.9 网络难以定位需关注区域。
- **truncation rate**：CUB-200 上 **r=0.86 最优**，对离散扩散采样质量"极其重要"。

## 创新点与影响
**核心贡献：**
1. **首个把离散扩散用于（条件）文生图**：在 VQ-VAE 离散隐空间上做 DDPM 的离散变体，跳出"连续像素扩散"与"自回归 token"两条已有路线。
2. **mask-and-replace 前向策略**：把 absorbing（mask）与 uniform（replace）两类离散噪声结合，理论上证明二者缺一不可，工程上加速收敛、让网络区分被破坏位置并强制理解全局上下文——这是本文最被引用的设计。
3. **重参数化（预测 x̃₀）+ 跳步快速推理**：使非自回归扩散在画质与速度间取得远优于 AR 的折中（约 15× 提速、推理时间与分辨率解耦）。
4. **统一/通用框架**：同一方法覆盖文生图、类条件、无条件三类任务，并天然支持 mask-inpainting（把待修补区域置 [MASK] 即可，无需重训）。

**影响**：VQ-Diffusion 与同期 MaskGIT 一起确立了"离散 token 上的掩码/非自回归并行生成"范式，是后来 Paella、MUSE、以及更广义"masked generative transformer"系谱的重要先声；并把"扩散"概念从连续高斯推广到离散类别，与 D3PM 一道成为离散扩散在视觉中的代表作。官方 repo 后续推出 **Improved VQ-Diffusion**（arXiv 2205.16007，CVPR 2022 同 repo）补充了 **learnable classifier-free guidance、高/低速可调推理、purity prior 采样**等，进一步把 MSCOCO 与 ImageNet 指标推高（细节见该后续论文，本页未展开）。

**已知局限**：① 训练算力/工程细节完全未披露（无法评估复现成本）；② 图像质量受限于所用 VQGAN tokenizer（256×256、32×32 token 的重建上限）；③ 与同期连续隐空间扩散 [[latent-diffusion-ldm]]（2021-12，几乎同时）相比，离散 token 路线在通用大规模文生图上的画质天花板后被 LDM/Stable Diffusion 的连续 latent diffusion 路线超越，离散扩散更多在"掩码并行生成"方向延续影响。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2111.14822
- arxiv_pdf: https://arxiv.org/pdf/2111.14822
- github: https://github.com/microsoft/VQ-Diffusion
- hf_model_card: https://huggingface.co/microsoft/vq-diffusion-ithq
- 后续工作（Improved VQ-Diffusion，README 指向）: https://arxiv.org/abs/2205.16007

## 本地落盘文件
- ../../../sources/omni/2021/arxiv-2111.14822.pdf
- ../../../sources/omni/2021/vq-diffusion--readme.md
- ../../../sources/omni/2021/vq-diffusion--hf-modelcard.md
