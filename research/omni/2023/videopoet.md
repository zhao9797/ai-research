---
title: "VideoPoet: A Large Language Model for Zero-Shot Video Generation"
org: Google
country: US
date: "2023-12"
type: paper
category: video
tags: [video, autoregressive, llm, discrete-token, multimodal, text-to-video, image-to-video, audio, magvit-v2, zero-shot]
url: "https://arxiv.org/abs/2312.14125"
arxiv: "https://arxiv.org/abs/2312.14125"
pdf_url: "https://arxiv.org/pdf/2312.14125"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://sites.research.google/videopoet/"
downloaded: [arxiv-2312.14125.pdf, videopoet--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
VideoPoet 是 Google 提出的**纯自回归 decoder-only LLM 视频生成模型**：把图像/视频/音频全部用离散 token 表示，套用 LLM 的"大规模多任务预训练 + 任务自适应"范式，在**一个模型一个词表**里统一了文生视频、图生视频、视频续写、修补/外扩、风格化、视频生音频等任务，并展示出 zero-shot 任务链式组合能力。最大卖点是**高保真大运动**——8B 模型在 MSR-VTT 上 CLIPSIM 0.305 / FVD 213、UCF-101 FVD 355，人评中除并发工作 Lumiere 外在 motion interestingness / realism 等多数维度优于 Show-1、VideoCrafter、Pika、Gen2 等扩散基线。

## 背景与定位
2023 年视频生成几乎被扩散模型垄断（Make-A-Video、Video LDM、ModelScopeT2V、Show-1、Pika、Gen2、Lumiere 等），它们多由文生图扩散模型派生，靠推理 trick、结构改造、adapter 层逐个堆叠新任务/新模态，**并非端到端统一训练**。语言模型路线（[[parti]]/DALL-E 式自回归、[[muse]]/MAGVIT 式掩码生成）虽在文生图上验证可行，但在文生视频上一直被认为质量不及扩散（Phenaki、[[cogvideo]] 等）。

VideoPoet 的论点是：**LLM 范式真正的价值不在"文生视频单任务"，而在"大规模多任务预训练学一个 foundation"**——正如 GPT-3/PaLM 通过多样任务获得 zero/few-shot 泛化。作者由此把视频生成完全纳入 LLM 工具链（复用 LLM 的 scaling recipe、训练/推理基础设施、硬件优化），并用一个 transformer + 一个统一词表承载所有任务，与扩散模型"改架构 + 加 adapter"形成鲜明对照。它是 2023 年末**自回归视频生成的代表作**，技术血脉上承 [[magvit]]/MAGVIT-v2 tokenizer、Phenaki、Parti，是后续 Loong、Emu3、统一多模态自回归路线的重要先声。

## 模型架构
三大组件：(1) 模态专用 tokenizer，(2) decoder-only LLM 主干，(3) 非自回归超分模块。

- **视觉 tokenizer：MAGVIT-v2**（与图像、视频共用）。把 17 帧、2.125 秒、8fps、128×128 的视频编码量化为 latent 形状 (5,16,16)，flatten 成 **1280 个 token**；竖屏 128×224 则为 (5,28,16)=2240 token。词表 2^18=262,144。强制**因果时序依赖**（causal temporal）以便长视频续写。图像视为 1 帧视频，单帧固定编码为 (1,16,16)=256 token，使图像/视频共享同一词表。inpaint/outpaint 用 **COMMIT 编码**（来自 MAGVIT/MAGVIT-v2 体系）。
- **音频 tokenizer：SoundStream**。2.125 秒音频 → 106 个 latent 帧，4 级 RVQ，每级独立 1024 码，合计音频词表 **4096**。RVQ 预测采取"由低到高级别顺序预测"（略优于同时预测所有级别）。
- **文本编码：冻结的 T5-XL encoder**（非从头学文本 token）。文本嵌入经线性层投到 transformer 嵌入空间，作为前缀注入。最多 64 个文本 token。
- **统一词表 ≈ 300,000**：前 256 为特殊 token / 任务前缀；接 262,144 视觉码；再 4096 音频码；外加少量英文文本词表。特殊 token（见论文 Table 4）如 `<task> <res> <bov_o> <eov_o> <source>` 等显式标注任务、分辨率、各模态输入/输出边界。
- **LLM 主干**：**prefix LM + decoder-only** 架构。输入端（双向 prefix：文本嵌入 + 视觉 token + 音频 token）做双向注意力，输出端（自回归生成视觉/音频 token）做因果注意力；通过不同的 input→output token 模式（task prompt）控制模型执行哪种任务。规模有 300M / 1B / 8B 三档。
- **超分模块（非自回归）**：自定义**多轴（multi-axis）windowed local-attention transformer**，在 token 空间对 LLM 输出做 2×空间超分级联两级（224×128 → 448×256 → 896×512）。每个 block 三层分别沿空间竖直 / 空间水平 / 时间轴做局部窗口自注意力，并 cross-attend 到 T5-XL 文本嵌入与低分 token。为应对 262,144 大词表，采用 **token factorization (k=2)**，把一个 262,144 类问题拆成两个 512 类。第一级用 1B 模型、第二级用 500M 模型。

为什么不直接自回归生高分辨率：17×896×512 视频 tokenize 后达 35,840 token，自回归采样不现实，故把高分留给非自回归掩码超分。

## 数据
- **总量**：约 **10 亿图文对** + **约 2.7 亿视频**（其中约 1 亿带配对文本，约 5000 万用于高质量微调；约 1.7 亿带配对音频），来自公开互联网及其他来源，**跨所有模态约 2 万亿 token**。
- **过滤/采样**：过滤掉恶劣内容；为提升上下文与人口统计多样性做了重采样。**有意排除含版权内容的来源（如 LAION）**，训练偏自然美学——作者承认这也导致静态画面的逐帧美学不及最佳扩散基线。
- **关键设计**：方法允许**同一视频用于多个训练任务、且不要求配对文本**（unpaired video 也能用于 SSL 任务），从而能用海量纯视频训练，大幅降低对视频-文本配对数据的需求。论文 Table 1 的 "SSL" 行显示纯自监督显著掉点，说明文本配对数据仍不可或缺。
- **图像 vs 视频采样**：发现均匀采样次优（图像帮助物体理解但无运动）。**两阶段采样**：前 25% 迭代图像 90% / 视频 10%，之后切换为视频 90% / 图像 10%。
- **高质量微调子集**：约 5000 万内部视频，含较简单的片段，未人工挑选；用于提升 T2V/I2V 质量、缓解"解码坍缩"（重复 token）、允许更高的 CFG scale。

## 训练方法
- **目标函数**：标准 **next-token 自回归交叉熵**（非 diffusion、非 flow matching）；超分模块用 **MAGVIT 掩码建模目标**（masked-token，含 token factorization k=2）。
- **两阶段范式（照搬 LLM）**：(1) 预训练——在多任务混合上做自回归预测，得到通用 foundation；(2) 任务自适应——在高质量子集上微调以提升特定任务（T2V/I2V）或适配新任务。
- **预训练任务混合**：无条件生成、文生视频(T2V)、文生图(T2I)、未来帧预测(FP)、图生视频(I2V)、视频修补/外扩(painting)、视频风格化（以 text+光流+深度为条件重建，光流用 RAFT、深度用 MIDAS，沿通道拼接后同样用 MAGVIT-v2 tokenize 无需重训）、音生视频、视频生音频(V2A)、音视频续写(AVCont)。同一 `<task>` 可对应多种输入变体（T2V/I2V/无条件共用一个 `<task>`）。
- **多任务训练 trick——Alternating Gradient Descent (AGD)**：按序列长度把任务分组，每步交替采一组，使**padding 比例接近 0%**（优于 packing），高效处理首帧、长视频等差异巨大的序列长度。
- **"把图像当视频"**：T2I 预训练时省略 `<eos>`/`<eov_o>`，使 token 可连续生成，模糊图像/视频边界、增强跨模态信息共享，提升首帧质量、减少后续帧伪影。
- **超分训练**：在 64M 高质量文本-视频对上用掩码目标训练；LR 序列来自 bicubic 下采后 tokenize，并在离散 latent 空间做 noise augmentation、10% 样本独立丢弃 LR 条件与文本嵌入，以缓解真实/生成分布失配。
- **推理 trick**：base 自回归采样；超分非自回归 24 步/级 + CFG（文本 4.0/8.0、LR 条件 1.0/2.0）；系统级用固定负面提示 + 轻量 prompt 改写（追加 "highly detailed, cinematic, arc shot, high contrast, soft lighting, 8k"）。
- **关键超参（300M task-analysis 配置）**：lr=1e-3、batch 1024、训练 300k 步。

## Infra（训练 / 推理工程）
- **训练框架**：完全复用 LLM 基础设施（论文卖点之一，未披露具体并行/混合精度配置）。AGD 多任务调度降低 padding 开销。
- **算力披露有限**：未报告总 GPU/TPU·时数。仅说 8B "utilized significantly more compute"。
- **scaling 数据点**：300M / 1B / 8B 三档分别在 **10 / 37 / 58 billion 视觉+音频 token** 上训练；log-log 曲线显示视频 FVD、音频 FAD 随模型与数据规模一致下降。
- **推理 runtime**（**TPUv5p，4 chip**，batch 4，生成 17 帧 @8fps）：base 模型 34s，detokenizer（token→像素）1.3s，超分 6.8s，**摊销约 5 秒计算/每秒输出视频**。作者强调模型**未做任何推理优化**，标准 LLM 加速技术均可套用。

## 评测 benchmark（把效果讲清楚）
全部为 **zero-shot**（模型未在评测集训练集上训练）。

**零样本文生视频（Table 2，VideoPoet 为 8B）**
- MSR-VTT：**CLIPSIM 0.3049**（pretrain）→ **0.3123**（task-adapt），**FVD 213**（pretrain）。对比 Show-1 0.3072、Make-A-Video 0.3049/FVD 367、VideoFactory 0.3049/FVD 410、CogVideo(EN) 0.2631/FVD 1294。
- UCF-101：**FVD 355、IS 38.44**（pretrain）。对比 Show-1 FVD 394/IS 35.42、Make-A-Video FVD 367/IS 33.00。
- VideoPoet 在 CLIPSIM 与 FVD 上整体居前列；pretrain foundation 未微调即有竞争力，T2V 微调进一步提升 CLIPSIM。

**8B 全任务（Table 1 "ALL (8B)" 行）**：MSR-VTT CLIPSIM **0.305** / UCF-101 FVD **355** / K600 帧预测 FVD **687** / SSv2 inpainting FVD **4.7** / outpainting FVD **13.76**。
（注：K600 给前 5 帧预测后 11 帧，16 帧 @128×128；SSv2 中心 inpaint/outpaint，按 MAGVIT 协议评测。）

**预训练任务消融（300M，Table 1）**：把所有任务（T2I+T2V+Uncond+FP+Painting+AVCont）一起训，平均表现最好；纯 SSL（无文本配对）显著掉点，证明文本配对数据必要；多任务相比单任务在单项上略降，作者归因为每任务训练步数不足。

**人评（T2V，task-adapt 版，7 名 rater，~250 prompt，5 维：text fidelity / video quality / motion interestingness / motion realism / temporal consistency）**：与 Phenaki、Show-1、VideoCrafter、Runway(Gen2)、Pika、WALT、Lumiere 对比。VideoPoet 在 **motion interestingness / realism** 上大幅领先（如对 Show-1 motion interestingness 偏好率显著占优）；**Lumiere（并发、扩散）是唯一在 Video Quality 上胜过 VideoPoet 的模型**。

**视频风格化（Table 3，对比 Control-A-Video[depth]，DAVIS 2016 20 视频×2 prompt）**：VideoPoet CLIPSIM **0.3417** vs Control-A-Video 0.3246；人评 text fidelity 70% / video quality 77.5% 偏好 VideoPoet。

**音频**：FAD 随规模下降（图 8b，具体数值以曲线形式给出，正文未列表化精确数字——**未报告**逐模型 FAD 表）。

**其他评测细节**：MSR-VTT 用全部 59,794 caption 算 CLIP（ViT-B/16；ViT-B/32 下为 30.01），FVD 在 2048 视频×20 repeat 上用 I3D(K400)；UCF-101 采 10,000 视频；SSv2 用 50,000 样本、K600 用 50,000×4。

## 创新点与影响
**核心贡献**
1. 证明**纯自回归 LLM（离散 token）可达 SOTA 级视频质量**，尤其在大幅度、复杂运动上优于同期扩散基线——挑战"扩散垄断视频生成"的主流认知。
2. **单模型 + 单词表统一多任务多模态**：T2V/I2V/续写/inpaint/outpaint/风格化/V2A/AVCont 全在一个 transformer 内，靠 task prompt 切换，而非扩散派的 adapter 堆叠；并涌现 **zero-shot 任务链式组合**（如先 I2V 再风格化、先 outpaint 再 stylize），以及未训练即具备的 3D 视角旋转、相机运动控制等能力。
3. **token 空间非自回归多轴超分** + token factorization，解决高分辨率自回归序列爆炸问题。
4. 提出可复现的零样本 T2V 评测设置规范（补齐前人缺失细节）。

**影响**：成为自回归/离散 token 视频生成路线的标杆，验证"复用 LLM scaling 与基础设施"的可行性；推动后续统一多模态自回归生成（Emu3、Loong、各类 any-to-any token 模型）的探索。

**已知局限**（作者自陈）
- 视觉保真度受 MAGVIT-v2 **tokenizer 重建上界**钳制（量化压缩造成的信息损失是天花板）。
- 静态场景逐帧美学不及最佳扩散基线，部分源于**排除 LAION 等版权数据、偏自然美学**的数据选择。
- 大运动下的**小物体 / 细粒度细节**仍难，token 建模易丢失。
- 推理偏慢（约 5s 计算/秒视频，未优化），自回归长序列代价高。
- 公平性：默认 prompt 输出分布偏 "Young Adults/Male/Light Skin Tone"，但可通过改 prompt 调节。
- **未开源**（无 GitHub/HF/权重发布），为 Google 内部研究模型；生成视频使用数字水印以便溯源。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2312.14125
- arxiv_pdf: https://arxiv.org/pdf/2312.14125
- blog (项目页): https://sites.research.google/videopoet/
- 会议: ICML 2024（PMLR 235）；v4 2024-06-04

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2312.14125.pdf
- ../../../sources/omni/2023/videopoet--blog.md
