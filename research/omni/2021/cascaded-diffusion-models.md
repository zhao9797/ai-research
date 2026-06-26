---
title: "Cascaded Diffusion Models for High Fidelity Image Generation (CDM)"
org: "Google Research / Brain"
country: US
date: "2021-05"
type: paper
category: method
tags: [diffusion, cascade, super-resolution, conditioning-augmentation, imagenet, class-conditional, fid]
url: "https://arxiv.org/abs/2106.15282"
arxiv: "https://arxiv.org/abs/2106.15282"
pdf_url: "https://arxiv.org/pdf/2106.15282"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://cascaded-diffusion.github.io/"
downloaded: [arxiv-2106.15282.pdf, cascaded-diffusion-models--project-page.html]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CDM 把"一个低分辨率基础扩散模型 + 多级超分扩散模型"串成级联流水线，并提出 **conditioning augmentation（条件增强）** 这一核心 trick 来对抗级联中的"误差累积/train-test 失配"，在 class-conditional ImageNet 上取得 **FID 1.48@64×64 / 3.52@128×128 / 4.88@256×256**、CAS top-1 63.02%/top-5 84.06%@256×256，**不借助任何 classifier guidance 就超越 BigGAN-deep 与 VQ-VAE-2**。其"级联超分"范式后来被 [[imagen]]、[[dall-e-2]] 直接沿用。

## 背景与定位
- **要解决的问题**：扩散模型（[[ddpm]]）此前已能在中等规模/强条件数据上生成高质量样本，但在 ImageNet 这种"高熵、多类、高分辨率"的困难数据上，纯扩散模型直接建高分辨率仍吃力。CDM 的目标是**只用原始扩散框架 + 最少的额外技巧**把样本质量推到 SOTA，刻意**不引入额外的图像分类器**来刷指标（与并行工作 [[diffusion-models-beat-gans]] 的 classifier guidance 形成对照）。
- **技术脉络中的位置**：
  - 上承 [[ddpm]]、[[improved-ddpm]]（cosine 噪声调度、learned variance / hybrid loss）与 [[sr3]]（Image Super-Resolution via Iterative Refinement，低分图 channel-concat 条件注入的超分扩散）。
  - 与 [[diffusion-models-beat-gans]]（"Diffusion Models Beat GANs", 2021）是**并行/同期工作**：ADM 走 classifier guidance + 改进架构路线；CDM 走纯级联路线。论文承认 ADM 带 guidance 时 FID/IS 更高，但 CDM 在"无 guidance"赛道上更优，且两者技术正交、可叠加。
  - 下启 [[imagen]]（文本→64×64→256×256→1024×1024 级联）、[[dall-e-2]]（unCLIP，64→256→1024 级联超分），把"级联超分 + 条件增强"做成大规模文生图的标准件。
- **相对前置工作的改进**：级联本身在扩散（[[improved-ddpm]]）和其他生成模型（VQ-VAE-2、Subscale Pixel Networks）里都出现过；CDM 的真正贡献是发现**级联流水线的样本质量"关键地"依赖 conditioning augmentation**——没有它，级联反而比非级联基线更差（64×64 FID 从 2.35 退化到 6.02）。

## 模型架构
- **总体形态**：纯扩散级联流水线，主结果 pipeline 为
  `32×32 base → 32×32→64×64 超分 → 64×64→128×128 或 64×64→256×256 超分`。所有 base 与超分模型**都额外以 class label 为条件**。
- **backbone**：全部是 **U-Net**（DDPM/Improved-DDPM/SR3 风格），无 DiT、无 VAE/latent、无 VQ tokenizer——CDM 是**像素空间**扩散，不是 latent diffusion（[[latent-diffusion-ldm]]）那条线。
- **条件注入方式**：
  - 标量条件（class label、扩散时间步 t、以及条件增强强度 s）：通过 embedding 加到 U-Net 中间层。
  - 低分辨率图像条件：先用 **bilinear/bicubic 上采样**到目标分辨率，再与反向过程输入 xt 做 **channel-wise concatenation**（沿用 SR3 / Improved-DDPM）。
- **逐模型架构超参（来自附录 B）**：
  | 模型 | base channels | channel mult | res blocks/分辨率 | attention res | heads |
  |---|---|---|---|---|---|
  | 32×32 base | 256 | 1,2,3,4 | 6 | 8,16 | 4 |
  | 32×32→64×64 超分 | 256 | 1,2,3,4 | 5 | 8,16 | 4 |
  | 64×64→128×128 超分 | 128 | 1,2,4,8,8 | 3 | 16 | 1 |
  | 64×64→256×256 超分 | 128 | 1,2,4,4,8,8 | 3 | 16 | 1 |
- **容量分配哲学**：级联的关键好处是"**把大部分建模容量放在低分辨率**"（经验上低分辨率最决定样本质量，且训练/采样最省算力）——可见 base/低分超分用 256 base channels + 6/5 个 res block，而高分超分只用 128 base channels + 3 个 res block。各级模型**独立训练**，架构可逐分辨率单独调优。
- **未使用**：无 text encoder（这是 class-conditional 而非 text-to-image 工作，T5/CLIP 等都不涉及）；无 latent/VAE；无 classifier guidance。

## 数据
- **数据集**：class-conditional **ImageNet**（Russakovsky et al. 2015），1000 类。裁剪与缩放方式与 **BigGAN 相同**。
- **规模/配比/清洗/re-caption/合成数据**：论文未单独讨论数据清洗、配比、标注或 re-captioning（这是 ImageNet 标准协议，非数据工程论文）。**未披露**额外数据处理细节。
- **数据增强（与本文方法强相关）**：
  - 训练时对 32×32 base 用 **random left-right flip**（提升 32×32 分数，代价是训练更久：不翻转时最好 FID 1.25@300k 步；加翻转后 FID 1.11，但需 700k 步收敛）。
  - 高分超分（256×256）也用 random flip，带来边际提升。
  - 真正的核心增强是下节的 **conditioning augmentation**（作用于低分条件输入而非目标图）。

## 训练方法
- **训练目标**：标准 DDPM 框架。base 与低分超分用 **learned variance + hybrid loss**（来自 [[improved-ddpm]]，同时用 `L_simple` 学 μ、用 ELBO 学 Σ）；高分超分（128/256）则用 **fixed variance + 连续噪声条件（continuous noise conditioning）**（同 SR3 / WaveGrad，以 ᾱt 为条件，便于训练后调采样器）。
- **扩散步数**：base 与 32→64 超分用 **4000 个扩散时间步**（这是为避开 classifier guidance 而付出的代价——ADM 只用几百步）；128/256 超分训练用 **2000 步**，**推理只用 100 步**（噪声调度训练后调优，无需重训）。
- **核心创新：Conditioning Augmentation（条件增强）**——对每个超分模型，在其**低分条件输入 z 上施加数据增强**，专门用来缓解级联中的 compounding error（误差累积 / exposure bias）。三种形式：
  1. **Gaussian augmentation（加高斯噪声）**：在低分辨率上采样阶段最有效。等价于把 z 用前向过程加噪到某时间步。
  2. **Blurring augmentation（高斯模糊）**：对 128×128、256×256 高分上采样最有效。用 k=(3,3) 的高斯核、σ 从固定区间随机采，**50% 训练样本施加，推理时不施加**；256×256 上最佳 σ∼U(0.4,0.6)。
  3. **Truncated vs Non-truncated conditioning augmentation**：把低分反向过程**截断在时间步 s>0**（truncated），或先采完整 z0 再用前向过程加噪到 z_s（non-truncated）。两者训练方式相同（超分模型额外吃 z_s 与 s 的 time embedding），仅采样时不同。论文实验证明二者**效果近似相等**，且推荐 **non-truncated**（搜索 s 时无需为每个 s 缓存所有 z_s，更省工程）。
- **关键 trick——按 s 摊销（amortize）**：把单个超分模型**在训练时对 uniform 随机的截断时间 s 摊销**（s 作额外 time embedding 输入），从而可在**训练后**做细粒度的 s 超参搜索而**无需重训**模型——这是"post-training hyperparameter search for optimal sample quality"的关键。
- **为何 conditioning augmentation 有效（机理结论）**：样本质量随 s 增大呈**非单调**（先升后降）——适量增强有益，过量则使超分模型退化成无条件模型。而当超分**以 ground-truth 低分图为条件**时，质量随 s **单调下降**。两相对照证明：条件增强恰好在"以生成样本为条件"时才有用，专门用于**抹平低分生成样本相对训练用 ground-truth 的 out-of-distribution 失配**，防止超分模型去放大低分图里错误的、OOD 的细节。
- **训练超参（附录 B，Adam）**：
  - 32×32 base：batch 2048，lr 1e-4，700k 步，dropout 0.1，EMA 0.9999。
  - 32→64 超分：batch 2048，lr 1e-4，400k 步，dropout 0.1，EMA 0.9999。
  - 64→128 超分：batch 1024，lr 1e-4，500k 步，dropout 0，EMA 0.9999。
  - 64→256 超分：batch 1024，lr 1e-4，500k 步，dropout 0，EMA 0.9999。
  - 另一发现：对非级联 64×64 基线加 **dropout** 会拖慢 FID/IS 收敛，但延长训练后能取得更好的最终值；把超分 batch 从 256 增到 1024 带来显著提升。

## Infra（训练 / 推理工程）
- **算力规模**：论文**未披露** GPU 型号、卡数、GPU·时、并行/分布式策略、混合精度或吞吐量（典型 Google Brain 内部 TPU 训练，但未给数字）。
- **推理加速**：
  - 高分超分（128/256）用**连续噪声条件训练**，可在训练后调噪声调度，**推理仅 100 步**；论文图 8 显示 64→256 超分**降到 4 步 FID 才轻微变差**，而从 100 步加到 1000 步**无明显提升**——说明高分超分对步数极不敏感（成本敏感，因采样开销随目标分辨率二次增长）。
  - 但 base 与 32→64 低分模型仍用 4000 步（为不上 guidance 而付出的采样成本）。
- **部署形态**：研究原型，**无开源代码 / 无 HF / 无 ModelScope 模型权重**发布（项目页称"Source code and details to reproduce results will appear there"，但实际未见正式 repo）。

## 评测 benchmark（把效果讲清楚）
评测协议：FID 用 50k 样本算（同 Heusel 2017），另报"FID vs validation"以观察过拟合；IS 用 50k 样本、10 splits；模型选择/early-stopping 用 10k 样本 FID。

**主结果（class-conditional ImageNet，无 classifier guidance 赛道）：**
| 分辨率 | 模型 | FID(vs train) | FID(vs val) | IS |
|---|---|---|---|---|
| 32×32 | CDM | 1.11 | 1.99 | 26.01±0.59 |
| 64×64 | BigGAN-deep | 4.06 | — | — |
| 64×64 | Improved DDPM | 2.92 | — | — |
| 64×64 | ADM(无 guidance) | 2.07 | — | — |
| 64×64 | **CDM** | **1.48** | 2.48 | 67.95±1.97 |
| 128×128 | BigGAN-deep | 5.7 | — | 124.5 |
| 128×128 | ADM(无 guidance) | 5.91 | — | — |
| 128×128 | **CDM** | **3.52** | 3.76 | 128.80±2.51 |
| 256×256 | BigGAN-deep | 6.9 | — | 171.4 |
| 256×256 | VQ-VAE-2 | 31.11 | — | — |
| 256×256 | SR3 | 11.30 | — | — |
| 256×256 | ADM(无 guidance) | 10.94 | — | 100.98 |
| 256×256 | ADM+upsampling | 7.49 | — | 127.49 |
| 256×256 | **CDM** | **4.88** | 4.63 | 158.71±2.26 |

> 注：GAN 在"为 IS 优化 truncation"时 IS 仍更高（如 BigGAN-deep max IS@128 达 253、@256 达 317），但 CDM 在 FID 上全面胜出；并胜过同期不带 guidance 的扩散模型（ADM）。

**Classification Accuracy Score (CAS, Ravuri & Vinyals)：**
| 分辨率 | 模型 | Top-1 | Top-5 |
|---|---|---|---|
| 128×128 | Real | 68.82% | 88.79% |
| 128×128 | BigGAN-deep | 40.64% | 64.44% |
| 128×128 | **CDM** | **59.84%** | **81.79%** |
| 256×256 | Real | 73.09% | 91.47% |
| 256×256 | BigGAN-deep | 42.65% | 65.92% |
| 256×256 | VQ-VAE-2 | 54.83% | 77.59% |
| 256×256 | **CDM** | **63.02%** | **84.06%** |

> CDM 在 CAS 上**大幅领先** BigGAN-deep 与 VQ-VAE-2（更接近真实数据），暗示其样本在下游任务上更有用。逐类对比中，在 256×256 上 CDM 训练出的分类器**在 96 个类上超过真实数据**，而 BigGAN-deep/VQ-VAE-2 分别只有 6/31 类。

**关键消融：**
- **级联 vs 非级联 + 条件增强是否必要（16×16→64×64 小规模）**：非级联 64×64 基线 FID 2.35；级联但 s=0（无条件增强）FID **退化到 6.02**；non-truncated 增强 s=101→3.41、s=1001→**2.13**（反超非级联基线）。证明**条件增强是级联能赢的前提**。
- **大规模 32×32→64×64，truncated vs non-truncated**（amortized s）：两者均把 base FID(vs val) 从无增强的 1.71 降到最佳 ~1.48（truncated 在 s=501/751、non-truncated 在 s=751/1251 取最佳），且对低分**生成样本**为条件时 FID 随 s **非单调**；对 **ground-truth** 为条件时随 s **单调变差**——坐实"条件增强专治生成样本的 OOD 失配"。
- **256×256 超分逐项增益**：baseline(σ∼U(0.4,0.6) blur) FID 6.18 → +class conditioning 5.75 → +large batch(256→1024) 5.00 → +flip LR **4.88**。其中"高分超分仍受益于 class conditioning"是个有趣发现（即便 64×64 低分输入已足够信息量）。
- **推理步数**：64→256 超分 4 步 FID 才轻微下降，100→1000 步无提升。

## 创新点与影响
- **核心贡献**：
  1. 系统化"**纯扩散级联超分流水线**"，证明仅靠级联（不靠 classifier guidance、不靠 latent 压缩）即可在 class-conditional ImageNet 上超越 BigGAN-deep / VQ-VAE-2。
  2. 提出 **conditioning augmentation**（Gaussian noise / Gaussian blur / truncated & non-truncated 两种采样实现），从机理上解决级联流水线的 **compounding error / train-test 失配（exposure bias）**，并给出"按截断时间 s 摊销 + 训练后搜索"的实用工程方案。
- **对后续工作的影响**：
  - "低分 base + 多级超分扩散 + 条件增强（加噪低分图）"成为大规模文生图标配：**[[imagen]]**（64→256→1024，文本条件 + noise conditioning augmentation 直接引用本文）、**[[dall-e-2]] / unCLIP**（64→256→1024 级联超分）都沿用了这套范式与"给低分条件加噪"的做法。
  - 与 [[latent-diffusion-ldm]] 的"潜空间压缩"路线形成两条扩高分辨率的主流思路（级联超分 vs latent）。
- **已知局限**：
  - 像素空间多级模型 + base 4000 步采样，**采样成本高**（论文坦承这是为回避 classifier guidance 付出的代价）。
  - 仅做 **class-conditional ImageNet**，未涉文本条件（文本条件留给后续 Imagen）。
  - **未开源代码/权重**，infra/算力细节未披露。
  - IS 指标上仍不及为 IS 调 truncation 的 GAN；作者也指出 classifier guidance 与级联正交、叠加应能进一步提升（本文未做该实验）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2106.15282
- arxiv_pdf: https://arxiv.org/pdf/2106.15282
- project_page: https://cascaded-diffusion.github.io/
- 期刊版本（JMLR 22(47):1-33, 2022）: 同 arXiv 内容

## 一手源存档（sources/）
- [arxiv-2106.15282.pdf](https://arxiv.org/pdf/2106.15282)  （arXiv 原文 PDF，不入 git）
- [project-page.html](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/cascaded-diffusion-models--project-page.html)
