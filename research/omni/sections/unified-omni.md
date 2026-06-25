---
title: "统一理解生成 & any-to-any 全模态专题"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [unified, understanding-generation, any-to-any, omni, early-fusion, decoupled-encoder, diffusion-ar-hybrid, autoregressive, rectified-flow, thinker-talker]
---

# 统一理解生成 & any-to-any 全模态专题

> **一句话主线**：2024–2026 的"统一模型"研究，本质是在反复回答三个问题——**理解能不能反哺生成（知识/推理迁移）**、**一套视觉表征该不该为"理解要语义、生成要像素"而解耦**、**in-context 编辑/交错生成的能力从哪来**。围绕这三问，学术界分化出三种范式：①早融合·单一 Transformer·离散 token（[[chameleon]]→[[emu3]]→[[show-o]]→[[x-omni]]）；②理解-生成解耦的"双塔/双路"（[[janus]]→[[janusflow]]→[[bagel]]/[[blip3-o]]/[[metaqueries]]）；③扩散+AR 混合（[[transfusion]]→[[show-o2]]/[[lumina-mgpt-2-0]]）。产品端则走向真正的 any-to-any 全模态（[[gpt-4o-native-image]]/[[gemini-2-0-flash-image]]/[[qwen2-5-omni]]/[[qwen3-5-omni]]/[[ming-omni]]）。本章按"谁在什么时间、用什么方法、把什么指标推到多少"串联，并在每条线索末尾收敛回三问。

---

## 0. 三个贯穿性问题（先立靶子）

1. **理解是否反哺生成？** 衡量它的标尺是 **WISE**（世界知识推理生成）这类"要先懂常识/物理/文化才画得对"的基准。早期纯离散 AR 统一模型在 WISE 上很低（[[emu3]] 0.39、[[janus-pro]] 0.35），说明"统一"只是把两个任务塞进一个网络、并未发生知识迁移；而把强 MLLM 的世界知识"查询"出来喂生成的 [[metaqueries]]（WiScore 0.55）和靠交错数据涌现的 [[bagel]]（带 CoT 0.70）才真正把理解的知识灌进了生成。
2. **视觉表征如何解耦？** 核心矛盾是"理解需要高层语义（SigLIP/CLIP 判别式特征）、生成需要低层结构（VQ token / VAE latent）"。[[chameleon]] 式单编码器在这对矛盾上做了牺牲（[[janus]] 消融实测：共享语义 tokenizer 把理解 POPE 从解耦的 87.0 拉到 83.9 以下），于是 [[janus]] 起把视觉编码"在入口处分叉"成为一条主线。
3. **in-context 编辑能力从哪来？** 三个来源：(a) 把图文当"联合分布"在交错数据上训出来的上下文一致性（[[gpt-4o-native-image]]、[[bagel]]）；(b) 把参考图当序列前缀、靠注意力做条件的 in-context 范式（[[lumina-mgpt-2-0]] 的 dual-panel、[[bagel]] 的 clean-VAE+ViT 条件）；(c) 冻结 MLLM 的 ICL 被"可学习查询"激活（[[metaqueries]]）。

---

## 1. 范式一：早融合 · 单一 Transformer · 离散 token

**核心信条**："把图像也量化成离散 token，和文本 token 共用一张词表、一套权重、一个 next-token 目标"，于是统一模型就退化成一个普通 LLM，直接吃 LLM 生态的 scaling 与 infra。代价是离散量化的信息瓶颈与自回归逐 token 的慢推理。

### 1.1 [[chameleon]]（Meta FAIR, 2024-05）— 把稳定性问题摊开

[[chameleon]] 是这条线的奠基：7B/34B，把 512×512 图像用 Make-A-Scene 式 VQ 编码成 **1024 个离散 token**（codebook 8192），与文本 BPE 合并成 **65,536 词表**，在 ~10T token 上**从头**训练单一 decoder-only Transformer。它最大的贡献不是效果而是**诊断并解决了早融合的训练发散**：共享 softmax 下不同模态熵差异大、logit 漂移到 bf16 范围外，必须用 **QK-Norm + Swin 式 norm 重排 + z-loss** 才能稳到 34B。效果上图像生成只做人评（对增强基线 GPT-4V+ 胜率 51.6%、对 Gemini+ 60.4%），**未报 FID/GenEval**；理解侧 COCO captioning CIDEr 达 SFT 后 140.8（开源 SOTA）。但公开 checkpoint **关闭了图像生成**，且 tokenizer 对含文字图像重建差——这两点暴露了离散范式的硬伤。

> 谱系：[[chameleon]] 直接承接 [[chameleon-cm3leon]]（CM3Leon，把 CM3 的 causal-masked 思路 scale 到自回归 T2I）。

### 1.2 [[emu3]]（BAAI, 2024-09）— "Next-Token Prediction is All You Need"

[[emu3]] 把这条信条推到最激进：8B 单 Transformer，**不用扩散、不用 CLIP、不用外接 LLM/文本编码器**，图/文/视频全离散化（视觉 tokenizer 基于 SBER-MoVQGAN，4×8×8 压缩、codebook 32768，一张 512² 图或 4 帧视频→**4096 token**）。它第一个证明纯 AR 能在多个一线基准同时达标：GenEval **0.66**（rewriter，超 SDXL 0.55、对标 DALL-E 3 0.67，但低于 SD3 0.74）、DPG-Bench 80.60、VBench 80.96（唯一 AR 视频选手，超 OpenSora-1.2）。它还**首次把 DPO 用于自回归视觉生成**（人评视觉质量 52.3→57.3）。

**对三问的回答**：表征上仍是单一离散 token（未解耦），理解走 encoder-free 路线、与 LLaVA-1.6-7B 相当；但理解**没有明显反哺生成**——WISE 仅 0.39。这正是范式一的天花板。

### 1.3 [[show-o]]（Show Lab/字节, 2024-08）— "图像不必也自回归"

[[show-o]] 的关键洞见：在同一 Transformer 里**文本保留自回归（NTP）、图像改用 MaskGIT 式离散扩散（masked-token prediction, MTP）**，并用 **Omni-Attention**（文本 causal、图像 full attention）随序列格式自适应切换。它以 1.3B（Phi-1.5）+ 35M 图文对拿到 MSCOCO FID **9.24**、GenEval **0.68**——逼近大数倍模型，且**文生图采样步数约为自回归的 1/20**。消融揭示了表征矛盾：理解任务上 CLIP-ViT 连续表征 ≫ MAGVIT-v2 离散 token，于是它不得不提供一个"理解专用 CLIP 输入"的 Show-o‡ 变体。这其实是**范式一向范式二妥协的早期信号**：纯离散 token 做理解就是吃亏。

### 1.4 [[x-omni]]（腾讯混元 X, 2025-07）— 用 RL"拯救"离散 AR

到 2025，主流已倒向 AR+扩散混合，[[x-omni]] 偏要回到**纯离散 AR**并证明它能"Great Again"——核心武器是 **RL（GRPO）**。它用 SigLIP2-g + VQ（codebook 16384）做**语义 tokenizer**（在理解任务上训，而非像素重建），Qwen2.5-7B 做 AR 主干，FLUX.1-dev 做离线扩散 decoder。机理上 RL 在整个采样过程提供监督、降低 AR 累积误差，并**把 AR 产出的 token 分布对齐到扩散 decoder 期望的分布**（弥合 SFT 阶段 tokenizer 与 decoder 各自独立训练的鸿沟）。结果：DPG-Bench **87.65**（统一模型 SOTA，超 GPT-4o 86.23、BAGEL 85.07）、GenEval 0.83；尤其**首个能精确渲染长中英文**（OneIG 文字渲染英文 0.901/中文 0.895，把 BAGEL 的 0.244、Show-o2 的 0.002 远远甩开），且**不依赖 CFG**（Emu3/Janus-Pro 去掉 CFG 质量暴跌）。关键发现 **RL > SFT+best-of-N**，与语言建模经验相反。

**小结**：范式一的演进 = 离散 token（[[chameleon]]）→ 纯 NTP all-in（[[emu3]]）→ 图像换 masked 离散扩散（[[show-o]]）→ 语义 tokenizer + RL 对齐（[[x-omni]]）。一条隐线是：**为了把理解做好，离散 token 一步步从"像素重建式"走向"语义判别式"**，这恰是范式二的核心主张提前渗透进来。

---

## 2. 范式二：理解-生成解耦的"双塔/双路"

**核心信条**：理解与生成对视觉表征的需求本质冲突，应在**入口处把视觉编码解耦**（理解走 SigLIP/CLIP 连续语义、生成走 VQ/VAE），共享或桥接一个 LLM。这条线又分裂出"自回归生成"与"扩散/流匹配生成头"两支，且越来越偏向"冻结强 MLLM、只训生成模块"。

### 2.1 DeepSeek Janus 家族 — 把"解耦"立为范式

- **[[janus]]（2024-10）** 第一个明确提出"统一框架内解耦视觉编码"：理解用 SigLIP-Large-384 连续语义、生成用 LlamaGen VQ（codebook 16384、下采样 16、384²→576 token），两路独立 adaptor 但共享单一 1.3B 自回归 Transformer。**它的消融是整条范式二的理论基石**：Exp-A（共享 VQ，类 Chameleon）理解 POPE 仅 60.1；Exp-C（共享语义 tokenizer 只训理解）POPE 83.9；Exp-D（SigLIP+VQ 解耦）POPE **87.0**、MMBench 69.4——坐实"共享单编码器在理解上做了折衷"。1.3B 即超 LLaVA-1.5-7B，GenEval 0.61、COCO-FID 8.53。
- **[[janusflow]]（2024-11）** 把生成从 VQ 自回归换成 **rectified flow**（[[rectified-flow]]，[[stable-diffusion-3]] 验证），证明**流匹配可"原生"嵌进 LLM、无需 Transfusion 式复杂注意力掩码**（普通 causal attention 即可），只需一对 ~70M 的 ConvNeXt encoder/decoder 在 SDXL-VAE latent 上做速度场预测。关键 trick 是 **REPA 表征对齐**（把 SigLIP 理解特征对齐到 LLM 第 6 层中间特征）。1.3B 即把 MJHQ FID 从 Janus 的 10.10 推到 **9.51**、GenEval 0.63、DPG 80.09。
- **[[janus-pro]]（2025-01）** 不改架构、只"加数据+加规模+改训练策略"，把 7B 推到 GenEval **0.80**、DPG 84.19、MMBench 79.2，成为 2025 年初开源统一模型标杆。

**三问回答**：解耦表征——典范；in-context 编辑——Janus 系列基本不做（JanusFlow 论文自陈"编辑未覆盖"）；理解反哺生成——**仍然没有**，Janus-Pro WISE 只有 0.35。这暴露一个关键事实：**光解耦表征不等于知识迁移**。要让理解真正反哺生成，得换思路。

### 2.2 [[metaqueries]]（Meta/NYU, 2025-04）— "冻结 MLLM + 可学习查询"激活 ICL

[[metaqueries]] 走到极致的解耦哲学——"生成归扩散、理解归 LLM"：**完全冻结 MLLM**（Qwen2.5-VL 7B），用一组 **256 个可学习查询**把 MLLM"查询"出生成条件，过一个 24 层 Enc-Proj 连接器（仅 316M）喂给可热插拔的扩散 decoder（Sana-1.6B / SD1.5），仅用 25M 图文对 + 标准去噪目标训练。它最重要的结果是**首个在 WISE 上超过纯 T2I SOTA 的统一模型**（WiScore **0.55**，超 FLUX.1-dev 0.50、SD-3.5 0.46，碾压 Janus-Pro 0.35/Emu3 0.39）——证明"**冻结 MLLM 的世界知识与 in-context learning 能被查询并转移到生成**"。关键消融：可学习查询 vs LLM 末层 embedding，质量几乎相同（FID 6.35 vs 6.41），但前者 WiScore 0.55 vs 0.48——**可学习查询的价值正是激活 ICL**（这是"末层 embedding 当 text encoder"路线如 Lumina-Next/Sana/Kosmos-G 做不到的）。MJHQ FID **6.02** SOTA。它还从 mmc4 天然图像对造了 2.4M 指令数据（MetaQuery-Instruct），编辑能力从重建迁移、仅微调 1000 步。

### 2.3 [[blip3-o]](Salesforce, 2025-05) — 系统化"自回归+扩散"设计空间

[[blip3-o]] 把 GPT-4o 被推测的"token→AR→diffusion→pixels"管线做成系统研究，三轴交叉给出可复现配方：**(1) 图像表征：CLIP 语义特征 > VAE 像素特征**（每图固定 **64 个连续向量**，比 VAE 高分辨率长序列紧凑，训练更快质量更高）；**(2) 训练目标：Flow Matching > MSE**（MSE 只对齐分布均值、输出趋确定，FM 继承随机性能多样采样）；**(3) 训练策略：顺序训练 > 联合**（冻结 Qwen2.5-VL 底座、只训 1.4B DiT）。8B 拿 GenEval **0.84**、WISE **0.62**、理解 MMMU 50.6/MME-P 1682.6。它还开源 **BLIP3o-60k**（GPT-4o 蒸馏的 60k 指令对，给任意 T2I 带来 5–7 分增益），是少有的代码/权重/数据全开放基线。

### 2.4 [[bagel]]（字节 Seed, 2025-05）— 用交错数据"涌现"出 in-context 与世界建模

[[bagel]] 在范式二里属"无瓶颈"派（Integrated Transformer），但它的真正贡献是**数据范式**：7B 激活/14B 总参的 **MoT（Mixture-of-Transformer-Experts）**——理解专家处理 ViT/text token、生成专家处理 VAE token，**每层共享同一条自注意力序列、只在 FFN/QKV 按模态硬路由**，因此理解(next-token)与生成(rectified flow)无任何压缩 connector 瓶颈地交互。双编码器："理解看语义"用 SigLIP2、"生成看像素"用 FLUX-VAE。

它最受引用的发现是**能力涌现的相位转变**：以"达 85% 峰值所需 token"衡量，理解 ~0.18T、生成 ~0.68T 早早饱和，**经典编辑要 ~2.64T，自由形变编辑/多模态推理要 ~3.61T 才涌现**（3T token 后 IntelligentBench 从 15 飙到 45），而 **loss 曲线完全看不出这种跃变**。效果：GenEval 0.88(rewriter)/0.82、WISE 0.52→**0.70(Self-CoT)**、GEdit-Bench G_O 6.52（持平专用 SOTA Step1X-Edit）、自建 IntelligentBench 44.9→55.3（远超开源 Step1X-Edit 14.9）。消融证明"VAE+ViT 双特征"对复杂编辑至关重要（去掉 ViT token，Intelligent Edit 掉 16%）——**这正是 in-context 编辑能力的表征来源**：语义 ViT 上下文 + 交错数据训练。

**范式二小结与三问**：表征解耦是公约数；**理解反哺生成**在这条线被真正解决——靠"冻结强 MLLM 查询其知识"（[[metaqueries]]/[[blip3-o]] WISE 0.55/0.62）或"交错数据 + CoT 让知识涌现并迁移"（[[bagel]] 0.70）；**in-context 编辑**也在这条线成熟（[[bagel]] 的双特征条件、[[metaqueries]] 的重建迁移）。生成头则从 VQ-AR（[[janus]]）→ rectified flow（[[janusflow]]/[[bagel]]）→ CLIP-feature flow matching（[[blip3-o]]）→ 任意扩散 decoder（[[metaqueries]]）持续演化。

---

## 3. 范式三：扩散 + AR 混合（连续空间，去掉量化瓶颈）

**核心信条**：图像不必量化成离散 token——让**同一个 Transformer 既对文本做 next-token、又对连续图像 latent 做扩散/流匹配**，无量化信息损失。它与范式二的"双塔"区别在于：范式三强调"**单一骨干、单套权重、两种损失**"（more整合），范式二更强调"两路编码器/可热插拔 decoder"（more解耦）。两者在 [[bagel]]/[[show-o2]] 处其实已高度交融。

### 3.1 [[transfusion]]（Meta/Waymo/USC, 2024-08）— 范式三的奠基与对照实验

[[transfusion]] 用**单 Transformer、单套权重**联合损失 `L = L_LM + λ·L_DDPM`（λ=5），文本走 next-token、图像在 VAE latent 上走 DDPM 扩散，**从零联合预训练**。关键设计：**Transfusion Attention**——全序列 causal、但单图内 patch 间 bidirectional（消融显示这把 FID 从 61.3 降到 20.3）。它最有力的证据是与 [[chameleon]] 的**同算力对照**（同数据/架构/FLOPs，只差量化层）：达到 Chameleon 同等图像 FID 只需 **0.029 倍算力（34× 更省）**，连纯文本也更高效（~50–60% FLOPs）。7B/2T token 拿 GenEval **0.63**（超 DALL-E 2 0.52、SDXL 0.55）、COCO-FID 6.78，文本 Llama-Acc 66.1 与 Llama 1 持平。仅 8k 样例微调即解锁图像编辑。**这是"统一多模态该走连续扩散还是离散 AR"之争的决定性证据，直接成为 [[bagel]] 的先驱**。局限：仍用经典 DDPM（未上 flow matching）、256² 分辨率、无开源权重。

### 3.2 [[show-o2]](Show Lab/字节, 2025-06) — 连续潜空间 + AR/flow 双头 + 扩到视频

[[show-o2]] 是 [[show-o]] 的范式跃迁：从 MAGVIT-v2 离散 VQ 换到 **Wan2.1 的 3D 因果 VAE 连续潜空间**，生成从 masked-token 换成 **flow matching**，于是图像和视频可共用同一表征。核心创新 **dual-path 空间(-时间)融合**：语义层 S(·)（SigLIP 蒸馏，能从干净/加噪 latent 都抽语义，余弦相似度收敛到 ~0.9）+ projector P(·)（低层信息）拼接融合成单一连续表征，**一套表征同时满足理解要语义、生成要低层结构**；双输出头 LM head（NTP）+ Flow head（adaLN-Zero 时间调制）。它仅用 **66M 图文对**（远少于 Janus-Pro 144M、BAGEL 1600M、Transfusion 3.5B）就拿到 GenEval 1.5B/7B = 0.73/0.76、DPG **86.14**（超 SD3-Medium 84.08、Janus-Pro 84.19），并把统一建模首次扩到视频（仅 2B 总参 VBench 81.34，超 Emu3-8B 80.96）。最关键的工程卖点是**两阶段训练保住语言能力**（Table 13：两阶段配方下 7B 的 MMLU 70.73/GSM8K 75.28 几乎无损于原 Qwen2.5-7B；而"一阶段+RefinedWeb 共训"灾难性退化到 MMLU 28.43）。短板：文字渲染极弱（OneIG Text 0.002）。

### 3.3 [[lumina-mgpt-2-0]](上海AI Lab/Alpha-VLLM, 2025-04) — 纯 AR 的"反潮流"旗舰

值得注意，[[lumina-mgpt-2-0]] 严格说是**纯自回归**（非扩散混合），放在这里是因为它代表"混合范式喧嚣中坚持纯 AR 也能追平扩散"的对照点。它**从零训练、不依赖任何预训练权重**（2B/7B，挣脱 Chameleon 的架构/tokenizer/license 三重束缚），用重建质量最佳的 SBER-MoVQGAN（8×8 下采样，PSNR 22.77 vs Chameleon-VQ 18.63）。它的 in-context 编辑能力来自一个巧思——**dual-panel raster-scan**：把参考图放上半部 `<upper half>`、待生成图放下半部 `<lower half>`，靠 AR 光栅顺序天然把先生成区域当上下文，再用 system prompt 区分 T2I/编辑/可控/稠密预测/主体驱动五类任务，**所有任务统一成 text-to-image，无需额外模块或单独 SFT**。GenEval 0.80（=Janus-Pro，靠 thinking 改写 prompt + best-of-16 推理期 scaling）、DPG 84.30。代价是纯 AR 的慢——64×A100 训 4–5 周，768² 推理优化前 694s，靠 Speculative Jacobi Decoding（-72% 时间）+ 4bit 量化（显存 80→33.8GB）压到 304s。

**范式三小结与三问**：连续空间去掉量化瓶颈是公约数；表征上 [[transfusion]] 用单一 VAE latent，[[show-o2]] 用"语义层+projector"融合（兼顾理解），呈现向范式二靠拢的趋势；in-context 编辑靠注意力条件（[[transfusion]] 8k 微调、[[lumina-mgpt-2-0]] dual-panel）；理解反哺生成在 [[transfusion]] 仍弱、在 [[show-o2]] 主要靠"保语言"而非"知识迁移到画面"。

---

## 4. 从范式到产品：any-to-any 全模态

学术三范式收敛出一个产品形态：**把生成做成 LLM 的原生一等能力，输入输出任意模态组合**。这里分两条产品线——以**图像生成**为旗舰的（OpenAI/Google）和以**语音/音视频实时交互**为旗舰的（阿里 Qwen / 蚂蚁 Ming）。

### 4.1 图像旗舰：[[gpt-4o-native-image]] 与 [[gemini-2-0-flash-image]]

- **[[gpt-4o-native-image]]（OpenAI, 2024-05 演示 / 2025-03 上线）** 定义了"原生出图"范式：从"DALL-E 扩散+工具调用"变为"**自回归主干原生嵌入 + 扩散 decoder 末端渲染**"（system card 称其为 autoregressive，白板 pipeline 写 `tokens→transformer→diffusion→pixels`）。它把扩散范式的三个老大难一举解决——**可靠文本渲染、多轮对话式编辑一致性、一次摆放 10–20 个物体**（同期扩散系统通常只稳 5–8 个）。能力来源被官方点名是"对网络图像与文本的**联合分布训练**"（这正是 in-context 编辑/一致性的数据来源）。无标准学术指标（不发 FID/GenEval），但产品指标惊人：上线首周 >1.3 亿用户生成 >7 亿张图。架构/数据/算力全部闭源。
- **[[gemini-2-0-flash-image]]（Google DeepMind, 2025-03 公开实验版）** 同属生成端统一路线，主打**原生多模态输出**——同一对话 LLM 在一次 API 调用里**交错生成文本与图像**（`response_modalities=["Text","Image"]`），支持自然语言多轮对话式编辑。官方称内部基准"长文本渲染强于业界领先竞品"，但同样**不发任何 FID/GenEval**。它是 Google "Nano Banana"路线（→ [[gemini-2-5-flash-image-nano-banana]] → [[gemini-3-pro-image-nano-banana-pro]]）的公开起点。架构内部完全未披露。

> 这两者印证：**产品级"理解反哺生成 + in-context 编辑"靠的是 omni 架构 + 图文联合分布训练 + 强化后训练**，与学术界 [[metaqueries]]/[[bagel]] 殊途同归，只是不公开细节。

### 4.2 语音/音视频旗舰：Qwen-Omni 与 Ming-Omni

这条线的"any-to-any"重心不在出图，而在**同时感知图/文/音/视、并以流式同时输出文本与自然语音**——对标 GPT-4o 的实时对话形态。

- **[[qwen2-5-omni]]（阿里 Qwen, 2025-03）** 是开源全模态标杆，两大创新：**Thinker-Talker 双脑**（Thinker 出文本、Talker 出语音 token，Talker 直接吃 Thinker 高维隐表示+采样文本 token，"未读完文本先定调"）+ **TMRoPE 时间对齐位置编码**（音视频逐帧时间戳对齐，1 temporal ID=40ms，配 2 秒块的音视频时间交织）。7B 在 **OmniBench** 多模态融合上 Avg **56.13%**（远超 Gemini-1.5-Pro 42.91%）；语音生成 seed-tts-eval RL 后 WER test-zh/en/hard = **1.42/2.33/6.54%**（优于 MaskGCT、CosyVoice 2）；且**语音指令遵循逼近文本指令**（GSM8K* 85.4 vs Qwen2-Audio 18.4）。流式靠分块预填充 + 滑动窗口块注意力 DiT + 流式 BigVGAN。
- **[[qwen3-5-omni]]（阿里 Qwen, 2026-04）** 把旗舰扩到数千亿参/256k 上下文（>10h 音频/400s 720P 音视频），Thinker/Talker 双双换 **Hybrid-Attention MoE + Gated Delta Net**（降长上下文 KV-cache I/O）。两项标志创新：**ARIA（自适应率交错对齐）**——以"前缀累计语音:文本比 ≤ 全局比"的约束把双轨语音生成统一成单轨交错流，免 MFA/固定交错率；以及在 **TM-RoPE 之上叠加"文本时间戳字符串"**缓解长视频稀疏索引。Plus 在 215 项音频/音视频子任务取 SOTA：MMAU 82.2、VoiceBench 93.1、LibriSpeech clean/other WER 1.11/2.23（全面超 Gemini-3.1 Pro），SEED-TTS test-zh/en WER 0.99/1.26，且**文本/视觉不掉点**（与同尺寸 Qwen3.5-Plus 持平）。仅 API 开放、未开源权重。后训练用专家蒸馏→On-Policy Distillation（补"音频 query 回答质量 << 文本"）→交互对齐 RL。
- **[[ming-omni]]（蚂蚁 Inclusion AI, 2025-06）** 走 **MoE 中枢 + 模态专属 router** 路线：以 Ling MoE 为中枢（64 routing+2 shared experts，每 token 激活 6 个），给 T/V/A 三类 token 各配 router 缓解模态冲突；感知与生成**解耦**（先练理解，再**冻结 MLLM 主体**只训语音 decoder 和图像 DiT，避免生成污染理解——明确指出 Qwen2.5-Omni 式联合训练会让理解/生成难同时优化）。作者称其为"**首个在模态支持上对齐 GPT-4o 的开源模型**"。Ming-Lite-Omni 仅**激活 2.8B** 即图像理解比肩 Qwen2.5-VL-7B（均值 71.4 vs 71.5）、语音理解超 Qwen2.5-Omni/Kimi-Audio、图像生成 GenEval 0.64/**FID 4.85**（号称当时新 SOTA）。语音侧对离散 token 再做 BPE（50Hz→~32Hz、长度 -36%、可逆无损、还改善韵律）。

**any-to-any 小结与三问**：产品端把三问统一收进"omni 架构"——理解反哺生成靠图文/音视联合分布训练；表征解耦在 [[ming-omni]] 体现为"冻结 MLLM + 轻量桥接生成"（与 [[metaqueries]] 同构），在 omni 语音侧体现为 Thinker/Talker 分轨；in-context 一致性靠对话上下文与交错输出。学术界的"双塔解耦 + 冻结 MLLM 接生成头"范式，正是产品级 omni 的工程公约数。

---

## 5. 横向收敛：三问的统一答案

| 问题 | 范式一（离散 AR） | 范式二（解耦双塔） | 范式三（扩散+AR 混合） | 产品 any-to-any |
|---|---|---|---|---|
| **理解反哺生成（WISE 等）** | 弱：[[emu3]] 0.39 | 强：[[metaqueries]] 0.55、[[blip3-o]] 0.62、[[bagel]] 0.70(CoT) | 中：[[transfusion]] 弱、[[show-o2]] 靠保语言 | 强（图文联合分布训练，闭源不报数） |
| **视觉表征解耦** | 单一离散 token（[[show-o]]/[[x-omni]] 渐向语义 tokenizer 妥协） | 典范：SigLIP/CLIP 理解 + VQ/VAE 生成（[[janus]] 消融奠基） | 趋势靠拢：[[show-o2]] 语义层+projector 融合 | [[ming-omni]] 冻结 MLLM+桥接；omni 语音 Thinker/Talker 分轨 |
| **in-context 编辑来源** | 较弱（[[x-omni]] 靠 RL+长文本） | 双特征条件/重建迁移（[[bagel]]/[[metaqueries]]） | 注意力条件（[[transfusion]] 8k 微调、[[lumina-mgpt-2-0]] dual-panel） | 图文联合分布 + 对话上下文（[[gpt-4o-native-image]]/[[gemini-2-0-flash-image]]） |

**三条贯穿性结论**：

1. **"统一"≠"知识迁移"**。把两个任务塞进一个网络（范式一、早期范式二的 Janus 系列）并不会自动让理解反哺生成（WISE 普遍 ≤0.39）。真正的反哺要么靠**冻结强 MLLM 并查询其知识**（[[metaqueries]]/[[blip3-o]]/[[ming-omni]]），要么靠**交错数据 + CoT 让能力涌现并迁移**（[[bagel]] 0.70）。

2. **视觉表征解耦是不可逆的共识**。从 [[janus]] 的消融把"共享单编码器伤理解"量化坐实开始，连原本走单一表征的范式一（[[show-o]]→[[x-omni]]）和范式三（[[transfusion]]→[[show-o2]]）都在向"理解要语义、生成要低层"的双特征/语义 tokenizer 靠拢。差异只在于"两路独立编码器"（Janus/BAGEL）还是"一套表征内融语义+低层"（Show-o2）。

3. **生成头的范式之争（离散 AR vs 扩散/流）尚未定论，但天平偏向连续**。[[transfusion]] 的 34× 算力对照是连续派的决定性证据，rectified flow（[[janusflow]]/[[bagel]]/[[show-o2]]）/CLIP-feature flow matching（[[blip3-o]]）成为生成头主流；但 [[x-omni]] 用 RL 证明**纯离散 AR 配合语义 tokenizer + 分布对齐仍可达 SOTA**（DPG 87.65、长文本渲染碾压），[[lumina-mgpt-2-0]] 证明纯 AR 也能追平扩散——离散路线靠 RL/推理期 scaling 续命，并未出局。

---

## 附：本章引用的单工作页（[[slug]] 内链）

范式一：[[chameleon]] · [[chameleon-cm3leon]] · [[emu3]] · [[show-o]] · [[x-omni]]
范式二：[[janus]] · [[janusflow]] · [[janus-pro]] · [[metaqueries]] · [[blip3-o]] · [[bagel]]
范式三：[[transfusion]] · [[show-o2]] · [[lumina-mgpt-2-0]]
产品 any-to-any：[[gpt-4o-native-image]] · [[gemini-2-0-flash-image]] · [[gemini-2-5-flash-image-nano-banana]] · [[gemini-3-pro-image-nano-banana-pro]] · [[qwen2-5-omni]] · [[qwen3-5-omni]] · [[ming-omni]]
相关：[[rectified-flow]] · [[stable-diffusion-3]] · [[flux-1]] · [[vila-u]] · [[emu3-5]]
