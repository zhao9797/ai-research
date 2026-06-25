---
title: "模型架构演进：从 U-Net 扩散到统一 omni 骨干（2020–2026）"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [omni, architecture, diffusion, dit, mmdit, rectified-flow, autoregressive, visual-tokenizer, vae, text-encoder, unified-multimodal, survey]
---

# 模型架构演进：从 U-Net 扩散到统一 omni 骨干

> **概述**：2020–2026 这六年，视觉/多模态生成的架构沿四条互相缠绕的主线推进。**(1) 生成式公式（formulation）**：从 DDPM 的离散去噪马尔可夫链（[[ddpm]]），到 score-SDE 的连续时间 SDE / 概率流 ODE（[[score-sde]]），再到 rectified flow / flow matching 的"直线轨迹"（[[rectified-flow]] [[flow-matching]]），最终被 [[stable-diffusion-3]]/FLUX 这一代确立为 T2I 默认；与之并行的是离散 token 自回归（VQGAN→[[dall-e-1]]→[[parti]]）与 next-scale/masked 等非光栅 AR 变体。**(2) Backbone**：`U-Net（[[ddpm]]/ADM/[[latent-diffusion-ldm]]）→ DiT（纯 Transformer，[[pixart-alpha]]/[[gentron]]）→ MMDiT（文图双流，[[stable-diffusion-3]]）`，与 `LLM 式 decoder-only AR Transformer（[[chameleon]]/[[emu3]]）` 两大谱系并存、并在统一模型里融合。**(3) Visual tokenizer / VAE**：从 VQGAN 离散 codebook（[[taming-transformers-vqgan]]）分叉出"离散 VQ"（AR 路线）与"连续 KL-VAE"（LDM 路线，d=4→16→冻结复用），再到"语义编码器当 VAE"（[[rae-diffusion-transformers-with-representation-autoencoders]]）和 next-scale 残差量化（[[var]]/[[infinity-bitwise-var]]）。**(4) Text encoder / 条件注入**：`CLIP → T5（[[imagen]]）→ 冻结 MLLM hidden state（[[qwen-image]]）→ 干脆没有外部编码器（[[emu3]]/[[gpt-image-1]]）`；注入方式从"加到 timestep embedding"到 cross-attention（[[latent-diffusion-ldm]]）、adaLN（DiT 类条件）、双流共享注意力（MMDiT）、再到"条件即上文 token"（AR 早融合）。到 2025–2026，单一骨干"原生"承载任意模态理解与生成（[[qwen2-5-omni]]/[[bagel]]/[[gpt-image-1]]）成为前沿汇流点。

---

## 一、扩散三件套：把 U-Net 去噪做成 SOTA（2020）

现代视觉生成的地基由 2020 年三篇方法论文奠定，三者共享同一个 backbone——**带自注意力的像素空间 U-Net**——但分别给出了训练目标、采样器与连续时间理论。

- **[[ddpm]]**（UC Berkeley, 2020-06, paper）——把扩散重参数化为"预测噪声 ε"并去掉权重得到一行 MSE 目标 `L_simple`，首次让扩散达 GAN 级质量：无条件 CIFAR-10 **FID 3.17 / IS 9.46**，LSUN 256² 对标 ProgressiveGAN。Backbone 是 PixelCNN++/Wide-ResNet 式 U-Net，在 **16×16 分辨率插自注意力**，扩散时间步 t 经 sinusoidal embedding **加到每个残差块**——这是"扩散唯一的条件"（无文本、无 VAE、无 tokenizer）。CIFAR 模型仅 35.7M、LSUN 114–256M 参数。固定方差、采样需 **T=1000 步串行**是其两大短板。
- **[[ddim]]**（Stanford, 2020-10, paper）——证明 `L_simple` 只依赖边缘分布，于是构造一族非马尔可夫前向过程、得到 **确定性（σ=0）采样器**，**不改架构、不重训**即可把 1000 步压到 20–100 步：CelebA 20 步 DDIM FID 13.73 ≈ 100 步 DDPM，10×–50× 加速；并揭示其等价于一个概率流 ODE 的 Euler 解，可逆编码—重构（DDIM inversion 即由此而来，后成 prompt-to-prompt 类编辑基石）。
- **[[score-sde]]**（Stanford/Google Brain, 2020-11, paper, ICLR21 Outstanding）——用连续时间 SDE 统一 SMLD/NCSN 与 DDPM（分别是 VE/VP-SDE 的离散化），提出 **Predictor-Corrector 采样**与 **概率流 ODE**（确定性、可算精确似然），并升级 backbone 为 **NCSN++/DDPM++**（FIR 抗锯齿采样、skip×1/√2、BigGAN 残差块、4 blocks/分辨率、连续时间用 random Fourier feature 编码 t）。CIFAR-10 刷到 **FID 2.20 / IS 9.89**、似然 2.99 bits/dim，首次用 score 模型生成 1024×1024。

同月 **[[taming-transformers-vqgan]]**（Heidelberg CompVis, 2020-12, paper）开辟了**离散 token 自回归**这条平行赛道：在 VQ-VAE 上加 patch 判别器（对抗）+ LPIPS 感知损失 + 自适应 λ，训出强压缩 tokenizer（256² → **16×16=256 个 token**，codebook 1024/16384），再用 GPT-2 式 AR Transformer 建模 token 序列。其分工哲学——"CNN+GAN 压低层统计、Transformer 建长程组合"——直接被 [[latent-diffusion-ldm]]（复用其 autoencoder 做 latent）、[[parti]]、[[muse]]、[[chameleon]] 继承；class-cond ImageNet 256² 自回归 SOTA **FID 15.78（无拒绝）/ 5.88（classifier rejection）**，1.4B 参数约为 VQVAE-2 的 1/10。两位一作 Esser/Rombach 正是 Stable Diffusion 核心作者。

---

## 二、似然、引导与 guidance 旋钮（2021–2022）

DDPM 留下三个缺口（似然差、不确定能 scale、采样慢），由 OpenAI 一条改进线补齐，并催生 guidance 这一统治性机制。

- **[[improved-ddpm]]**（OpenAI, 2021-02, paper）——四点改进：**学习反向方差**（在 log 域对 β_t/β̃_t 插值，配混合目标 `L_hybrid=L_simple+0.001·L_vlb` 且对 μ 加 stop-grad）、**余弦噪声调度**（修正 linear 在低分辨率"末端过噪"）、**VLB 重要性采样**降梯度噪声、**跳步快采样**。把 ImageNet 64² 似然做到 **3.53 bits/dim**，并因学习方差白送"50–100 步保质量"。架构上把注意力扩到 8×8、改 multi-head，并引入 **scale-shift / AdaGN（自适应 group norm）** 注入时间步——这个组件被后续 ADM 沿用。
- **[[diffusion-models-beat-gans]]**（OpenAI, 2021-05, paper）——通过架构消融得到 **ADM**（多分辨率 32/16/8 注意力、每头 64 通道、BigGAN 上下采样残差块、AdaGN 注入 time+class，AdaGN 把 FID 15.08→13.06），并发明 **classifier guidance**：用带噪图分类器梯度 `∇log p(y|x_t)` 把均值平移，一个标量 s 在"多样性↔保真度"间权衡。首次让扩散全分辨率超 BigGAN-deep：ImageNet 128² **FID 2.97**、256² **4.59（+上采样 3.94）**、512² **7.72（3.85）**，且 recall 显著更高。
- **[[classifier-free-guidance]]**（Google Brain, 2022-07, paper）——用同一网络 + null token **联合学有/无条件分数**（训练时以概率丢条件），采样时外推 `(1+w)·ε(z,c) − w·ε(z)`，**零额外参数、剔除分类器**。ImageNet 128² 在 w=0.3 时 FID 2.43，优于带分类器的 ADM-G（2.97）。CFG 此后成为**几乎所有**文生图/视频扩散的标配（negative prompt、guidance distillation 皆源于此）。

集大成者是 **[[latent-diffusion-ldm]]**（LMU/Heidelberg CompVis/Runway, 2021-12, paper）——把扩散从像素搬进**预训练 VAE 的低维潜空间**（下采样 f=4/8），并用 **cross-attention 注入任意 token 化条件**（文本/语义图/布局）。两阶段解耦：第一阶段 VQGAN 式 autoencoder（KL-reg 或 VQ-reg，弱正则保高保真，R-FID f4-KL **0.27**），训完冻结复用；第二阶段在 latent 上跑 ADM U-Net。ImageNet 类条件 LDM-4-G **FID 3.60（400M 参，271 V100-days）超 ADM-G 4.59**，MS-COCO 文生图 LDM-KL-8-G **FID 12.63（1.45B）**对标 GLIDE（6B）/Make-A-Scene（4B）。注意此时文本编码器还是**从头训的 BERT-tokenizer Transformer**，并非后来 SD 用的冻结 CLIP——"潜空间扩散 + cross-attention 条件"这一统治至今的范式由此定型，直接催生 [[stable-diffusion-1]]。

---

## 三、像素级级联：T5 大文本编码器登场（2022–2023）

与"潜空间 + CLIP"路线并行，Google 走的是"**像素空间三级级联 + 冻结大语言模型文本编码器**"。

- **[[imagen]]**（Google Brain, 2022-05, paper）——管线 `text → 64² base 扩散 → 64→256 超分 → 256→1024 超分`，三级都条件于同一份文本嵌入、都用 CFG。核心发现：**用只读纯文本预训练且训练时冻结的 T5-XXL encoder（4.6B）当文本编码器，比放大图像 U-Net 更能提升对齐**。条件注入双路：pooled 向量加到 timestep embedding + 整段序列做 cross-attention（消融证明序列 cross-attn 显著优于 pooling）。还为超分设计 **Efficient U-Net**（参数下移到低分辨率块、skip×1/√2、调换采样与卷积顺序，采样快 2–3×）。零样本 COCO **FID-30K 7.27**，并提出 DrawBench 人评。base 2B / 超分 600M+400M。
- **[[deepfloyd-if]]**（Stability/DeepFloyd, 2023-04, model-card）——开源复刻 Imagen：**冻结 T5-XXL（~4.5B）+ 三级像素级联 U-Net（64→256→1024）**，把算力堆在 64² base（IF-I-XL **4.3B**），是首个能可靠把正确文字渲染进图像的开源模型，零样本 COCO **FID-30K 6.66**。代价是 T5+两级 U-Net 高达 4.5B+4.3B+1.2B 参数；第三级 1024 超分权重从未发布，实际用 SD x4 Upscaler 顶替。

T5（或 T5+CLIP 组合）从此成为高对齐文生图的标配文本塔，被 [[pixart-alpha]]、[[gentron]]、[[stable-diffusion-3]] 全面继承。

---

## 四、Backbone 换芯：U-Net → DiT → MMDiT（2023–2024）

DiT（Peebles & Xie 2023，本调研无独立单页，经 [[pixart-alpha]]/[[gentron]] 转述）用**纯 Transformer 在 latent patch 序列上做扩散**，以 adaLN-Zero 注入类条件，证明可扩展性优于 U-Net——但原版只做 ImageNet 类条件。两项 2023 工作把它推上文生图：

- **[[pixart-alpha]]**（Huawei Noah, 2023-09, paper, ICLR24 Spotlight）——首个把 DiT 做到"近商用"的开源 T2I。在 **DiT-XL/2**（28 block, 0.6B）里 self-attn 与 FFN 之间插 **cross-attention 注入 T5（Flan-T5-XXL, 120 token）**（输出投影 zero-init 以复用 ImageNet 预训练权重）；用 **adaLN-single**（只在首 block 算一组共享 time 调制 + 各层可学习 embedding 微调）把 DiT 中占 27% 的 per-layer adaLN MLP 瘦身、参数比 833M 配置减 26%；配三阶段训练 + LLaVA 高密度 re-caption，仅 **753 A100-days（~SD1.5 的 12%）**就达 COCO **FID 7.32**、T2I-CompBench 6 项 5 项最优。VAE 直接复用 LDM 冻结 VAE。
- **[[gentron]]**（Meta/HKU, 2023-12, paper）——把 DiT 从类条件推到自由文本并扩到 **3B**（GenTron-G/2，3083.8M）。两条关键实证：**(a) 条件注入** adaLN 在自由文本下失效（类条件只有有限固定信号、全局调制够用；自由文本需空间细粒度对齐），**cross-attention 全指标占优**（但保留 adaLN 单独建模 time）；**(b) 文本编码器** CLIP-L + Flan-T5-XXL 组合最佳，用 interleaved cross-attention 交替注入。T2I-CompBench 综合 49.99 超 PixArt-α/SDXL，并首次用纯 Transformer 试水视频（只加轻量 TempSelfAttn）。

集大成者 **[[stable-diffusion-3]]**（Stability AI, 2024-03, paper）——两大架构升级合流：

1. **生成式公式换 rectified flow**：通过 61 种公式的控制变量大规模对比，确认 **RF + logit-normal 中间步加权**优于标准 DDPM/EDM 的弯曲轨迹。
2. **MMDiT（多模态扩散 Transformer）**：文本与图像序列拼接后做联合注意力，但**各持一套独立权重**（独立 LayerNorm/Linear/MLP/modulation），实现双向信息流——优于 PixArt 的"文本单向喂入"。加 **QK-RMSNorm** 抑制高分辨率微调时的 attention-logit 爆炸（使 bf16 稳定）。文本塔用 **CLIP-G + CLIP-L + T5-XXL 三编码器**（池化向量进 AdaLN modulation，T5 序列进注意力），且推理可灵活 drop。VAE **latent 通道从 d=4 提到 d=16**（重建与 scaling 双赢）。规模由深度 d 决定（hidden=64d），最大 d=38（8B），GenEval **0.74（w/DPO@1024²）超 DALL·E 3 的 0.67**。SD3 是 SD 系从 U-Net 转向 **DiT+flow matching** 的转折点，直接奠定 [[flux-1]]（同批作者）范式。其潜空间公式由两篇 2022 方法论文提供：

- **[[rectified-flow]]**（UT Austin, 2022-09, paper）——把生成与域迁移统一为"运输映射"，用最小二乘回归学 ODE 拟合两分布样本对的直线方向 `X1−X0`，配 reflow 拉直 + distillation 实现单步生成（CIFAR-10 蒸馏后 2-RF **FID 4.85**、全步 1-RF **FID 2.58**）。沿用 score-SDE 的 DDPM++ U-Net、像素空间无 VAE。
- **[[flow-matching]]**（Meta FAIR/Weizmann, 2022-10, paper）——simulation-free 训练 CNF：Conditional Flow Matching 证明边际/条件向量场损失梯度等价，并用 **OT 直线路径**替代扩散曲线（σ_min→0 时即 rectified flow 的直线插值）。ImageNet-128 **FID 20.9**（仅 500k iter 即超扩散基线 4.36m iter），复用 ADM U-Net。

三者（含 Stochastic Interpolants）殊途同归，成为 SD3/FLUX/Lumina 这代"RF 文生图"的理论基石。

---

## 五、自回归 next-token：把图像当语言说（2021–2024）

与扩散并行，"图像离散化成 token、用 LLM 式 AR Transformer 逐 token 生成"一脉从 VQGAN 延伸出来，到 2024 年完成"从外接 tokenizer 到统一早融合骨干"的演化。

- **[[dall-e-1]]**（OpenAI, 2021-02, paper）——120 亿参数稀疏 Transformer，把"文本 token（BPE 16384，≤256）+ 图像 token（dVAE，32×32=1024，词表 8192）"拼成最长 1280 的单一数据流做联合 AR 建模。dVAE 用卷积 ResNet + 自创 logit-Laplace 重建分布，下采样 8×。COCO 零样本人评 90% 更真实。
- **[[parti]]**（Google, 2022-06, paper）——**encoder-decoder Transformer**（像机器翻译：文本 enc → 图像 token dec），tokenizer 换 **ViT-VQGAN**（ℓ2 归一化 + 因子化码，8192 词表，256²→1024 token），scale 到 **20B**（decoder 64 层远深于 encoder 16 层，因建模图像更吃容量）。COCO 零样本 **FID 7.23 / finetuned 3.22**，证明 AR 在内容丰富度/组合泛化上能与扩散并驾。
- **[[chameleon]]**（Meta FAIR, 2024-05, paper）——**早融合（early-fusion）**纯 token 化基座（7B/34B）：图像（Make-A-Scene VQ，512²→1024 token，codebook 8192）与文本共享**同一套词表（65536，含 8192 图像码）、同一 embedding、同一 softmax、同一 Transformer 权重**，无独立编码器、无 cross-attention——"条件即上文 token"，由 `<start-image>`/`<end-image>` 触发生成。Backbone 沿用 Llama-2（RMSNorm/SwiGLU/RoPE），核心是用 **QK-Norm + post-norm 重排 + z-loss** 解决共享权重下的多模态 logit drift 发散。
- **[[emu3]]**（BAAI, 2024-09, tech-report）——8B 单 Transformer 用**纯 next-token**统一图/文/视频的生成与理解，**不用扩散、不用 CLIP、不用外接 LLM**。视觉 tokenizer 基于 SBER-MoVQGAN（codebook 32768，空间 8× 时间 4× 下采样，4×512² 视频或 512² 图 → 4096 token）；Llama-2 框架 + GQA + RoPE base 1e6 + 上下文 131072（容视频）；文本条件天然由序列里的 caption token 提供。图像生成超 SDXL、对标 DALL-E 3，视频 VBench 80.96（AR 唯一选手）。

这条线在 2025–2026 继续：**[[nextstep-1]]**（StepFun）用 14B AR 主干 + 仅 157M flow-matching 头在**连续图像 token**上做 next-patch 预测（无 VQ 量化损失），GenEval 0.63（Self-CoT 0.73）；**[[hunyuanimage-3-0]]** 用 80B/13B-激活 MoE LLM 走 Transfusion 路线，是迄今最大开源图像生成模型。

---

## 六、跳出光栅：next-scale 与 masked 生成（2023–2024）

AR 的"光栅扫描逐 token"既慢又违反图像的非序列本性，两类变体重新定义自回归单元。

- **next-scale（下一尺度预测）**：**[[var]]**（ByteDance/PKU, 2024-04, paper, NeurIPS24 Best Paper）——以整张**多尺度 token map** 为 AR 单元、尺度内 token 并行生成。tokenizer 是**多尺度残差 VQVAE**（共享 codebook 4096，从粗到细 K 张分辨率递增的 token map，残差式编码 `f -= φ_k(z_k)`）；Stage-2 是 GPT-2 式 Transformer 配 block-wise causal mask + AdaLN 注入类别。**首次让 AR 在 ImageNet 256² 超 DiT：FID 18.65→1.73、IS 350.2、推理快 ~20×**，并展现 −0.998 的幂律 scaling。**[[infinity-bitwise-var]]**（ByteDance, 2024-12, paper, CVPR25 Oral）——把 VAR 推到 T2I 且做**比特级**：词表理论扩到 2^64（BSQ 维度无关量化器），用"无限词表分类器 IVC"预测 d 个比特而非 2^d 个索引、"比特级自纠正 BSC"消除 teacher-forcing 失配；文本编码 Flan-T5-XL 经每层 cross-attention 注入，RoPE2d + scale embedding。Infinity-2B **GenEval 0.62→0.73 超 SD3-Medium**，0.8 秒出 1024²（比 SD3-Medium 快 2.6×）。
- **masked 生成（并行解码）**：**[[muse]]**（Google, 2023-01, paper）——在 VQGAN token 空间做 **MaskGIT 式掩码 Transformer 并行解码**（base 仅 24 步、super-res 8 步）。级联两个 VQGAN（base f16→256 token、super-res f8→4096 token，codebook 8192）+ 冻结 T5-XXL（cross-attention 注入），3B 模型 512² 单图 1.3s（比 Imagen/Parti-3B 快 >10×），COCO FID 7.88，天然支持零样本 inpaint/编辑。**[[show-o]]**（Show Lab/ByteDance, 2024-08, paper）——首个把**文本 AR（causal NTP）与图像离散扩散（MaskGIT 式 masked-token 预测）融进同一 1.3B Transformer**（Phi-1.5 骨干 + MAGVIT-v2 LFQ tokenizer），用 **Omni-Attention**（文本因果、图像全注意力）与 `[MMU]/[T2I]` 任务 token 统一序列；35M 数据即 COCO FID 9.24、GenEval 0.68，文生图步数约为 AR 的 1/20。

---

## 七、统一理解 + 生成：一个骨干两件事（2024–2025）

把"看懂图（理解）"和"画出图（生成）"塞进同一模型，是 2024–2025 的主线。关键张力是：理解要高层语义、生成要低层细节，单一视觉编码器难两全。几种代表性解法：

- **解耦视觉编码（双编码器）**：**[[janus]]**（DeepSeek, 2024-10, paper）——单一 AR Transformer（DeepSeek-LLM 1.3B），但**理解走 SigLIP 连续语义编码、生成走 LlamaGen VQ 离散编码（codebook 16384）**两条独立路径，缓解表征冲突。仅 1.3B 即理解超 LLaVA-1.5-7B（MMBench 69.4）、生成 GenEval 61%/COCO-FID 8.53 超 SDXL/DALL-E 2。其后 [[janus-pro]]（2025-01）靠数据与规模放大进一步。
- **单骨干双损失（AR + diffusion）**：**[[transfusion]]**（Meta/Waymo/USC, 2024-08, paper）——**单 Transformer、单套权重**，文本走 NTP、图像走 DDPM 去噪，混合序列从零联合预训练。Llama 风格骨干 + 模态特定轻量编解码层（图像经 86M VAE 压成 32×32×8 latent，再 linear/U-Net block 压成 patch 向量）；关键是 **Transfusion Attention**——整序列 causal、但单图内 patch 双向（消融：causal-only FID 61.3 → bidirectional 20.3）。7B/2T token，GenEval 0.63 超 DALL-E 2/SDXL 且文本能力持平 Llama 1。
- **MoT 双专家 + 共享注意力**：**[[bagel]]**（ByteDance Seed, 2025-05, paper）——7B 激活/14B 总参 **Mixture-of-Transformer-Experts**：理解专家（处理 text+SigLIP2 ViT token）与生成专家（处理 FLUX VAE token，rectified flow）**每层共享同一条多模态自注意力**、只在 FFN/QKV 按模态硬路由，实现"无瓶颈"耦合。理解看 SigLIP2、生成看冻结 FLUX VAE（latent 16 通道）；timestep 直接加到 VAE token hidden（非 AdaLN）。万亿级交错数据上涌现"自由形变编辑/多模态推理最晚收敛（~3.61T token）"的相位转变；GenEval 0.88（带 rewriter）超 FLUX.1-dev 0.82。架构消融证明 MoT 在生成/理解 loss 上一致优于 Dense/MoE。
- **冻结 MLLM + learnable queries 接扩散**：**[[metaqueries]]**（Meta/NYU, 2025-04, paper）——`token → [冻结 MLLM] → [256 个可学习 query] → [connector] → [扩散解码器] → pixels`，MLLM（Qwen2.5-VL 3B/7B）全程不动保留 SOTA 理解，仅用图文对 + 去噪目标训出 SOTA 生成。connector 24 层 Enc-Proj 仅 316M 参数；扩散头可换（Sana-1.6B/SD1.5）。首个在世界知识推理生成 WISE 上超 SD-3.5/FLUX 的统一模型（WiScore 0.55 远超 Janus-Pro-7B 0.35）——证明"冻结 LLM 在因果掩码下已是强力特征重采样器"。

文本编码器在这条线上完成最后一跳：从 CLIP/T5 走向**直接取冻结 MLLM 的 hidden state**当条件——典型如 **[[qwen-image]]**（Alibaba Qwen, 2025-08, tech-report）：20B 双流 MMDiT，**条件编码器是冻结的 Qwen2.5-VL（取最后一层 hidden state）**（理由：图文空间已对齐、保留语言能力、支持多模态输入解锁编辑），VAE 用 Wan-2.1 单编码器-双解码器（冻结编码器只微调图像解码器），新设计 MSRoPE 把文本编码放在网格对角线。编辑（TI2I）走双编码：原图经 Qwen2.5-VL 得语义特征注入文本流、经 VAE 得重建特征拼接进图像流。RL 后 GenEval 0.91（唯一破 0.9 的基础模型）、中文渲染碾压 GPT-Image-1。

---

## 八、any-to-any omni：生成端并入语言骨干（2024–2026）

终点是单一"原生"骨干承载任意模态的理解与生成。两种工程形态：

- **闭源 omnimodal（生成焊进对话 LLM）**：**[[gpt-image-1]]**（OpenAI, 2024-05 起, system-card）——把图像作为与文本同一序列的 token、由**同一个自回归 Transformer**在 `p(text, pixels, sound)` 上联合建模，白板明示 `tokens → [transformer] → [diffusion] → pixels` 的**"AR 先验 + 扩散末端解码器"**两段式（扩散被降级为 decoder，AR 才是承载语义/指令/文字的主体）；"条件"就是 AR 上下文本身，故指令遵循（稳定协调 10–20 对象）、文字渲染、in-context 图生图极强。**[[gemini-2-0-flash-image]]**（Google DeepMind, 2025-03, blog）——同一对话模型在一次调用里**交错输出文本与图像**、支持多轮对话式编辑，与 [[chameleon]]/GPT-4o 同属"生成端并入语言骨干"。两者均**未披露** tokenizer/参数/解码器结构（AR-VQ 还是扩散 decoder 不明）。
- **开源端到端全模态**：**[[qwen2-5-omni]]**（Alibaba Qwen, 2025-03, tech-report）——文/图/音/视四输入、流式同出文本与语音的单模型，**Thinker-Talker 双脑**（Thinker 出文本，Talker 双轨 AR 接 Thinker hidden 出语音 token）+ **TMRoPE 时间对齐位置编码**（1 temporal ID=40ms，音视频逐帧对齐 + 每 2 秒时间交织）；视觉编码器取自 Qwen2.5-VL ViT（~675M），音频取自 Qwen2-Audio（Whisper-large-v3 初始化），语音生成经 Flow-Matching DiT + BigVGAN。7B 在 OmniBench Avg 56.13% 超 Gemini-1.5-Pro。

到 2025 下半年，**tokenizer/VAE 这一最底层组件也在被重新发明**：**[[rae-diffusion-transformers-with-representation-autoencoders]]**（NYU 谢赛宁组, 2025-10, paper）用**冻结的预训练表示编码器（DINOv2/SigLIP2/MAE）+ 轻量 ViT 解码器替换 SD-VAE**，把扩散搬到"语义丰富、不压缩"的高维隐空间，ImageNet 256² 无引导 gFID **1.51**、有引导 **1.13**，相对 SiT 提速 47×——预示着"VAE = 几何压缩器"向"VAE = 语义编码器"的范式迁移，与 [[bagel]]/[[qwen-image]] 用 MLLM/语义编码器做条件的方向遥相呼应。

---

## 九、四条主线一张图（小结）

| 维度 | 2020 起点 | 中段 | 2025–2026 前沿 |
|---|---|---|---|
| **生成式公式** | DDPM 离散去噪（[[ddpm]]） | score-SDE 连续 ODE（[[score-sde]]）→ CFG（[[classifier-free-guidance]]） | rectified flow / flow matching（[[stable-diffusion-3]]）；AR next-token（[[emu3]]）；连续 token AR（[[nextstep-1]]） |
| **Backbone** | 带注意力 U-Net（[[ddpm]]/ADM） | latent U-Net（[[latent-diffusion-ldm]]）→ DiT（[[pixart-alpha]]/[[gentron]]） | MMDiT 双流（[[stable-diffusion-3]]/[[qwen-image]]）；LLM 式 AR / MoT（[[chameleon]]/[[bagel]]） |
| **Visual tokenizer/VAE** | VQGAN 离散 codebook（[[taming-transformers-vqgan]]） | KL-VAE d=4 冻结复用（[[latent-diffusion-ldm]]）；VQ 离散（[[dall-e-1]]/[[parti]]）；next-scale 残差量化（[[var]]） | VAE d=16（[[stable-diffusion-3]]）；比特级 2^64（[[infinity-bitwise-var]]）；语义编码器当 VAE（[[rae-diffusion-transformers-with-representation-autoencoders]]） |
| **Text encoder / 条件注入** | timestep embedding（无文本，[[ddpm]]） | CLIP/T5 + cross-attention（[[imagen]]/[[deepfloyd-if]]/[[latent-diffusion-ldm]]）；adaLN 类条件→ cross-attn 文本（[[gentron]]） | 冻结 MLLM hidden state（[[qwen-image]]）；条件即上文 token（[[emu3]]/[[gpt-image-1]]）；learnable queries（[[metaqueries]]） |

一句话脉络：**像素 U-Net 去噪（2020）→ 潜空间 + cross-attention 条件（2021–2022）→ T5 大文本塔 + 像素级联（2022–2023）→ Transformer 换芯 DiT/MMDiT + rectified flow（2023–2024）→ 离散/连续 AR 与 next-scale/masked 变体（2021–2024）→ 单骨干统一理解生成（2024–2025）→ 原生 any-to-any omni 与语义编码器重写 VAE（2025–2026）**。
