---
title: "StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets"
org: "University of Tübingen / Max Planck Institute for Intelligent Systems"
country: EU
date: "2022-02"
type: paper
category: t2i
tags: [gan, stylegan, projected-gan, imagenet, progressive-growing, classifier-guidance, image-synthesis]
url: "https://arxiv.org/abs/2202.00273"
arxiv: "https://arxiv.org/abs/2202.00273"
pdf_url: "https://arxiv.org/pdf/2202.00273"
github_url: "https://github.com/autonomousvision/stylegan-xl"
hf_url: "https://huggingface.co/spaces/hysts/StyleGAN-XL"
modelscope_url: ""
project_url: "https://sites.google.com/view/stylegan-xl/"
downloaded: [arxiv-2202.00273.pdf, stylegan-xl--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
StyleGAN-XL 用 Projected-GAN 判别器 + 重新引入的渐进式增长 + 预训练类嵌入 + GAN 版分类器引导，把 StyleGAN3 生成器成功扩到 ImageNet 规模，在 ImageNet 256² 取得 **FID 2.30**（论文 Table 2，发布权重 2.26），并首次在 ImageNet 尺度做到 1024² 合成；它是 GigaGAN 之前最强的纯 GAN 图像合成器，是「GAN vs 扩散」缩放之争里 GAN 一侧的关键数据点。

## 背景与定位
StyleGAN 在 FFHQ 等结构化、单峰数据集上质量与可控性都极强，但在 ImageNet 这类大而无结构的多峰数据上「严重退化」，此前 [Gwern 2020]、[Grigoryev 2022] 等多次尝试把 StyleGAN/StyleGAN2 扩到 ImageNet 均效果不佳，业界因此怀疑 Style-based 生成器的受限设计（mapping network 调制卷积核）本身不适合多样数据。本文的核心论点相反：**限制因素不是架构，而是训练策略**。

定位坐标：
- 当时 ImageNet 上 GAN 的 SOTA 是 BigGAN（靠大 batch/大模型，但训练方差大、无中间隐空间故难做 GAN 编辑），而 BigGAN 已被扩散模型（[[diffusion-models-beat-gans]] / Dhariwal & Nichol 的 guided-diffusion）在 FID 上超过。
- 扩散模型多样性好但推理慢（数百~上千步），且基于 GAN 的编辑方法不直接适用。
- 本文承接作者自己的前作 **Projected GAN**（NeurIPS'21，把真假样本投影到固定预训练特征空间，显著提升训练稳定性/速度/数据效率），并在最新的 **StyleGAN3**（alias-free，[Karras 2021]）生成器上施加这些改造，外加从 ADM 借来的 **classifier guidance**。

相关工作内链：[[stylegan3]] [[projected-gan]] [[biggan]] [[diffusion-models-beat-gans]] [[ddpm]]。

## 模型架构
backbone 是 **StyleGAN3-T**（平移等变配置；初实验发现旋转等变的 StyleGAN3-R 在复杂数据上生成「万花筒」式过度对称图案，故弃用）。生成器由 mapping network Gm（z+类嵌入 → 风格码 w）与 synthesis network Gs（从 Fourier features 起，经卷积/非线性/上采样，每个非线性被上/下采样包裹以抗混叠）组成。关键架构设计：

- **低维隐空间 z**：把 StyleGAN 原本 R⁵¹² 的 z 降到 **R⁶⁴**（自然图像内在维度低，ImageNet 估计 ~40，512 维高度冗余拖慢 mapping network 收敛、吃不到 Projected-GAN 的加速）；同时**保留 w∈R⁵¹²** 不限制 mapping network 容量。这是从 Config-A→B 的关键改动。
- **预训练类嵌入**：取 EfficientNet-lite0 最低分辨率特征做空间池化，按 ImageNet 每类求均值得到类嵌入，再经线性投影对齐 z 维度；Gm 与判别器都用此嵌入条件化，训练中嵌入+投影可学。解决了直接 one-hot 嵌入在 Projected-GAN 下「类嵌入坍塌」（recall 仅 0.004）的问题，引入后 recall 升到 0.15。
- **判别器（Projected GAN）**：真假图先过冻结的预训练特征网络 F，再经 **CCM（跨通道 1×1 随机卷积混合）+ CSM（跨尺度残差随机 3×3 + 双线性上采样）** 得到 4 尺度特征金字塔；**多个独立判别器**各自带谱归一化、无梯度惩罚；F 前加可微数据增强。本文创新：**联合用两个 F——EfficientNet-lite0（CNN）+ DeiT（ViT）**（论文 Table 1 标 DeiT-M，正文 §3.3 称 DeiT-base，原文此处表述不一致），因 CNN 与 ViT 学到互补表示，对 Projected-GAN 有协同效应（见消融）；高分辨率下 CNN 收原图、ViT 收下采样图以省显存但保留全局反馈，最终用 **8 个独立判别器**。
- **分类器引导分支 CLF**：生成图过预训练 DeiT-small，加交叉熵项到生成器损失（详见训练方法）。
- **规模/分辨率策略**：渐进式增长，16²→1024² 共 7 个阶段；**1024² 时生成器达 39 层**（16² 起 11 层，每升一档砍掉末 2 层、新增 7 层，最后 1024² 只加 5 层）。整体「比标准 StyleGAN3 在深度与参数量上大三倍」（论文未给出具体百万级参数数字 → 此项未披露绝对值）。

## 数据
- **训练数据集**：ImageNet（类条件，主战场）；另在 FFHQ、Pokémon、CIFAR-10 上验证。**不使用 x-flip 数据增广**（遵循 StyleGAN2-ADA 的做法），判别器侧用可微数据增强。
- **高分辨率预处理**：ImageNet 平均分辨率仅 469×387，缺高清数据。为做 ≥512²/1024² 训练，作者**用 SwinIR-Large（真实图像超分模型）把整个 ImageNet 上采样**（类比 CelebA-HQ 的制作流程）。作者强调这不是「跑 256² 生成再过 SwinIR」那种 trick——SwinIR 比其上采样栈慢 60×，且会破坏平移等变性；SwinIR 仅用于准备高清训练数据。
- 配比/清洗/re-caption/美学安全过滤：本工作是类条件图像 GAN，无文本-图像对、无 caption 流程，**不涉及 re-captioning / 美学/安全过滤**（未披露，亦不适用）。

## 训练方法
- **训练目标**：标准对抗损失，但在 **Projected-GAN 框架**下——真假样本投影到固定预训练特征空间后再判别（公式见论文式(1)，多个 D 在不同尺度特征上独立对抗）。非扩散、非 flow-matching、非 next-token。
- **重新引入渐进式增长（Config-D）**：先在极低分辨率（16²）训「stem」，FID 饱和后再逐级加「超分阶段」。每升分辨率砍掉前一阶段的临界采样末 2 层（否则做中间层会引入混叠）、新增层并按 StyleGAN3 的 flexible layer specification 设滤波器参数。**只训新加的层，旧层冻结**防模式坍塌；**Gm 只在初始 16² 阶段训练，之后冻结**。判别器侧**不加层**。各阶段训到 FID 不再降为止（非固定 schedule）。batch：16²/32² 用大 batch 2048（仿 BigGAN），64²~256² 用 256，512²~1024² 用 128。
- **分类器引导（GAN 版，Config-F）**：生成图过预训练 DeiT-small，加交叉熵 L_CE 到生成器损失并乘常数 λ=8。与 ADM 不同——ADM 在**采样阶段**对低分辨率模型加梯度引导，本文是在**训练阶段**对高分辨率模型（>32²，否则会模式坍塌）加引导。带来 IS 大幅提升。
- **正则化策略**：尽量少正则（多峰数据上正则反而有害）。关闭 style mixing（StyleGAN3 已不需要）；path-length 正则只在模型训练充分后（200k 图之后）才开启以兼顾可逆性、避免发散；判别器只用谱归一化无梯度惩罚；前 200k 图对所有图做 σ=2 高斯模糊（discriminator blurring，防判别器早期只盯高频）。
- **渐进改造的消融轨迹（ImageNet 128²，每配置训 15 V100-天，见 Table 1）**：A StyleGAN3 baseline → B +Projected GAN & 小 z → C +预训练嵌入 → D +渐进增长 → E +ViT&CNN 双 F → F +分类器引导（即 StyleGAN-XL）。
- **蒸馏/加速**：本身无步数蒸馏（GAN 单步生成）；论文把「GAN 蒸馏减小模型」列为未来工作。

## Infra（训练 / 推理工程）
- **算力**：以 **V100-天** 计量。论文称要匹配扩散模型当时 SOTA 性能，StyleGAN-XL 在单卡 V100 上整模训练约 **400 天**，而同样找最优模型 ADM 把 256²→512² 需从 393 涨到 **1914 V100-天**——StyleGAN-XL 用零头算力即达到。渐进增长是省算力关键：到 512² 阶段仅再训 **2 V100-天**即达 prior SOTA 的 FID 3.85；1024² 阶段训 **1 V100-天**即得 FID 2.8。注：作者明确这些数不完全可比（其 stem 是预训练的，只给数量级感觉）。
- **并行/混精/吞吐**：训练用官方 StyleGAN3 PyTorch 代码库（自定义 CUDA kernel），多 GPU（消融用 4 GPU、batch 256；ImageNet 主训用 8 GPU），梯度累积自动补齐总 batch；混合精度/具体吞吐数字**未披露**。
- **推理（Table 3，batch=1，V100-秒）**：GAN 单次前向出图，**StyleGAN-XL 0.05 / 0.07 / 0.10 秒**（128²/256²/512²）；对比 **ADM 27.07 / 40.26 / 91.54 秒**——快约 **3 个数量级**（512² 约 900×）。
- **部署**：开源代码+多分辨率预训练 .pkl（ImageNet 16²~1024²、FFHQ、CIFAR-10、Pokémon），HF Space 在线 demo。

## 评测 benchmark（把效果讲清楚）
所有指标用官方 StyleGAN3 代码库评测；P/R 用 10k 真 vs 50k 生成样本算（遵循 ADM 口径）。还提出 **rFID**（随机初始化 Inception 的 pool_3 层算 Fréchet 距离，避免引导模型「为 FID/IS 作弊」）与 sFID（空间结构）。

**ImageNet 主结果（Table 2，论文自评 FID；下表逐格按 PDF 原文核对）：**

| 分辨率 | 模型 | FID↓ | sFID↓ | rFID↓ | IS↑ | Pr↑ | Rec↑ |
|---|---|---|---|---|---|---|---|
| 128² | BigGAN | 6.02 | 7.18 | 6.09 | 145.83 | 0.86 | 0.35 |
| 128² | CDM | 3.52 | 128.80 | — | 128.80 | — | — |
| 128² | ADM | 5.91 | 5.09 | 13.29 | 93.31 | 0.70 | 0.65 |
| 128² | ADM-G | 2.97 | 5.09 | 3.80 | 141.37 | 0.78 | 0.59 |
| 128² | **StyleGAN-XL** | **1.81** | 3.82 | 1.82 | 200.55 | 0.77 | 0.55 |
| 256² | StyleGAN2 | 49.20 | — | — | — | — | — |
| 256² | BigGAN | 6.95 | 7.36 | 75.24 | 202.65 | 0.87 | 0.28 |
| 256² | CDM | 4.88 | 158.70 | — | 158.70 | — | — |
| 256² | ADM | 10.94 | 6.02 | 125.78 | 100.98 | 0.69 | 0.63 |
| 256² | ADM-G-U | 3.94 | 6.14 | 11.86 | 215.84 | 0.83 | 0.53 |
| 256² | **StyleGAN-XL** | **2.30** | 4.02 | 7.06 | 265.12 | 0.78 | 0.53 |
| 512² | BigGAN | 8.43 | 8.13 | 312.00 | 177.90 | 0.88 | 0.29 |
| 512² | ADM | 23.24 | 10.19 | 561.32 | 58.06 | 0.73 | 0.60 |
| 512² | ADM-G-U | 3.85 | 5.86 | 210.83 | 221.72 | 0.84 | 0.53 |
| 512² | **StyleGAN-XL** | **2.41** | 4.06 | 51.54 | 267.75 | 0.77 | 0.52 |
| 1024² | **StyleGAN-XL** | **2.52** | 4.12 | 413.12 | 260.14 | 0.76 | 0.51 |

（注：以上每格数值已逐一对照 PDF Table 2 原文，**纠正了此前 128²/256² 整行错位的问题**——论文 Table 2 报的 StyleGAN-XL FID 为 128²=**1.81**、256²=**2.30**、512²=**2.41**、1024²=**2.52**；ADM 在 ImageNet 上**不带引导/上采样时 FID 较高**（如 256² 裸 ADM=10.94），带 G/U 后才到 3~4。发布的预训练权重 FID 与论文略有差异，README 报 128²=1.77、256²=2.26、512²=2.42、1024²=2.51。结论：**StyleGAN-XL 在 FID/sFID/rFID/IS 上全面超过 BigGAN 与同期 ADM-G-U**，唯 recall（多样性）多数分辨率低于带引导扩散——比 BigGAN 多样性强很多，但仍未完全追上扩散模型。BigGAN 单样本保真（Pr 高）但 recall 极低。注意 StyleGAN-XL 的 rFID 在 512²/1024² 显著偏高（51.54 / 413.12），高分辨率上随机-Inception 距离并不占优。)

**低分辨率 ImageNet（Table 6）**：16²=0.73、32²=1.10、64²=1.51。

**单峰数据集（Table 4，1024²）**：FFHQ-1024² **FID 2.02**（StyleGAN2 2.70、StyleGAN3 2.79）；Pokémon-1024² **25.47**（FastGAN 56.46、Projected GAN 33.96）。CIFAR-10 32² FID 1.85（README 权重表）。

**反演/编辑（Table 5，ImageNet val 512²）**：基础隐空间优化即可，StyleGAN-XL PSNR 13.45 / SSIM 0.33 / 重建-目标 FID 21.73，全面优于 BigGAN（PSNR 10.85 / SSIM 0.26 / FID 47.48）。配合 **PTI（Pivotal Tuning Inversion）** 可精确反演域内/域外图像并保持平滑；编辑支持 GANSpace 方向、in-plane 平移/外插、跨类 style mixing，及 StyleMC 文本驱动编辑。

**关键消融结论**：① 双 F（EfficientNet+DeiT-ViT）把 128² FID 从 19.51→**12.43**，远好于双 CNN（16.16）或不同预训练目标组合（自监督 MoCo-v2 无额外收益）；② 渐进增长对 FID 提升不大但**大幅省高分辨率算力**，且把平移等变 EQ-T 仅从 55 微降到 48（带混叠架构 EQ-T~15），证明几乎不引入 texture sticking；③ 分类器引导主要拉高 IS（35.74→86.21），但 ≤32² 会模式坍塌。

## 创新点与影响
**核心贡献**：
1. 证伪「StyleGAN 架构不适合多样数据」的成见——把问题归到训练策略，用 Projected-GAN + 小 z + 预训练类嵌入 + 渐进增长 + GAN 版 classifier guidance 一揽子方案把 StyleGAN3 扩到 ImageNet。
2. 在 ImageNet 上把 GAN 的 FID 推到当时 SOTA（128²=1.81、256²=2.30、512²=2.41，全面超 ADM-G-U 与 BigGAN），并**首次**在 ImageNet 尺度做到 1024² 合成。
3. 提出双特征网络（CNN+ViT）联合判别、GAN 版 classifier guidance（训练期对高分辨率施加）、rFID 评测等可迁移技巧。
4. 推理比扩散快 ~3 个数量级，且保留 StyleGAN 的隐空间可逆/可编辑性（PTI、StyleMC、GANSpace）。

**影响**：成为「GAN 仍能与扩散在 ImageNet 上掰手腕」的最强论据；其大规模 GAN 训练思路直接启发后续的 [[gigagan]]（把 GAN 进一步扩到文本到图像/十亿参数），并影响 StyleGAN-T 等文本条件 GAN 工作（同作者 Axel Sauer 线）。在「GAN vs 扩散缩放之争」中是 GAN 一侧的标杆数据点。

**已知局限**：① 模型比 StyleGAN3 大三倍，微调/部署开销高（作者建议探索 GAN 蒸馏）；② 继承 StyleGAN3 的弱可编辑性（为等变牺牲语义可控，W 空间编辑不如 StyleGAN2，需借 StyleSpace/StyleMC）；③ recall（多样性）仍不及扩散；④ 截断 trick 对高多样 GAN 不提升 precision，需新截断方法；⑤ 受限于缺乏更大的高清多样数据集，难再往上扩 megapixel 多样数据；⑥ 在「含人脸」类上 ADM 生成的人脸更可信。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2202.00273
- paper (PDF): https://arxiv.org/pdf/2202.00273
- github (official repo): https://github.com/autonomousvision/stylegan-xl
- project page: https://sites.google.com/view/stylegan-xl/
- HF Space (demo): https://huggingface.co/spaces/hysts/StyleGAN-XL
- 会议: SIGGRAPH '22 Conference Proceedings, DOI 10.1145/3528233.3530738

## 一手源存档（sources/）
- [arxiv-2202.00273.pdf](https://arxiv.org/pdf/2202.00273)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/stylegan-xl--readme.md)
