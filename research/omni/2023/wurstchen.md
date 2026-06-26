---
title: "Würstchen: An Efficient Architecture for Large-Scale Text-to-Image Diffusion Models"
org: "Wand Technologies / TH Ingolstadt / Mila / Stability AI(compute)"
country: EU
date: "2023-06"
type: paper
category: t2i
tags: [t2i, latent-diffusion, cascade, compression, vqgan, efficient-training, convnext, stable-cascade]
url: "https://arxiv.org/abs/2306.00637"
arxiv: "https://arxiv.org/abs/2306.00637"
pdf_url: "https://arxiv.org/pdf/2306.00637"
github_url: "https://github.com/dome272/Wuerstchen"
hf_url: "https://huggingface.co/warp-ai/wuerstchen"
modelscope_url: ""
project_url: "https://huggingface.co/blog/wuerstchen"
downloaded: [arxiv-2306.00637.pdf, arxiv-2306.00637.txt, wurstchen--readme.md, wurstchen--hf-blog.md, wurstchen--hf-warp-ai-wuerstchen.md, wurstchen--hf-warp-ai-wuerstchen-prior.md, wurstchen--openreview-iclr2024.json]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Würstchen 是一个三阶段级联文生图扩散模型，核心创新是把文本条件扩散放进 **42:1 超高压缩潜空间**（远超 LDM/SD 常用的 4–8x），从而把 SOTA 级文生图的训练成本从 SD 2.1 的 200,000 A100-GPU-h 砍到 **24,602 GPU-h（约 8x 降本）**、推理快 2x 以上，同时在 PickScore 人类偏好上一致优于同体量的 SD 1.4/2.1。它后来演化为 Stability AI 的 **Stable Cascade**。

## 背景与定位
文生图扩散模型质量已逼近照片级，但算力代价巨大：SD 1.4 用了 150,000 GPU-h，SD 2.1 用了 200,000 GPU-h。降本的主流思路是 [[latent-diffusion-ldm]] 那样在压缩潜空间里训扩散，但单级自编码器的压缩率受限——常规 VQGAN/VAE 在 4x–16x 之间，再高就重建崩坏（>16x 难以忠实重建细节）。

Würstchen 的赌注是：**把压缩做到极致（42x），让文本条件扩散在一个极小的语义潜空间里跑**。它没有用一个自编码器硬压，而是用**两级压缩 + 解耦**：
- Stage A/B（合称 Decoder）负责把图像压到/解回像素；
- Stage C（Prior）才是文本→图像的真正生成器，运行在 42x 压缩的小潜空间。

直觉是：语言潜空间（CLIP/T5 文本嵌入）对生成的指导太"稀"，而一个**高度压缩但语义致密的图像表征**能给扩散过程提供更细的引导，因此可以在远小的空间里达到同等保真度。相对前置工作：比 [[latent-diffusion-ldm]]/SD 压缩更狠（42x vs 8x）；比 Imagen/unCLIP 的 upsampler 级联思路（64→256→1024 像素级超分）更省，因为生成核心在 latent 而非像素。

## 模型架构
三阶段全部是深度网络，**推理顺序 C→B→A，训练顺序 A→B→C**（反向）。

**Stage A — f4 VQGAN（18M 参数）**
- 把 `3×1024×1024` 图像编码成 `256×256` 离散 token，码本大小 8,192，压缩率 4:1。
- Encoder/Decoder 各 2 个 stage，用 4×4 stride-2 下/上采样；encoder 起、decoder 末各有一个 scale=2 的 pixel-shuffle。每个 stage 是 ConvNeXt block（384 输入通道 / 1536 嵌入通道）；encoder 末用 1×1 conv + BatchNorm 把通道压到编码维度 4。decoder 第一 stage 用 16 个 block。
- 训练完成后**丢弃量化**，Stage B 在 Stage A encoder 的"未量化"连续潜空间上训练。

**Stage B — Diffusion Autoencoder / 条件 LDM（1B 参数）**
- U-Net（编/解码各 4 stage，通道宽 320/640/1280/1280），building block = ConvNeXt block + 时间步 block（线性条件）+ cross-attention（文本与图像嵌入条件）。各 stage cross-attention 头数 -, 10, 20, 20（首 stage 仅时间条件）。encoder/decoder 各 stage block 数 4,4,14,4。
- 任务：在 Stage A 的潜空间里，从噪声重建出 VQGAN latent，**强条件于 Semantic Compressor 给出的高压缩语义嵌入** `Csc` 与文本嵌入。
- **Semantic Compressor**：ImageNet1k 预训练的 **EfficientNetV2-S** 主干，去掉 global-pool/分类头，换 1×1 conv 把通道压到 16。它把 `3×786×786`（由 1024→786 bicubic 缩放）图像编码成 `1280×24×24`，再用 1×1 conv 归一化投影到 **`Csc ∈ R^{16×24×24}`**。这个 16×24×24 即 42:1 总压缩的来源（1024²×3 / (16×24×24) ≈ 42）。训练 Stage B 时该 compressor 权重被一起更新（ImageNet 判别式特征不适合语义投影）。
- 训练技巧：对 Semantic Compressor 嵌入**间歇性加噪**（教模型适应不完美嵌入，因为推理时这些嵌入由 Stage C 生成而非真实图像）；随机 drop `Csc` 以支持 classifier-free guidance。`Csc` flatten 后投影并 concat 到每个 block。

**Stage C — 文本条件 LDM / Prior（1B 参数）**
- **不用 U-Net**：作者认为图像已压缩 42x，再下采样有害，所以 Stage C 是 **16 个 ConvNeXt block 的纯序列（无下采样）**，宽 1280 通道，每个 block 后接时间条件 block + 16 头 cross-attention 文本条件。
- 直接在 finetuned Semantic Compressor 的 `16×24×24` 潜空间里做标准扩散。
- 文本编码器：v1 用 **CLIP-H/14**（unpooled，dim 1024），v2 用 **CLIP ViT-bigG/14**。注意：论文正文用 CLIP-H，HF v2 模型卡用 bigG。
- 噪声目标重参数化：网络输出 `A,B`，预测噪声 `ε̄ = (X_sc,t − A) / (|1−B| + 1e-5)`，使初始化（输出≈0）时模型返回输入、对高噪声样本 loss 小，训练更稳。用 cosine 噪声表 + 连续时间步 + **p2 loss 加权**（高噪声级贡献更大）。

**采样**：Stage C 用 DDPM 跑 τ_C=60 步生成 `16×24×24` latent → flatten 成 `576×16` 作为 Stage B 条件 → Stage B 在 `4×256×256` 未量化 VQGAN 空间跑 τ_B=12 步（w=4 CFG）→ Stage A VQGAN decoder 解回像素。支持可变长宽比，单边可达 ~1538px。附录 D 证明 **Stage C 决定图像内容、Stage B 只做细化/去模糊/提分辨率**，且 Stage B 的文本条件几乎无增益（未来可去掉）。

## 数据
- 全部三个 stage 都训练在 **improved-aesthetic LAION-5B** 的去重子集上（[[laion]] 美学评分过滤后的子集）。
- 仅使用**去重的公开数据**（reproducibility statement）；人类偏好研究用的生成图被人工筛查过有害/暴露内容。
- Stage A：128×128 crop（原图 resize 到 256×256）。Stage B/C：见训练方法。
- Stage C 最后一轮额外用"美学艺术作品"过滤子集（aesthetical artworks）训练，以提升美学质量。
- **训练样本总量**：Würstchen 处理 **1.42B 样本**（Table 2），远少于 SD 1.4 的 4.8B、SD 2.1 的 3.9B（†来自官方模型卡估算；该列按 Table 2 原始数值，注意 SD 1.4 反而比 SD 2.1 多）。
- 具体配比/清洗细节、LAION 子集规模数字：未进一步披露。

## 训练方法
**目标**：标准 DDPM 扩散（MSE 噪声预测 + p2 加权），不是 flow matching。

**多阶段（训练顺序 A→B→C，各自独立训）**：
- **Stage A（VQGAN）**：500,000 iter，AdamW lr=1e-4，batch 256，128×128 crop。三损失 MSE+对抗+感知，前 10k iter 权重 (1.0, 0.0, 0.1)，10k 步后开启对抗损失（权重 0.01）。随机 drop 量化（10%）以预备后续去量化。
- **Stage B**：AdamW lr=1e-4，10k 步 linear warm-up。先 **457,000 iter @ 512×512（batch 512）**，再 **300,000 iter @ 1024×1024（batch 128）**；Semantic Compressor 对应吃 384×384 / 768×768 输入。CLIP 文本 dim 1024。
- **Stage C**：AdamW lr=1e-4，**连续训练 4 轮**：
  1. 500,000 iter，12×12 latent（compressor 吃 384×384），batch **1536**；
  2. +364,000 iter，24×24 latent（768×768），batch 1536；
  3. +4,000 iter，长宽比自适应（在 768×1280 / 1280×768 / 768×768 间随机），batch 768；
  4. +50,000 iter 美学微调，24×24 latent（768×768），batch 384。
  **最终模型 = 第 3 轮权重与第 4 轮权重的 50:50 插值**（混合写实与艺术风格），同时也开源插值前的两个端点模型。
- 文本条件随机 drop（Stage C 5%、Baseline LDM 在 CLIP-H text 上 5%）以支持 CFG。
- **未使用** RLHF/DPO/奖励模型，也**未做步数蒸馏/LCM/ADD**——加速完全来自 42x 压缩的小潜空间，而非蒸馏。

## Infra（训练 / 推理工程）
- **训练算力（Stage C，最贵的从零训练部分）**：**24,602 A100-GPU-h**（v2）；vs SD 2.1 200,000 GPU-h ≈ **8x 降本**。即便加上 Stage B 的 ~11,000 GPU-h / 318M 样本，整体仍显著更省。
- **HF 官方博客补充**：Würstchen **v1（512×512）只用 9,000 GPU-h**（vs SD 1.4 150,000，**16x 降本**）；v2（最高 1536）24,602 GPU-h，相比只在 512 训的 SD 1.4 仍便宜 6x。
- 硬件：A100 PCIe 40GB，AWS US-east（HF 模型卡）。
- **碳排**：v2 训练估算 **2,275.68 kg CO2 eq**（Lacoste 2019 计算器），vs SD 1.4 ~11,250、SD 2.1 ~15,000（官方卡估算）。
- **推理**：1024×1024 单图比 SD 2.1/SDXL 快 2x+；`torch.compile` 后进一步提速（论文 Fig.4 给出有/无优化两组曲线）。Stage B τ_B=12 步、Stage C τ_C=60 步。
- **工程集成**：已全量集成进 🧨 diffusers，自动支持 PyTorch 2 SDPA flash-attention、xFormers、model offload / sequential CPU offload、prompt weighting、Apple MPS。低显存友好（"没有 A100 也能跑"）。
- 并行/分布式/混合精度细节：未在论文披露。

## 评测 benchmark（把效果讲清楚）
**主指标 = PickScore**（模拟人类偏好，二选一胜率；表中数字为 Würstchen 被偏好的百分比）：

| 对手 | COCO-30K | Localized-Narratives-5K | Parti-prompts |
|---|---|---|---|
| DF-GAN | 99.8% | 98.0% | 99.6% |
| GALIP | 98.1% | 95.5% | 97.9% |
| **SD 1.4 (150k GPU-h)** | **78.1%** | **79.9%** | **82.1%** |
| **SD 2.1 (200k GPU-h)** | **64.4%** | **70.0%** | **74.6%** |
| SD XL | 39.4% | 39.1% | 39.0% |
| Baseline LDM (ours, 25k GPU-h) | 96.5–98.6% | — | — |

结论：**一致优于同体量但算力 8x 的 SD 1.4/2.1**；输给更大的 SD XL（2.6B，数据/算力未知，作者认为不公平故后续实验剔除）；把自家 25k GPU-h 的 U-Net Baseline LDM 碾压（证明是架构而非纯算力带来的效率）。

**FID / IS @ COCO-30K（256² FID，299² IS；Table 2）**：
- Würstchen：FID **23.6**，IS **40.9**（IS 为表中最高，超过所有对比模型）。
- 对比：SD 1.4 FID 16.2 / IS 40.6，SD 2.1 FID **15.1** / IS 40.1，SD XL FID >18，LDM 12.63，CogView2 24.0，Baseline LDM 43.5。
- **FID 偏高**作者归因于生成图偏"平滑"（缺高频细节），在 COCO 这种真实照片分布上 FID 惩罚更重；附录 B 还实证 FID 对 JPEG 压缩/重采样极敏感（70% JPEG 就能凭空造出 ~10 的 FID），说明该指标本身不可靠，故以 PickScore + 人评为主。

**人类偏好研究（仅对比 SD 2.1，最近的同级竞品）**：90 名参与者，Parti-prompts 3343 次 + COCO 2262 次比较。
- Parti-prompts：Würstchen **明显被偏好**（论文 intended use case）；
- MS-COCO：总体不分胜负（vague prompt 导致更主观），但取比较次数 ≥50 百分位的活跃用户后，COCO 上 Würstchen 也略占优、Parti 上强占优。
- 个人偏好维度：Parti 上 72.22% 用户更偏好 Würstchen。

**消融/分析**：附录 D 用一个 3.9M 的小 decoder 直接从 Stage C latent 重建，证明 Stage C 已决定内容，Stage B 仅补细节。

未做 GenEval / T2I-CompBench / DPG-Bench / HPSv2 / ImageReward 等后来的标准 benchmark（2023-06 时尚未流行）——**这些维度未报告**。

## 创新点与影响
**核心贡献**：
1. 首个把文本条件扩散放进 **42:1 超高压缩潜空间**的级联架构（两级压缩 Decoder + 在小空间训 Prior），突破"压缩>16x 重建崩坏"的常识。
2. 证明**架构设计本身**能带来 8x（甚至 v1 的 16x）训练降本，而非靠堆算力或蒸馏，且质量在人评/PickScore 上不输甚至超过算力多 8x 的 SD 1.4/2.1。
3. Stage C 弃 U-Net 改用纯 ConvNeXt 序列；A/B 解耦使 Prior 极易适配新分辨率（"finetune 到 2048² 很便宜"）。
4. 全开源（代码 + 全套权重，含插值前两端点），ICLR 2024 oral。

**影响**：
- 直接演化为 **Stability AI 的 [[stable-cascade]]**（2024-02，把 Würstchen v3 产品化），是 Stability 在 SD3 之前的高效路线代表作。
- 提出的"解耦高分辨率投影与文本条件生成 + 极致潜空间压缩"思路，推动了对**计算可及性（computational accessibility）**作为一等目标的关注，呼应了同期对扩散效率的研究浪潮（[[sdxl-turbo-add]]、[[latent-consistency-models]] 走蒸馏路线，Würstchen 走压缩路线）。

**已知局限**：
- 重建有损，Stage B 对**人脸、手部**等细节常缺失/失真（模型卡明确承认）。
- 生成图偏平滑、缺高频，导致 FID 偏高（真实照片域更明显）。
- 美学/写实需靠权重插值平衡，非端到端最优。
- 仅 PickScore + 小规模人评，缺组合性/对齐类 benchmark；文本编码器仍是 CLIP（非 T5/LLM），长 prompt 精确度受限。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2306.00637
- arxiv_pdf: https://arxiv.org/pdf/2306.00637
- github: https://github.com/dome272/Wuerstchen
- hf_blog(官方): https://huggingface.co/blog/wuerstchen
- hf_model_card(decoder): https://huggingface.co/warp-ai/wuerstchen
- hf_model_card(prior): https://huggingface.co/warp-ai/wuerstchen-prior
- openreview(ICLR2024 oral): https://openreview.net/forum?id=gU58d5QeGv

## 一手源存档（sources/）
- [arxiv-2306.00637.pdf](https://arxiv.org/pdf/2306.00637)  （arXiv 原文 PDF，不入 git）
- [arxiv-2306.00637.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/arxiv-2306.00637.txt)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/wurstchen--readme.md)
- [hf-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/wurstchen--hf-blog.md)
- [hf-warp-ai-wuerstchen.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/wurstchen--hf-warp-ai-wuerstchen.md)
- [hf-warp-ai-wuerstchen-prior.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/wurstchen--hf-warp-ai-wuerstchen-prior.md)
- ../../../sources/omni/2023/wurstchen--openreview-iclr2024.json (ICLR 2024 decision: Accept (oral))
