---
title: "Infra：训练规模·并行·tokenizer 工程·推理加速"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [infra, parallelism, tokenizer, vae, distillation, quantization, scaling, omni-survey]
---

# Infra：训练规模 · 并行 · tokenizer 工程 · 推理加速

> 横向综述章节。视觉/多模态生成的"工程底座"四件事——**用多少算力怎么切（训练规模与并行）**、**怎么把像素压成可学的 token（VAE/tokenizer）**、**怎么把出图变快变便宜（推理加速）**、以及**闭源产品永远藏起来的那部分**。本章的硬线索全部来自单工作页（已对抗式核过），用 [[slug]] 内链可回溯。

一句话主张：**2020–2026 这六年里，"模型变大"远不是主线，"把序列变短、把步数变少、把卡切对"才是。** 真正决定一个生成模型能不能 4K、能不能上端侧、能不能实时的，是 tokenizer 的压缩率和推理的步数——而不是参数量。下面按四维拆开，最后单列"黑盒边界"。

---

## 一、训练算力与并行：谁把数字说清了

### 1.1 一手 GPU·时是奢侈品——绝大多数模型只字不提

最值得先讲的事实是：**到 2026 年，连"训练用了多少卡、多少 GPU·时"这种最基础的数字，公开披露的都是少数。** 把单页里"算力规模"一栏逐个核过，结论是分裂的：

- **完全披露绝对算力的，几乎只剩早期学术模型和 Meta。** [[stable-cascade]] 的底层 Würstchen 论文给出一手数字：1B Stage C 仅 **24,602 A100 GPU-时**，Stage B 约 **11,000 GPU-时**，对照 SD 1.4 的 **150,000**、SD 2.1 的 **200,000**——把"训练效率/碳排"（估算 ~2,276 kg CO₂eq vs SD 2.1 的 15,000 kg）当成一等评测维度。[[movie-gen]] 则是工业界最大方的一家：**最多 6,144 张 H100**（700W、80GB HBM3，Meta Grand Teton 平台，节点内 8 卡 NVSwitch 全连、跨节点 400Gbps RoCE RDMA），音频模型甚至给到 **384 GPU × 14 天**预训练、**64 GPU × 1 天**微调的颗粒度。

- **披露了并行策略、却死活不给卡数的，是 2025 年起的绝对主流。** [[qwen-image]]（20B MMDiT）讲清了 **4-way 张量并行**布局、Megatron-LM 混合并行、激活重计算的取舍，但报告**明说未披露总 GPU 数/GPU·时**。[[hunyuan-video]] 给了完整 **5D 并行**（TP+SP+CP+DP+ZeroCache）和 AngelPTM/星脉网络，同样**未给卡数**。[[hunyuanimage-3-0]]（80B MoE）正文只有一句"efficient infrastructure enables large-scale training"，TP/EP/FSDP/吞吐**全无**。[[seedream-3-0]]、[[qwen-image-edit]]、[[emu3-5]]、[[sana]] 等都属此类。**这是一条清晰的行业趋势线：方法可以讲，算力是商业机密。**

### 1.2 并行范式：从 FSDP 单招到"序列维才是战场"

把各页的并行设计排在一起，能看到一条由"模型放不下"转向"序列放不下"的演进：

- **图像模型：FSDP 够用，直到 20B 才上 TP。** [[stable-cascade]] 用 PyTorch **FSDP** + slurm 就能训 3.6B。到 [[qwen-image]] 的 20B，报告点破关键门槛——**"单靠 FSDP 装不下 20B，故用 Megatron-LM"**，混合 DP+TP，MMDiT 用 NVIDIA Transformer-Engine 以便无缝切 TP 度，多头自注意力用 head-wise parallelism 降通信。一个被引用最多的工程结论也来自这里：**激活重计算把单卡显存从 71GB 降到 63GB（−11.3%），但单 iter 时间从 2s 涨到 7.5s（3.75×）——不划算，于是关掉重计算、只靠分布式优化器**（all-gather 用 bf16、梯度 reduce-scatter 用 fp32）。

- **视频模型：序列长度才是敌人。** [[wan-2-1]] 给了全行最透的 workload 分析——**DiT 占训练总算力 >85%**；序列长度 s 常达数十万甚至百万，attention 随 s² 增长，**s=1M 时 attention 可占端到端 95%**，14B DiT 在 s=1M/micro-batch=1 时激活显存可超 **8 TB**。对策是 **FSDP + 2D Context Parallel**（外层 Ring Attention + 内层 Ulysses，即 USP 思路）：在 256K 序列/16 GPU 场景把 2D CP 通信开销从纯 Ulysses 的 >10% 压到 **<1%**；128 GPU 示例配置为 CP=16（Ulysses=8×Ring=2）、FSDP=32、DP=4。[[movie-gen]] 在最贵的 768px/**73K token 上下文**阶段用满 **FSDP+TP+SP+CP** 四维（self-attn 用满所有维度），且因用全双向注意力、未用 GQA，**享受不到 LLM 因果掩码的 ~2× 加速、CP 通信的 K/V 比 LLaMa3 大 8×**——直接点出"视频 DiT 的并行特性与 LLM 不同"。[[seedance-1-0]] 则贡献了 **HSDP（Hybrid Sharded Data Parallelism）缓解超千卡扩展退化 + MLAC（多级激活检查点，异步 offload attention/FC2 输出做到 GPU 激活近零占用）+ 运行时感知负载均衡**（异质长短视频用 all-to-all 在 batch 内均衡）。[[cogvideox]] 的 context parallel 用在 VAE 上（时间维切 3D 卷积，因因果性每 rank 只需传 k−1 帧），还有 Explicit Uniform Sampling（按 rank 分 timestep 区间降 loss 方差）。

- **统一/自回归模型：照搬 LLM 栈。** [[emu3-5]]（34B）、[[emu3]]（8B）统一基于 **FlagScale**，TP=8/CP=2；DiDA 适配进一步上 **TP+PP+SP+ZeRO-1 DP** 混合并行。[[movie-gen]] 最核心的架构主张本身就是 infra 驱动的——**把视频骨干从 DiT 整体换成 LLaMa3 block，就为了复用 LLM 的 3D 并行栈与 scaling 经验**（消融显示质量 +18.6%、文本对齐 +12.6%）。

### 1.3 scaling 的另一条路：不堆参数，用算力换质量

[[pixart-and-sana-1-5]]（SANA-1.5）是"反堆参数"的标杆：**深度生长（model growth）**把 1.6B→4.8B（20→60 层）训练成本省 60%、收敛快 2.5×；**深度剪枝**（Minitron 式，用输入输出相似度算 block 重要性，发现头尾重要、中间冗余）把 4.8B 灵活压回 3.2B/1.6B，**仅微调 100 步/单 GPU ~5 分钟即可恢复**；**推理时缩放**（best-of-N 重复采样 + VILA-Judge 锦标赛评判）把 GenEval 从 0.81 推到 **0.96**，超 24B 的 Playground v3（0.76）整整 20 个点。配套的 **CAME-8bit 优化器**（一阶动量 block-wise 8-bit 量化）把优化器内存压到 AdamW 的 1/8，让 4.8B 能在单张 RTX 4090 上微调。这是"thoughtful optimization > 单纯堆参数"的完整论证。

---

## 二、VAE / tokenizer 工程：压缩率才是真正的杠杆

**一句话：决定生成模型快慢的不是 backbone，是 tokenizer 的下采样因子。** 因为 DiT 计算量随潜 token 数二次方增长（[[qwen-image-vae-2-0]] 写明复杂度 O(L²)=O(H²W²/f⁴)），压缩率每提一档，序列长度降一截，算力是平方级地省。这条线分两支——离散 token（自回归用）和连续 latent（扩散用）——下面合起来看压缩率的演进。

### 2.1 离散 tokenizer：从"够用"到"码本无限"

- **[[magvit-v2]]（2023-10）是分水岭论文，命题直白："LM 生成不如扩散，问题不在模型而在 tokenizer。"** 核心是 **Lookup-Free Quantization（LFQ）**——把码本嵌入维度降到 0、用符号函数二值化，从而把词表扩到 **2^18 ≈ 262K** 而生成质量仍随词表单调上升（传统 VQ 词表变大后 FID 反而恶化）。配它的 token，掩码语言模型在 ImageNet 512×512 首次反超扩散：**有引导 FID 1.91**（超 VDM++ 的 2.65，↓28%），且模型更小（307M）、步数更少（64 vs 250）。
- **[[emu3]]（2024）** 基于 SBER-MoVQGAN-270M，码本 32,768、**8×8 空间 + 4× 时间下采样**，把 512×512 图编码成 **4096 token**。
- **[[infinity-bitwise-var]]（2024-12）** 把 magvit-v2 的思路推到极致：**比特级建模**把词表理论扩到 **2^64（"无限词表"）**，用 BSQ（O(d) 近似 entropy penalty，避开 LFQ 在 d=20 即 OOM 的全码本相似度）+ 无限词表分类器 IVC（**d 个二分类器预测每比特**而非 2^d 个索引，省 99.95% 参数：8.8 万亿→0.65M）。Infinity-2B 把 GenEval 0.62→**0.73**，0.8 秒出 1024px（比 SD3-Medium 快 2.6×）。
- **[[emu3-5]]（2025-10）** 用 IBQ 框架、f=16 下采样、码本扩到 **131,072**、tokenizer 放大到 455M，借 REPA 蒸馏 SigLIP 特征增强语义性，**同一张图只用 Emu3 的 1/4 token**（1024² ≈ 4096 token）。

### 2.2 连续 VAE：压缩率从 8× 一路爬到 42×，再回头补保真

主流潜扩散十年都卡在 **f8**（[[latent-diffusion-ldm]] 的 SD-VAE，1024→128，通道 4/16）。突破来自两个方向——更高压缩、更高保真：

- **更高压缩的开路者是 [[stable-cascade]]（2024-02）**：落地 [[wurstchen]] 的三级级联，把文本条件扩散放进 **42.67× 压缩潜空间**（1024×1024 → 24×24 latent），靠 Stage A VQGAN + Stage B 潜扩散 + EfficientNetV2-S 语义压缩器三件套替代单一 VAE，Stage C 索性抛弃 U-Net 用 16 个无下采样 ConvNeXt block。代价是**人脸/高频细节弱、FID 偏高**——这是"压得越狠重建越差"的早期实证。
- **[[sana]]（2024-10）** 把压缩做成系统工程的地基：**DC-AE F32C32P1（32× 下采样、通道 32、patch=1）**，latent token 比 AE-F8C4P2 少 16×（DiT 端再少 4×）。关键消融——**把 token 压缩放在 AE 而非加大 DiT patch size 更优**（F32C32P1 生成 FID 优于 F8C16P4/F16C32P2，尽管后者重建 rFID 更好）。这直接撑起 0.6B 模型 4K 生成比 FLUX-12B 快 100×。
- **视频 VAE 走时空联合压缩。** [[movie-gen]] 的 TAE **8×8×8 三维各 8× 压缩**、C=16，定位并修掉了"high-norm latent dot → spot 伪影"这一 shortcut learning（Outlier Penalty Loss）。[[hunyuan-video]] 从零训 **4×8×8 Causal 3D VAE**（C=16），[[wan-2-1]] 的 **Wan-VAE 仅 127M 参数、4×8×8**，靠 RMSNorm + feature cache 支持**无限长（甚至 1080P）流式编解码**。[[cogvideox]] 从零训 **8×8×4 3D 因果 VAE**，并实证"16×16×8 压缩过激即使加通道也难收敛"。[[seedance-1-0]] 的 VAE 下采样 (4,16,16)、通道 C=48。[[qwen-image]] 复用 **Wan-2.1-VAE**（冻编码器只微调图像解码器，8×8 压缩、通道 16），意在让图像模型当未来视频 backbone。
- **2025 末的前沿是"压缩、保真、可扩散性三难"的统一。** [[flux-2]] 从零重训 **128 通道/token 的 VAE**（每 token 通道数：SD 16 / FLUX.1 64 / **FLUX.2 128** / RAE 768），用语义正则（REPA/DINOv2 式）+ 放大潜维度，**同时**把重建 rFID 做到 0.1124（SOTA）和可学习性 gFID 拉到 3.70（接近纯语义型 RAE 的 3.10，比 FLUX.1 的 10.13 降 63.4%）。[[qwen-image-vae-2-0]] 把这条线写成方法学：用**扩通道补空间损失**（信息瓶颈 N(z)=CHW/f²）+ Global Skip Connection（像素直达深层潜空间的高频捷径）+ DINOv2 语义对齐 + **attention-free backbone**（把算力从 O(N²) 降到卷积 O(N·k²)），让 **f16c128 首次在文字密集文档上（OmniDoc SSIM 0.9706/PSNR 30.45）超过所有 f8 VAE 含 FLUX.1-dev**。
- **最激进的"不压缩"主张是 [[rae-diffusion-transformers-with-representation-autoencoders]]（2025-10，谢赛宁组）**：直接用**冻结的 DINOv2/SigLIP2/MAE 编码器（768 维、不做通道压缩）+ 轻量 ViT 解码器**替换 SD-VAE，把扩散搬进"语义丰富、高维"的隐空间。论证 SD-VAE 三宗罪（卷积过时、低维信息瓶颈、纯重建隐空间线性探测 ImageNet 仅 ~8%），ImageNet 256² 无引导 gFID **1.51**、相对 SiT 提速 **47×**。关键洞察：**高维隐空间几乎不增算力——token 数由 patch size 固定，通道在 DiT 第一层即被投影到隐藏维度**。这把"自编码"从压缩机制重新定义为表示基座，FLUX.2 已预告 FLUX.3 探索类似路径。

> tokenizer 这一维的总脉络：**离散侧靠"码本无限化"（LFQ→BSQ）让自回归追平扩散；连续侧靠"高压缩降序列长 + 大通道/语义对齐补回保真"——压缩率从 8× 推到 16×/32×/42×，而文字保真这道坎一直要到 2025 末（FLUX.2 VAE、Qwen-Image-VAE-2.0）才在高压缩下被跨过。**

---

## 三、推理加速：步数蒸馏 · 缓存 · 量化 · 端侧

出图慢和贵，靠四类手段解决——**减步数（蒸馏/求解器）、减重复计算（缓存）、减比特（量化）、减序列（高压缩）**。把数字排出来：

### 3.1 步数蒸馏：从 50 步压到 4–8 步乃至 1 步

- **图像侧**：[[flux-2]] 的 [klein] 经尺寸+步数蒸馏做到 **4-step**（base 档 50-step）；[[qwen-image-edit]] 生态的 **Qwen-Image-Lightning** 对 Edit-2511 实现 **DiT NFE 降 25×、整体 42.55× 提速**（号称可实时编辑）。[[hunyuanimage-3-0]] 把 **MeanFlow 扩到 80B 统一模型蒸馏**、NFE 降到 **4–8 步**。[[emu3-5]] 的扩散图像解码器用 **LoRA 蒸馏把去噪步数 50→4（约 10× 加速）**。
- **视频侧**：[[seedance-1-0]] 多阶段蒸馏（TSCD 轨迹分段一致性 + APT 对抗训练扩到多步），DiT 在 4× 加速下仍有竞争力，端到端 >10×。[[wan-2-1]] 用 LCM/VideoLCM 蒸成 **4 步**一致性模型，配 Streamer 得 **10–20× 加速、8–16 FPS**（8×A100 实时 8 FPS 生 15 分钟长视频）。[[hunyuan-video]] 的 CFG distill 带 **1.9× 加速**。
- **求解器/调度器**（无需重训）：[[sana]] 的 **Flow-DPM-Solver** 把采样压到 **14–20 步**（vs Flow-Euler 的 28–50）；[[movie-gen]] 的 **Linear-Quadratic t-schedule** 用 **50 步逼近 250 步线性结果，最多 ~20× 加速**；[[hunyuan-video]] 的 time-step shifting 在 10 步极低步数下优于 movie-gen 的 linear-quadratic；[[seedream-3-0]] 的"一致噪声期望 + 重要性时间步采样"实现 **4–8× 提速**。
- **AR 模型的并行解码**：[[emu3-5]] 的 **DiDA（离散扩散适配）**——把训练好的 AR 模型上的视觉 token 从"逐 token 顺序解码"改造成"双向并行离散去噪"，**单图 ~20× 加速且质量无损**（T2I 1024²/4096 token：AR 120s → DiDA 10s），让自回归首次在速度与质量上同时逼近闭源扩散。

### 3.2 量化与缓存

- **量化**：[[wan-2-1]] 的 FP8 GEMM（DiT 提速 1.13×）+ 8-bit FlashAttention（Int8 算 S、FP8 算 O，借 DeepSeek-V3 的 FP8 跨块 FP32 累加），在 **NVIDIA H20 上达 95% MFU、提速 >1.27×**。[[sana]] 的 **W8A8 INT8**（per-token 激活 + per-channel 权重，CUDA 手写 GEMM + 核融合）让笔记本 GPU 1024px 从 0.88s→**0.37s（2.4×）**近无损。[[emu3-5]] 推理侧用 **FP8 量化**，4 卡 +50% 吞吐。[[hunyuan-video]]、[[flux-2]] 均发 FP8/NF4 权重。
- **缓存/核融合**：[[sana]] 的 Triton 融核（线性注意力前反向）带 ~10% 额外加速；[[qwen-image-edit]] 生态的 LeMiCa 缓存近 3× 无损、DiffSynth FBCache、[[hunyuanimage-3-0]] 的 FlashInfer（~3×）/Taylor Cache 均属此类。

### 3.3 端侧：把高分辨率塞进消费级显存

- **[[sana]]** 是端侧标杆：0.6B 模型在 16GB 笔记本 GPU <1s 出 1024px（量化后 **0.37s/张**），4bit-SANA（SVDQuant/Nunchaku）<8GB 显存可跑，DC-AE tiling 让 4K 推理在 22GB（offload+量化后 8GB）内完成。[[pixart-and-sana-1-5]] 的 4.8B 也能在 RTX 4090 上微调。
- **[[flux-2]]** 是另一端：32B DiT + Mistral-3 24B 文本编码器 + VAE，bf16 全量 **>80GB VRAM**（H100-80G 都装不下三件套），靠 NF4 4-bit 压到 24–32GB（4090/5090）、remote text-encoder 压到 ~18GB、**group_offloading 极限压到 8GB VRAM**（需 ~32GB RAM）。28 步是质量/速度甜点。这组数字赤裸地展示了"开源最强权重"与"能在家用卡上跑"之间的张力。
- 视频侧的端侧门槛仍高：[[wan-2-1]] 的 1.3B 仅 **8.19GB 显存** 跑 480P（RTX 4090 约 4 分钟/5s），但 14B 单卡无优化约 **30 分钟**；[[hunyuan-video]] 单卡推理 720p×1280×129f 需 **60GB** 显存峰值。

---

## 四、黑盒边界：哪些维度被系统披露、哪些永远黑盒

把开源/闭源两侧逐页对照，能划出一条清晰的"披露边界线"：

### 4.1 闭源产品：架构本身就是产品机密

- **[[sora]]** 技术报告原文直接声明 **"Model and implementation details are not included in this report"**——参数量、层数、tokenizer 结构、文本编码器选型、潜空间维度**全部未披露**，只能确证"时空潜 patch + DiT + 视频压缩网络"的高层设计和"base/4×/32× 算力的 scaling 实证"。
- **[[gpt-image-1]]**：OpenAI 未发论文，只在发布白板给出 `tokens → [transformer] → [diffusion] → pixels` 的两段式（自回归先验 + 扩散末端解码器），**tokenizer/VQ、潜空间维度、解码器规模、参数量、数据规模全部未披露**。
- **[[imagen-3]]**：报告把架构当产品机密——**denoiser 是 U-Net 还是 DiT、用什么 VAE、文本编码器是 T5 还是 Gemini-based、参数量，全是"未披露"**；唯一确证的硬件信息是用 **TPUv4/TPUv5** 训练，但**算力规模/GPU·时/并行/吞吐仍未披露**。
- **[[gemini-3-pro-image-nano-banana-pro]]**：明说"built on Gemini 3 Pro"，但**backbone 类型（DiT/自回归/掩码）、参数量、tokenizer/VAE、文本编码器全部未披露**；能讲的只有产品参数（最多 14 张参考图、1K/2K/4K、SynthID 水印）。

### 4.2 开源/半开源：方法越来越透，绝对算力越来越藏

值得强调的是，**"开源"不等于"infra 透明"**。即便权重开放、论文详尽，2025 年起的中国大厂模型几乎一致地**披露并行策略与单卡显存、却隐去集群规模与 GPU·时**：[[qwen-image]]、[[hunyuan-video]]、[[hunyuanimage-3-0]]、[[seedream-3-0]]、[[qwen-image-edit]]、[[emu3-5]]、[[sana]] 全部如此。最透明的反而是早期学术工作（[[stable-cascade]] 给到 GPU-时与碳排）和 Meta（[[movie-gen]] 给到 6,144×H100 + 各阶段卡天 + 73K 上下文配方）。

### 4.3 一个被隐去但能侧面读出的维度：训练用的什么卡

闭源/合规背景下，**硬件型号本身成了信号**。[[wan-2-1]] 把 FP8 优化基准跑在 **NVIDIA H20**（中国特供低带宽卡）上并报 95% MFU，[[seedance-1-0]] 的端到端延迟基准用 **NVIDIA-L20** 报 41.4s/5s@1080p——这两处"非旗舰卡"出现在 ByteDance/Alibaba 的报告里，间接折射出受限算力下的工程取向（把 FP8/序列并行/激活 offload 做到极致以补硬件代差）。而 Meta（H100）、Google（TPU）则直接点名旗舰硬件。

### 4.4 边界总结

| 维度 | 系统披露的代表 | 永远黑盒的代表 |
|---|---|---|
| 训练总算力（卡数/GPU·时） | [[stable-cascade]]（24.6K A100h）、[[movie-gen]]（6144 H100） | [[qwen-image]] / [[hunyuanimage-3-0]] / [[sora]] / [[imagen-3]] / [[gpt-image-1]] |
| 并行策略 | [[wan-2-1]]（2D CP）、[[hunyuan-video]]（5D）、[[seedance-1-0]]（HSDP+MLAC）、[[movie-gen]]（4D） | [[sora]] / [[imagen-3]] / Nano Banana / [[gpt-image-1]] |
| VAE/tokenizer 结构 | 几乎所有开源（[[sana]] / [[flux-2]] / [[wan-2-1]] / [[emu3-5]] / [[qwen-image-vae-2-0]]） | [[imagen-3]] / Nano Banana / [[gpt-image-1]]（仅"compressed representations"一句） |
| 推理加速细节 | [[sana]] / [[wan-2-1]] / [[seedance-1-0]] / [[emu3-5]]（DiDA） | 闭源产品仅给"单张约 1 分钟"级别的体感数字 |
| 训练数据规模/配比 | [[movie-gen]]（O(100)M 视频）、[[qwen-image]]（七阶段过滤） | 几乎全部模型对绝对条数/配比含糊；闭源全黑 |

> 一句话收束：**到 2026 年，生成模型的 infra 披露呈"M 型"——学术小模型和 Meta 给得最全，中国开源大厂给方法不给算力，纯闭源产品（OpenAI/Google）连架构都当机密。** 而无论开源闭源，**训练数据的绝对规模与配比，是全行业共同的、最稳定的黑盒。** 能被工程复现的，永远是 tokenizer 压缩率和推理步数这两个"可验证"的杠杆；藏起来的，永远是算力规模和数据配方这两个"花钱买来"的护城河。

---

## 相关章节

- 方法/架构演进见 `sections/` 同级的方法综述；本章只聚焦工程底座。
- 单工作页索引见 [[01-INDEX]]。
