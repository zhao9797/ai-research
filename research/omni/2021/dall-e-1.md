---
title: "DALL·E: Zero-Shot Text-to-Image Generation"
org: OpenAI
country: US
date: "2021-02"
type: paper
category: t2i
tags: [autoregressive, transformer, dvae, vqvae, t2i, zero-shot, sparse-attention, clip-rerank]
url: "https://openai.com/index/dall-e/"
arxiv: "https://arxiv.org/abs/2102.12092"
pdf_url: "https://arxiv.org/pdf/2102.12092"
github_url: "https://github.com/openai/DALL-E"
hf_url: ""
modelscope_url: ""
project_url: "https://openai.com/index/dall-e/"
downloaded: [arxiv-2102.12092.pdf, dall-e-1--blog.md, dall-e-1--model-card.md, dall-e-1--readme.md, dall-e-1--arxiv-abs.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
DALL·E 是 OpenAI 2021 年 2 月发布的首个引爆全球关注的文生图模型：一个 **120 亿参数的自回归稀疏 Transformer**，把"文本 token + 图像 token"拼成单一数据流（最长 1280 token），用最大似然逐 token 建模图文联合分布；图像先由一个 **离散 VAE（dVAE）** 压成 32×32=1024 个离散 token（每个 token 取自 8192 词表）。在 MS-COCO 上**零样本**评测，人评 **90.0% 认为更真实、93% 认为更贴合 caption**（best-of-five 投票，对手为当时报告该数据集最佳 IS/FID 的领域专用 GAN [[df-gan]]）。

## 背景与定位
2021 年以前的文生图主流是 GAN 路线（[[reed-gan-t2i]]、StackGAN、AttnGAN、DM-GAN、DF-GAN），核心思路是在固定的小数据集（MS-COCO ~12 万图、CUB-200 鸟类）上**精心设计建模假设**：多尺度生成器、文本-图像注意力、辅助匹配损失、物体部件标签/分割掩码等 side information。样本仍常有物体扭曲、不合理摆放、前后景融合不自然等严重缺陷。

DALL·E 提出一个相反的、极简的假设："不要复杂架构和辅助损失，只要**足够的数据和规模**"。它把 GPT-3（[[gpt-3]]）的自回归语言建模范式直接搬到"文本+图像"序列上——延续了 OpenAI 自家 [[image-gpt]]（在像素上做自回归 Transformer）和 [[gpt-3]] 的"scale is all you need"信仰。技术上它属于 **two-stage 离散表示 + 自回归先验** 这一脉，直接继承 [[vqvae]]/[[vqvae-2]] 的"先学离散视觉码本、再在码本 token 上学先验"思路，但把第二阶段的 PixelCNN 先验换成了 12B 参数的稀疏 Transformer，并首次把规模推到 2.5 亿图文对 / 120 亿参数。它与同期发布的 [[clip]] 互为姊妹工作：CLIP 在 DALL·E 中被用作离线重排序器（rerank）来挑选最优样本。DALL·E 开创的"大规模自回归 T2I"范式直接启发了后续的 [[cogview]]、Parti、[[muse]] 等，也是后来 DALL·E 2 / 扩散路线兴起前的关键奠基。

## 模型架构
**整体两阶段**（类似 VQ-VAE）：

**Stage 1 — dVAE（离散视觉 tokenizer）**
- 把 256×256×3 的 RGB 图压成 **32×32 = 1024** 个 image token，空间分辨率下采样 **8 倍**，每个 token 取值于 **K=8192** 的码本。相对直接用像素，Transformer 的上下文长度缩短约 **192 倍**（256×256×3 / 1024 ≈ 192）。
- 编码器/解码器都是**卷积 ResNet**（bottleneck resblock），主用 3×3 卷积，skip 连接上用 1×1；编码器首层 7×7、末层 1×1（输出 32×32×8192 logits）；解码器首末层均 1×1。编码器用 **max-pooling** 下采样（实测 ELB 优于 average-pooling），解码器用最近邻上采样。
- 重建分布用作者自创的 **logit-Laplace 分布**（对 Laplace 随机变量套 sigmoid，把支撑限制在 (0,1) 内），解决"像素值有界、而 L1/L2 对应的 Laplace/Gaussian 支撑是整条实轴"的不匹配；解码器输出 6 张 feature map（RGB 各一组 μ 和 ln b）。
- 公开的 GitHub 仓库 `openai/DALL-E` **只放出了这个 dVAE**（PyTorch 包 `pip install DALL-E`），生成图像的 12B Transformer **未开源**。

**Stage 2 — 自回归 Transformer（先验）**
- **decoder-only 稀疏 Transformer**，架构沿用 Child et al. 2019 的 Sparse Transformer。**64 层注意力**，每层 **62 个注意力头**，**per-head state size = 64**，**dmodel = 3968**，合计 **120 亿参数**。
- 输入是单一数据流：最多 **256 个 BPE text token**（文本词表 16,384）拼上 **1024 个 image token**（图像词表 8192），最长 1280 token，自回归建模联合分布。
- **三种稀疏注意力掩码**：文本→文本用标准因果掩码；图像→图像用 **行注意力（row）/列注意力（column）/卷积注意力（convolutional）** 三种之一。卷积掩码只用在**最后一层**（11×11 kernel，带 wraparound）；其余各层按 `i-2 mod 4 == 0` 用列注意力、否则用行注意力（例如前四层为 row, column, row, row）。每个 image token 都能在某层注意到所有 text token。作者发现"文本注文本/图像注文本/图像注图像"用**同一个注意力算子**（联合归一化）比分开三个独立算子效果更好。
- **位置/padding 处理**：image token 的嵌入额外加上**行嵌入和列嵌入**（broadcast）；text 与 image 之间的 padding 位置不设 -∞，而是为 256 个文本位置**各自学一个专门的 padding token**——实测虽然验证 loss 略升，但对分布外 caption 的表现更好。

## 数据
- **规模**：从互联网收集 **2.5 亿（250M）图文对**，量级对标 JFT-300M。预备实验（≤1.2B 参数）只用 Conceptual Captions（330 万对）。
- **来源**：Conceptual Captions + **Wikipedia 的图文对** + **YFCC100M 的过滤子集**。**刻意不含 MS-COCO**；但因 MS-COCO 由 YFCC100M 派生，训练数据含有约 21% 的 MS-COCO 验证集**图像**（但不含其 caption），论文用去重做了对照，确认对结果无实质影响。
- **过滤清洗**（采用 Sharma et al. 2018 的子集 filter）：丢弃 caption 太短的；用 Python 包 `cld3` 判定**非英文**的丢弃；丢弃主要由 boilerplate 短语（如 "photographed on <date>"）构成的；丢弃**长宽比不在 [1/2, 2]** 的图像（否则训练时的方形 crop 会裁掉 caption 里提到的物体）。
- **预处理/增强**：训练 dVAE 与训练 Transformer 用略有不同的增强（见 Listing 1/2），核心是随机方形 crop + AREA 缩放到 256；**不做水平翻转**（因为图里可能含文字）。BPE 编码时对 caption 用 **10% BPE dropout**。保留约 **606,000 张图作验证**，收敛时未见过拟合。
- **标注/合成数据**：纯用网络原生 alt-text/caption，**无 re-captioning、无合成数据**（这是 2021 年与后来 DALL·E 3 等的关键差别）。

## 训练方法
- **总目标**：最大化图文联合似然的 **证据下界（ELB）**，分解 pθ,ψ(x,y,z) = pθ(x|y,z)·pψ(y,z)。Stage 1 对 (φ,θ) 优化（只训 dVAE），Stage 2 固定 (φ,θ) 只对 ψ（Transformer）优化先验。两阶段分开训优于联合训（ImageNet 预实验验证过）。
- **dVAE 训练（Stage 1）**：离散分布无法用重参数化梯度，作者**不用** VQ-VAE 的 online cluster + straight-through，而改用 **Gumbel-Softmax 松弛**（温度 τ→0 时收紧），并用 logit-Laplace 算似然。关键 trick：KL 权重 β 在前 5000 步从 0 升到 **6.6**（更大 β 反而促进码本利用、降低最终重建误差，与常规直觉相反）；松弛温度 τ 在前 150,000 步从 1 退火到 **1/16**（线性退火会发散）；step size 在 1.2M 步内从 1e-4 退到 1.25e-6；编码器末/解码器首用 1×1 卷积缩小感受野以更好泛化到真 ELB；resblock 输出乘小常数稳初始化。优化器 **AdamW**（β1=0.9, β2=0.999, wd=1e-4），iterate averaging 衰减 0.999。
- **Transformer 训练（Stage 2）**：image token 由 dVAE 编码器 logits **argmax**（不加 Gumbel 噪声，因为模型处于欠参数化 regime）。文本/图像交叉熵损失按各自 token 总数归一化后，**文本损失 ×1/8、图像损失 ×7/8**（更看重图像建模）。优化器 **AdamW**（β1=0.9, **β2=0.96**, wd=4.5e-2），梯度按范数裁剪阈值 4（仅 warm-up 期触发）；step size 5000 步 linear ramp 到 4.5e-4，loss plateau 时**手动减半，共减 5 次**，最终 step size 为初始的 1/32。iterate averaging（每 25 步异步拷到 CPU，衰减 0.99）。**未做任何 SFT / RLHF / 偏好对齐 / 蒸馏**——纯预训练。
- **训练量**：dVAE 训 **3,000,000 步**（总 batch 512）；Transformer 训 **430,000 步**（总 batch 1024）。
- **采样/推理**：生成时 t=1（不降温），每个 caption 采 **N=512 个候选**，用预训练对比模型（[[clip]]）打分**重排序**取 top-k（默认展示 top 32）。这等价于一种"语言引导搜索"，对样本质量影响巨大；rerank 样本数增到 32 后收益递减。

## Infra（训练 / 推理工程）
DALL·E 论文有相当篇幅是**大模型混合精度训练工程**，是其重要贡献：
- **硬件**：Transformer 用 **1024 张 16GB NVIDIA V100**；dVAE 用 64 张 V100（per-GPU batch 8，总 batch 512）。
- **混合精度**：绝大多数参数、Adam moment、激活存 16-bit；用 **activation checkpointing**（反向时在 resblock 内重算激活）。"让模型超过 10 亿参数还能 16-bit 不发散"是本项目最难的部分，根因是 **16-bit 梯度下溢（underflow）**。
- **per-resblock gradient scaling**：放弃全局 loss scaling，给**每个 resblock 单独一个梯度 scale**（共 128 个），各自动态调整（无 nonfinite 时每步 ×2^(1/1000)，遇 nonfinite 则 ÷√2 并跳过更新，clamp 在 [M·2^7, M·2^24]）；这是 Flexpoint 的轻量替代，且不需要专用 GPU kernel。配套规则：gains/biases/embeddings/logits 一律存 32-bit。
- **参数分片（ZeRO 式）**：12B 模型 16-bit 存储约 **24GB**，超过单张 16GB V100，故按机内 8 卡做 **parameter sharding**（Rajbhandari et al. 2019，即 ZeRO 思路）；forward/backward 时用 all-gather 预取下一/上一 resblock 的参数分片、用完即弃，用 reduce-scatter 聚合梯度，几乎完全把机内通信延迟藏在计算后。
- **梯度压缩（PowerSGD）**：跨机 all-reduce 是主瓶颈（机间带宽远低于机内），用 **PowerSGD** 把梯度压成低秩因子通信，**压缩率约 85%**（与模型大小无关；Transformer 用总 compression rank 896 即每卡 112，压缩率 ~86%）。工程细节包括用 Householder 正交化替代 Gram-Schmidt、为 error buffer 用自定义 16-bit 浮点格式、Q 矩阵固定为随机高斯且不更新（省去 warm-start）等。
- **Adam moment 压缩**：running mean 用 1-6-9 格式、running variance 用 0-6-10 格式存 16-bit。
- **GPU·时 / 总算力**：论文**未明确报告** total GPU-hours 或 FLOPs（只给了 1024×V100、430k steps）。

## 评测 benchmark（把效果讲清楚）
所有数字均来自论文正文/图表（已落盘 PDF）：
- **MS-COCO 零样本（人评，vs DF-GAN）**：best-of-five 投票，DALL·E 样本被选为**最真实的比例 90.0%**、被选为**最贴合 caption 的比例 93.3%**（正文另处写 93%）。注意：DALL·E **从未在 MS-COCO 上训练**（caption 完全没见过）。
- **FID / IS（MS-COCO，30,000 caption 子集）**：在轻微高斯模糊（半径 1）下，DALL·E 的 **FID 比最好的先验方法低约 6 个点**（领先），且 blur 半径越大领先越明显；blur 半径 ≥2 时 IS 也最高。即便**不加模糊**，FID 也与最好的先验方法相差**约 2 个点以内**。FID/IS 用 DM-GAN 官方代码计算。
- **数据重叠对照**：训练集含约 21% 的 MS-COCO 验证图，去重前后 FID 无显著变化。
- **CUB（鸟类，零样本）**：表现**显著较差**，FID 比 leading 先验方法**差近 40 个点**（12% 重叠，去重无明显差别）。作者认为零样本在 CUB 这类专门分布上吃亏，**fine-tuning 是有希望的改进方向**（留作 future work）。
- **CLIP 重排序消融**：rerank 候选数 N 从小增大，MS-COCO 的 FID/IS 持续改善，**到 N=32 后收益递减**。
- **对比基线**：AttnGAN、DM-GAN、DF-GAN（其中 DF-GAN 报告了当时 MS-COCO 上最好的 IS/FID）。
- **未报告**：GenEval / T2I-CompBench / DPG-Bench / HPSv2 / ImageReward / PickScore / MJHQ-30K 等现代 T2I benchmark 当时**尚不存在**，论文自然未涉及。

## 创新点与影响
**核心贡献**
1. 首次证明 **"纯自回归 Transformer + 海量数据 + 规模"** 就能做出高质量、自然语言可控的通用文生图模型，无需复杂架构/辅助损失/部件标注——把 T2I 从"领域专用建模"推向"通用大模型 scaling"范式。
2. **离散视觉 token（dVAE，Gumbel-Softmax 松弛 + logit-Laplace）** 把图像压到 1024 token，使 256×256 图像可纳入自回归 Transformer 上下文，并引入 KL 权重退火等稳定训练技巧。
3. **CLIP 离线重排序**（language-guided search）作为质量放大器，成为后续 T2I 的常用配方。
4. 一套**十亿级模型 16-bit 混合精度训练工程**（per-resblock gradient scaling + ZeRO 式参数分片 + PowerSGD 梯度压缩），影响远超 T2I 领域。
5. 涌现出**零样本图到图翻译、变量绑定、组合泛化、文本渲染**等未刻意设计的能力。

**影响**：DALL·E 是引爆公众对"AI 文生图"认知的里程碑（"穿芭蕾裙的萝卜遛狗""牛油果形扶手椅"成为标志性 demo），直接催生 CogView、Parti、Muse 等自回归/掩码 T2I 工作，并奠定了 OpenAI 后续 DALL·E 2/3 的产品线。其 two-stage 离散表示 + Transformer 先验思路，也为后来的多模态统一生成（如 Chameleon、Emu 等）提供原型。

**已知局限**
- dVAE 8× 压缩导致**高频细节丢失**，细纹理/文字/细线常模糊或失真（模型卡明确说不适合高保真图像处理、不宜当通用压缩器）。
- 专门分布（CUB）零样本表现差，**未做 fine-tuning**。
- 变量绑定**不稳定**（有时给两只动物都画上圣诞毛衣）。
- 需**采 512 个样本 + CLIP rerank** 才出好图，单样本质量与推理成本不占优；自回归逐 token 解码慢。
- 训练数据全为网络原生 caption，无 re-captioning，prompt 遵循度受限；存在偏见/安全的社会影响（**博客**明确提示计划后续分析"对工作流程/职业的经济影响、模型输出偏见、长期伦理挑战"；ICML 论文正文则无专门的 bias/safety 章节）。

## 原始链接
- blog: https://openai.com/index/dall-e/
- paper (arxiv abs): https://arxiv.org/abs/2102.12092
- paper (pdf): https://arxiv.org/pdf/2102.12092
- github (dVAE only): https://github.com/openai/DALL-E
- model card (dVAE): https://github.com/openai/DALL-E/blob/master/model_card.md

## 一手源存档（sources/）
- [arxiv-2102.12092.pdf](https://arxiv.org/pdf/2102.12092)  （arXiv 原文 PDF，不入 git）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/dall-e-1--blog.md)
- [model-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/dall-e-1--model-card.md)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/dall-e-1--readme.md)
- [arxiv-abs.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/dall-e-1--arxiv-abs.md)
