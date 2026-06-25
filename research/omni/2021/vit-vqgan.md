---
title: "Vector-quantized Image Modeling with Improved VQGAN (ViT-VQGAN)"
org: "Google Research"
country: US
date: "2021-10"
type: paper
category: method
tags: [tokenizer, vqgan, vit, vector-quantization, autoregressive, codebook, image-generation, representation-learning]
url: "https://arxiv.org/abs/2110.04627"
arxiv: "https://arxiv.org/abs/2110.04627"
pdf_url: "https://arxiv.org/pdf/2110.04627"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2110.04627.pdf, arxiv-2110.04627.txt]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ViT-VQGAN 把 [[vqgan]] 的 CNN 编码器/解码器整体换成 Vision Transformer，并引入「factorized codes + ℓ2-归一化码本」两项码本学习改进，将离散图像 tokenizer 的重建保真度、码本利用率与吞吐同时大幅提升；在此 tokenizer 上做两阶段自回归图像建模（VIM），ImageNet 256×256 类条件生成达到 **IS 175.1 / FID 4.17**（vanilla VQGAN 为 70.6 / 17.04），是 [[parti]]、[[muse]] 等自回归与掩码 T2I 模型 tokenizer 的直接技术源头。

## 背景与定位
- **两阶段离散建模范式**：[[vqvae]] → [[dall-e-1]] → [[vqgan]] 这条线把图像生成拆成「stage-1 把图像量化成离散 token + stage-2 用自回归/Transformer 建模 token 分布」。stage-2 模型的天花板被 stage-1 tokenizer 的重建质量和码本表达力卡死——重建越糊、码本越少被用到，下游生成与表征就越差。
- **vanilla VQGAN 的痛点**：① 编码器/解码器是 CNN（+少量 non-local attention），受卷积归纳偏置约束、在 TPU 上吞吐不高；② 码本「死码」严重，VQGAN 默认只能用 size=1024 的小码本并依赖 top-k/top-p 采样启发式才能出好结果，码本利用率低导致重建损失大、stage-2 多样性差。
- **本文目标**：受 NLP「next-token 预训练带来强 zero/few-shot 与表征」启发，提出 Vector-quantized Image Modeling (VIM)，把图像也当成离散 token 序列做 GPT 式自回归预训练。要让这条路走通，关键瓶颈是 tokenizer——于是从架构到码本系统性改进 VQGAN，得到 ViT-VQGAN。相比同期纯像素自回归的 [[igpt]]（最大只能 64×64、序列极长），ViT-VQGAN 先量化再建模，序列短、可上 256×256，用更小模型、更少数据拿到更强结果。

## 模型架构
ViT-VQGAN 是「ViT 编码器 + 向量量化 + ViT 解码器」的自编码器（stage-1），配一个独立的自回归 Transformer（stage-2，称 VIM）。

**Stage-1 ViT-VQGAN（tokenizer）**
- **Patch 化**：把 256×256 图像切成 **8×8 不重叠 patch**，线性映射成 image token，经 ViT Transformer block 编码为 **32×32 = 1024** 个 latent；解码器做逆操作，把每个 token 映回 8×8 patch 再拼回 256×256。token block 输出后接一个带 tanh 中间层的两层 FFN；编/解码器输出端不加激活（除 logit-laplace 均值预测用 sigmoid）。这个简单设计就能得到无明显网格伪影的高质量重建。
- **码本**：size = **8192**（远大于 VQGAN 默认的 1024），生成时直接用 temperature=1.0 简单采样，**不用 top-k/top-p**。
- **码本学习两大改进（核心创新）**：
  - **Factorized codes（因式分解码）**：在编码器输出后加一个线性投影，把高维特征（如 768-d）降到**低维查找空间**（如 32-d 或 8-d）再做最近邻码本查找，匹配到的低维码再投影回高维 embedding。等于把「码查找」与「码嵌入」解耦。把查找维度从 256-d 降到 32-d 持续提升重建质量；消融里把 latent 维降到 16/8 时码本利用率冲到 95–96%、FID 最好到 1.50。
  - **ℓ2-normalized codes**：对编码 latent 与码本向量都做 ℓ2 归一化，把所有 latent 映到单位球面，于是欧氏距离最近邻等价于**余弦相似度**最近邻，显著提升训练稳定性与重建质量。消融显示去掉 ℓ2 归一化后 FID 从 1.55 恶化到 5.44、码本利用率从 96% 崩到 2%。
- **判别器**：用 **StyleGAN 判别器**（而非 VQGAN 用的 PatchGAN），更稳定、重建质量更好（消融：PatchGAN FID 3.88 vs StyleGAN 1.55）。
- **三种规模**（encoder–decoder 对称/非对称）：Small (32M)、Base (91M)、Large (599M)，分别 8/12/32 个 block。默认主结果用 **ViT-VQGAN-SS**（小编码器+小解码器）——动机是 stage-2 训练只需 tokenizer 编码器前向，把算力留给 stage-2，stage-1 保持轻量高吞吐；也试过非对称 **SL**（小编码器+大解码器）。

**Stage-2 VIM（自回归 Transformer）**
- decoder-only Transformer，对 raster 顺序展平的 1024 个 token 做因果注意力 next-token 预测，目标是最小化负对数似然。token id 经可学习 embedding + **可学习 2D 位置编码**，最后一层加额外 LayerNorm，残差/激活/注意力输出都用 0.1 dropout。
- 两种规模：**VIM-Base (650M, 24 block, dim 1536)**、**VIM-Large (1697M, 36 block, dim 2048)**。主结果用 VIM-Large。
- **类条件生成**：在 image token 前**前置一个 class-id token**（class 与 image 用各自独立的 embedding 层），采样时先给定 class-id 再自回归解码其余 token。

## 数据
- **纯图像、无文本**：stage-1 与 stage-2 全部在图像-only 数据上端到端训练，不需要标注（类条件生成才用 class id）。
- **三个标准数据集**：**ImageNet**（1.28M 训练图）、**CelebA-HQ**、**FFHQ**，分别独立训练，沿用 VQGAN（taming-transformers）的默认 train/val 划分。
- 输入分辨率统一 **256×256**。论文未使用额外 web 规模图像数据（对比中 DALL-E dVAE、iGPT-XL 都用了 extra web data，ViT-VQGAN 在不用额外数据的前提下仍更强）。
- **stage-2 输入侧增广**：先对图像做随机增广，再过 tokenizer 编码器得到输入 token——这也是作者强调 tokenizer 编码器要高吞吐的原因（每步都要前向）。
- 数据清洗/配比/re-captioning：本工作是纯视觉 tokenizer + 类条件生成，**无 caption、无合成数据、无美学/安全过滤流程**（与后续 T2I 工作不同）。

## 训练方法
**Stage-1 ViT-VQGAN 训练目标（复合损失）**
最终默认组合：
`L = L_VQ + 0.1·L_Adv + 0.1·L_Perceptual + 0.1·L_Logit-laplace + 1.0·L_2`
- **L_VQ**：标准 VQ 损失 `‖sg[z_e(x)]−e‖² + β·‖z_e(x)−sg[e]‖²`，commitment 系数 **β=0.25**，码本用直通估计（straight-through）+ argmin 欧氏（归一化后即余弦）查找。
- **Logit-Laplace loss**：可视作归一化 ℓ1，假设像素噪声服从 Laplace 分布；作者发现它主要贡献**码本利用率**。
- **ℓ2 loss + 感知损失（VGG-based）**：主要贡献 **FID**。
- **GAN loss**：StyleGAN 判别器对抗损失。
- 损失权重经一次超参 sweep 调定后，对 CelebA-HQ/FFHQ/ImageNet **全部沿用同一套**。
- **表征评测的公平性处理**：感知损失基于在 ImageNet 上有监督训练的 VGG，可能把监督信号泄漏进 stage-2 的 linear-probe；因此**所有无监督/表征结果都用「不含感知损失」训练的 tokenizer**，而生成结果则用「含感知损失」的（保真更高）。
- **优化**：batch=256，分布在 **128 块 CloudTPUv4** 上训 **500k 步**；Adam（β1=0.9, β2=0.99），lr 50k 步线性 warmup 到峰值 **1e-4**，随后余弦衰减到 5e-5；decoupled weight decay 1e-4；分辨率 256×256。

**Stage-2 VIM 训练**
- 训练目标：纯 **next-token 自回归**（最小化 token 序列负对数似然），无 diffusion / 无 masked-token。
- batch=1024，训 **450k 步**；Adam（β1=0.9, β2=0.96），lr 5k 步线性 warmup 到峰值 **4.5e-4**，从 80k 步起指数衰减到 1e-5。
- 为省显存用 **Adafactor**（一阶矩量化成 Int8 + 二阶矩因式分解）。论文明确**没有用混合精度、模型分片或梯度压缩**等额外技巧。
- **采样/加速**：生成时 token-by-token 采样、不降温；可选 **ResNet-101 分类器拒绝采样**（acceptance rate 0.5/0.25）进一步压 FID。无蒸馏（consistency/LCM/ADD 等本工作不涉及）。

## Infra（训练 / 推理工程）
- **全程 Google CloudTPUv4**。stage-1：128 块 TPUv4 × 500k 步；stage-2：batch 1024 × 450k 步（论文未直接给 stage-2 TPU 数与总 GPU·时/挂钟天数——**未披露**）。
- **吞吐对比**（同 128 CloudTPUv4，imgs/sec）：ViT-VQGAN-Base 960 vs CNN-VQGAN(channels×1) 946、CNN-VQGAN(channels×2) 仅 400；ViT-VQGAN-SS 高达 1520。即 ViT 化在「质量更好」的同时吞吐还更高，并直接加速 stage-2（编码器前向更快）。
- 工程上刻意保持简单：Adafactor + Int8 一阶矩省显存，**未用混合精度/模型分片/梯度压缩**。
- 推理：stage-2 自回归 1024 步逐 token 解码 + tokenizer 解码器还原像素；可叠加分类器拒绝采样换取更低 FID。量化/缓存/部署形态本工作**未涉及**。

## 评测 benchmark（把效果讲清楚）
全部数字来自已落盘的 arXiv PDF 正文与附录表格。

**① Tokenizer 重建 FID（val 重建 vs 原图，越低越好，Table 3）**
- ImageNet：ViT-VQGAN **1.28**（VQGAN 16×16/1024 为 7.94；VQGAN 16×16/16384 为 4.98；DALL-E dVAE 32×32/8192 为 32.00）。
- CelebA-HQ：**4.66**；FFHQ：**3.13**（均 32×32, 码本 8192）。

**② Tokenizer 消融（ImageNet, Table 4）**
- 架构：CNN-VQGAN-Base FID 2.26 / 码本用率 63% / 吞吐 946，ViT-Base FID **1.55** / 用率 **96%** / 吞吐 960；判别器 StyleGAN 1.55 vs PatchGAN 3.88。
- Factorized 查找维：256-d → FID 3.68/用率 4%；64-d → 2.50/37%；**16-d → 1.50/95%**；8-d → 1.52/96%；过小(4-d) 反退化到 3.68。
- 去 ℓ2 归一化：FID 5.44 / 用率 **2%**（崩溃）。
- 规模（encoder–decoder，Table 1/4）：Small-Small FID 1.99（吞吐 1520）、Base-Base 1.55（吞吐 960）、非对称 Small-Large 1.28（吞吐 384，质量最好但解码慢）。

**③ 无条件生成 FID（不用 top-k/top-p，Table 5）**
- CelebA-HQ **7.0**（VQGAN 10.2）、FFHQ **5.3**（VQGAN 9.6；StyleGAN2 3.8 仍更低，但 ViT-VQGAN 已显著超过同范式 VQGAN）。

**④ ImageNet 256×256 类条件生成（Table 6，主结果）**
- 无拒绝采样：ViT-VQGAN+VIM-Large **FID 4.17 / IS 175.1**（vanilla VQGAN 17.04 / 70.6；ADM-G 无引导 10.94 / 101.0；ADM-G 1.0 引导 4.59 / 186.7；BigGAN-deep 6.84 / 203.6）。
- 加分类器拒绝采样（acc 0.5）：**FID 3.04 / IS 227.4**；acc 更激进时报告**最佳 FID 3.04、最佳 IS 321.7**。
- stage-2 规模消融（Table 8，无拒绝采样）：VIM-Base 8.81 / 110.8，VIM-Large 4.17 / 175.1——更大 stage-2 收益明显。

**⑤ 无监督表征 linear-probe（ImageNet top-1, Table 7）**
- **VIM-Large 73.2%**（iGPT-L 60.3%，相近参数；iGPT-XL 用额外 web 数据+更大模型才 72.0%——VIM-L 仍超过它）；VIM-Base 65.1%。
- 取**中间层**特征最优（VIM-L 用第 15/36 block，VIM-B 用第 10/24 block）。
- tokenizer 重要性消融：VIM-Base 换成 CNN-VQGAN tokenizer 掉到 61.8%（-3.3），换 DALL-E dVAE 掉到 63.8%（-1.3）——印证 ViT-VQGAN 改进对下游表征的贡献。

## 创新点与影响
**核心贡献**
1. **架构**：首次把 VQGAN 编/解码器完全 ViT 化，去 CNN 归纳偏置，TPU 上质量与吞吐双赢。
2. **码本学习**：factorized（低维查找空间）+ ℓ2 归一化（球面/余弦最近邻）两项简单改动，把大码本（8192）的利用率从个位数百分比拉到 95–96%、消灭死码，是本文最被后续广泛复用的 trick。
3. **范式验证**：在更好的 tokenizer 上，纯自回归 next-token 图像建模（VIM）同时在「生成（IS/FID）」和「无监督表征（linear-probe）」两条线上达到/超越同期方法，且无需额外数据、模型更小。

**影响**
- ViT-VQGAN 直接成为 Google 后续 T2I 旗舰 **[[parti]]**（自回归）与 **[[muse]]**（掩码生成）的 tokenizer 基础；factorized + ℓ2-normalized codebook 也被大量后续离散 tokenizer 工作（含视频 [[magvit]] 一系）继承。
- 它把「tokenizer 质量是离散生成天花板」这一认知量化、可操作化，推动了「先把 tokenizer 做好再谈 stage-2」的研究路径。

**已知局限**
- stage-2 自回归 1024 步逐 token 解码、推理慢；无任何步数蒸馏/加速。
- 仅在 ImageNet/CelebA-HQ/FFHQ 等标准集、256×256、类条件层面验证，**本文未做文本条件（T2I）**——T2I 留给了 Parti/Muse。
- 无官方开源代码/权重（模型为 Google 内部实现）；复现需自行实现。
- 含 VGG 感知损失会泄漏监督信号到表征评测，需特意分两套 tokenizer 规避——说明感知损失与「纯无监督」之间存在张力。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2110.04627
- arxiv_pdf: https://arxiv.org/pdf/2110.04627
- 备注: 无官方 GitHub / HF / ModelScope 发布；Google Research 该论文无独立官方博客页（pub 页 404）。MaskGIT（CVPR 2022）为同组后续工作、非本文代码。

## 本地落盘文件
- ../../../sources/omni/2021/arxiv-2110.04627.pdf
- ../../../sources/omni/2021/arxiv-2110.04627.txt
