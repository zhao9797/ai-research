---
title: "Ovis-U1: Unified Understanding, Generation and Editing"
org: "阿里巴巴 (Alibaba Group, Ovis Team)"
country: China
date: "2025-06"
type: tech-report
category: unified
tags: [unified, mllm, t2i, edit, mmdit, flow-matching, qwen3, ovis, open-source]
url: "https://arxiv.org/abs/2506.23044"
arxiv: "https://arxiv.org/abs/2506.23044"
pdf_url: "https://arxiv.org/pdf/2506.23044"
github_url: "https://github.com/AIDC-AI/Ovis-U1"
hf_url: "https://huggingface.co/AIDC-AI/Ovis-U1-3B"
modelscope_url: ""
project_url: "https://huggingface.co/spaces/AIDC-AI/Ovis-U1-3B"
downloaded: [arxiv-2506.23044.pdf, ovis-u1--hf-readme.md, ovis-u1--github-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Ovis-U1 是阿里 Ovis 团队 2025 年 6 月开源的 **3B（实际 3.6B）统一多模态模型**，单模型同时做多模态理解、文生图、指令图像编辑；核心创新是在 Ovis「结构化视觉嵌入对齐」之上接一个**从零训练的 1B MMDiT diffusion 视觉解码器 + 双向 token refiner**，并**从纯语言模型（Qwen3-1.7B）而非冻结的 MLLM 出发做统一训练**。最亮结果：OpenCompass 理解 69.6（超 Ristretto-3B/SAIL-VL-1.5-2B 等同级模型）、GenEval 0.89 / DPG-Bench 83.72（文生图）、ImgEdit-Bench 4.00 / GEdit-Bench-EN 6.42（编辑），三任务在 3B 量级都接近或领先同期开源 SOTA。

## 背景与定位
GPT-4o 的原生图像生成证明了「理解 + 生成」统一模型的价值，并暗示**统一训练能反哺理解能力**。Ovis-U1 要回答两个问题：(1) 如何给一个多模态理解模型装上图像生成能力（需要设计能与 MLLM 协同的视觉解码器）；(2) 如何在理解与生成任务上**有效联合训练**一个统一模型。

它在统一模型谱系中的定位：
- 相对 **OmniGen / OmniGen2 / BAGEL / UniWorld-V1 / BLIP3-o / Janus-Pro / Emu3** 等同期统一模型，Ovis-U1 在 3B 量级用更小的生成端（1B 解码器）取得有竞争力甚至领先的成绩。
- 与许多前作的关键区别：很多统一模型**冻结预训练 MLLM**（如 BLIP3-o、UniWorld-V1）或直接用 Qwen-VL 当 backbone 保持不动，导致理解能力往往**低于其 MLLM 底座**（论文点名 Ming-Lite-Uni 用 Qwen2.5-VL-7B 却理解更差）。Ovis-U1 反其道——**从语言模型 Qwen3-1.7B 起步**、在理解+生成数据上联合训练，理解分数反而比不做统一训练的 Ovis 基线**高 1.14 分**。
- 架构上承接 [[ovis]]（结构化嵌入对齐 MLLM）做理解端，生成端借鉴 [[flux]] / [[stable-diffusion-3-mmdit]]（MMDiT + rectified flow）。编辑端的 in-context 条件注入借鉴 FLUX.1 Kontext / FLUX.1 Redux，CFG 双条件借鉴 InstructPix2Pix。

## 模型架构
整体 = 共享 MLLM + 视觉编码器/adapter（理解端）+ 视觉解码器/refiner（生成端）+ 文本 detokenizer。各模块参数量（Table 1，总 **3644M ≈ 3.64B**）：

| 模块 | 参数(M) | 预训练来源 |
|---|---|---|
| LLM | 1720 | Qwen/Qwen3-1.7B |
| Vision Decoder | 1046 | 随机初始化（从零训） |
| Visual Encoder | 578 | apple/aimv2-large-patch14-448 |
| Adapter | 135 | — |
| VAE | 84 | madebyollin/sdxl-vae-fp16-fix（冻结） |
| Refiner | 81 | — |

注意参数口径：Table 1 合计 3.64B；正文主结果处又写「仅 3.34B 参数」，其中真正服务**理解任务的约 2B**（LLM 1.72B + 视觉编码器 + adapter），生成端是那颗 1B 解码器。

- **LLM & 文本 tokenizer**：用 **Qwen3-1.7B**。关键设计——不像别人拿现成 MLLM（如 Qwen-VL）当固定 backbone，而是**从纯 LLM 初始化**，用视觉理解+生成数据一起训，理解/生成协同增益。
- **视觉编码器 & adapter**：编码器初始化自 **AIMv2-large-patch14-448**，改造成**原生任意分辨率**（不做 sub-image 切分）：固定位置嵌入插值 + 2D RoPE 增强空间感知；用变长序列注意力（FlashAttention）+ NaViT token packing 高效处理混分辨率 batch。Adapter 沿用 Ovis 的**概率化 tokenization**——pixel shuffle 空间压缩 → 线性头 + softmax 把特征变成「视觉词表」上的概率分布，最终送入 LLM 的嵌入是基于该分布对一张可学习嵌入表做的加权平均（即 Ovis 的结构化嵌入对齐核心思想）。
- **视觉解码器 & VAE**：diffusion transformer 当解码器。仿 **FLUX**，用 **MMDiT + RoPE** 作 backbone、**flow matching** 为训练目标。把 FLUX 的 57 层/24 头**砍到 27 层/16 头**得到 **1B 解码器**，随机初始化**从零训练**。因解码器容量有限，直接用 **SDXL 的 4 通道 VAE 并在统一训练中冻结**。条件注入两路：(a) 仿 FLUX.1 Redux，把**视觉语义嵌入**与文本嵌入拼接作语义条件；(b) 仿 FLUX.1 Kontext，把**上下文图像**经 VAE encoder 编成 latent token（含细节信息），这些「视觉细节嵌入」与噪声图像 token 一起进解码器 visual stream。
- **Refiner（双向 token refiner，核心创新）**：在视觉嵌入与文本嵌入间做交互。堆 **2 层 transformer block + modulation**（仿 HunyuanVideo / Ma et al.）。两个巧思：
  - **跨层特征拼接**——把 LLM **最后一层**与**倒数第二层**特征拼起来送进 refiner（不同层捕获不同粒度的图文信息），生成更好的条件 guidance。
  - **clip-free 全局信息**——传统 FLUX 引入 CLIP 抓全局特征，Ovis-U1 改用**可学习 [CLS] token**：把 [CLS] 与 LLM 嵌入拼接送进 refiner 交互来聚合全局信息，从而**去掉 CLIP**。

## 数据
三类多模态数据（仅披露来源与处理 pipeline，**未披露各部分确切规模/配比数字**）：

- **多模态理解数据**：公开集 **COYO、Wukong、Laion、ShareGPT4V、CC3M** + 自研数据；自建预处理 pipeline 做噪声过滤、caption 质量增强、数据配比调整。
- **文生图数据**：取自 **Laion5B**（先筛**美学分 > 6**）+ **JourneyDB**；用 **Qwen 模型为每张选中图重新生成详细描述（re-caption）**，得到自建 **Laion-aes6** 数据集。
- **图+文→图（编辑/可控生成）数据**，四子类：
  - 图像编辑：**OmniEdit、UltraEdit、SeedEdit**。
  - 参考图驱动生成：主体驱动用 **Subjects200K、SynCD**；风格驱动用 **StyleBooth**。
  - 像素级可控生成：canny→图、depth→图、inpainting、outpainting，来自 **MultiGen-20M**。
  - 自研数据：风格驱动、内容移除、风格翻译、去噪/去模糊、上色、文字渲染等。

各阶段消融用的数据量级有提及（refiner 消融用 ~10M / ~50M 文生图对），但**整体训练数据总量、token 数、各任务样本数未披露**。

## 训练方法
**六阶段渐进式统一训练**（Table 2；雪花=冻结，火焰=可训）。底座是「预训练 LLM + 视觉编码器」，Ovis 原本 4 段（adapter 预训练→视觉编码器对齐→理解学习→DPO），生成端再加阶段：

| Stage | 可训参数 | 任务 | 步数(K) | Batch | LR |
|---|---|---|---|---|---|
| 0 视觉解码器预训练 | refiner + Decoder | T2I | 500 | 1024 | 1e-4 |
| 1 adapter 预训练 | adapter | 理解+T2I+编辑 | 1.51 | 8192 | 5e-4 |
| 2 视觉编码器对齐 | Encoder + adapter | 理解+T2I+编辑 | 2.63 | 8192 | 1e-4 |
| 3 理解学习 | Encoder + adapter + LLM | 理解 | 23 | 2240 | 5e-5 |
| 4 生成学习 | refiner + Decoder | T2I | 275 | 256 | 5e-5 |
| 5 生成微调 | refiner + Decoder | T2I + 编辑 | 325 | 256 | 5e-5 |

- **Stage 0**：1B diffusion transformer 随机初始化**从零训**，用文生图数据让解码器+refiner 学会从 LLM 嵌入生图。
- **Stage 1–2**：adapter 与视觉编码器对齐图文嵌入；与 Ovis 不同，**这两段就同时用理解+文生图+编辑三类任务**——生成任务反过来帮助跨模态嵌入对齐（这是「统一训练增强理解」的来源）。
- **Stage 3**：理解学习（同 Ovis），训视觉编码器+adapter+LLM；**训完冻结这些参数以保住理解能力**。
- **Stage 4**：因 Stage 3 动过 LLM，重新训 refiner+解码器去对齐优化后的文本/图像嵌入；文生图相比 Stage 0 有提升（因 1–3 段已把文本嵌入打磨得更对齐图像嵌入）。
- **Stage 5**：文生图 + 图像编辑数据一起微调解码器。论文消融：**加入编辑数据使 DPG-Bench 文生图分再涨 0.77**（编辑数据反哺文生图）。

训练目标：理解端 next-token；生成端 **flow matching（rectified flow）**。编辑推理用 **双条件 CFG**（InstructPix2Pix 式）：CFG_img 越高越保留原图细节、CFG_txt 越高越贴合编辑指令；论文实测对 CFG 取值鲁棒（ImgEdit / GEdit 波动 < 0.2），不同 benchmark 最优 CFG 不同（如 ImgEdit 最优 CFG_img=2、CFG_txt=7.5 得 4.13，高于主表统一 CFG 的 4.00）。

**显式说明缺 RL 阶段**：结论里坦承「Ovis-U1 目前缺少 RL，而 RL 对大模型优化已被证明关键」，与人类偏好对齐是 open question——即**没有 RLHF/DPO 风格的偏好对齐用于生成端**（Ovis 原 pipeline 的 DPO 属理解侧）。无步数蒸馏/consistency/LCM 等加速训练。

## Infra（训练 / 推理工程）
- **未披露**算力规模/GPU 数/GPU·时/总训练时长/并行分布式策略/吞吐。
- 仅可从超参推断：Stage 1–2 batch size 高达 8192、Stage 0 batch 1024 步数 500K——属较大规模训练，但无机器配置披露。
- 工程组件：变长序列注意力 + **FlashAttention/FlashAttention-2**、**NaViT token packing**（混分辨率高效 batch）。
- 推理：文生图默认 1024×1024、**50 步**、txt_cfg=5；编辑默认 50 步、img_cfg=1.5、txt_cfg=6（来自官方推理脚本）。环境 Python 3.10 / Torch 2.4.0 / Transformers 4.51.3 / DeepSpeed 0.15.4。**无量化/缓存/步数蒸馏等推理加速披露**；部署形态：开源权重 + HF Space demo + transformers 加载。

## 评测 benchmark（把效果讲清楚）
对比对象主要为 GPT-4o 及开源统一模型 Janus-Pro/Emu3/BLIP3-o/BAGEL/UniWorld-V1/OmniGen/OmniGen2；多数基线数字引自 OmniGen2，OmniGen2 理解为作者自测（‡）。GenEval 用**原始 prompt**（不重写）。

**多模态理解（OpenCompass，8 benchmark 均值）**——Ovis-U1 **Avg 69.6**，在 ~3B 档**全面超越** InternVL2.5-2B(59.9)/SAIL-VL-2B(61)/InternVL3-2B(61.1)/Qwen2.5-VL-3B(64.5)/Ovis2-2B(65.2)/SAIL-VL-1.5-2B(67)/Ristretto-3B(67.7)。分项：MMB 77.8、MMStar 61.3、MMMU 51.1、MathVista 69.4、Hallusion 56.3、AI2D 85.6、OCRBench 88.3、MMVet 66.7。（GPT-4o Avg 75.4 仍领先。）

**文生图**：
- **GenEval Overall 0.89**（原始 prompt），超 GPT-4o(0.84) 及所有列出开源模型（BAGEL 0.82、OmniGen2 0.80、重写后 OmniGen2 0.86）。分项：Single 0.98 / Two 0.98 / Counting 0.90 / Colors 0.92 / Position 0.79 / Attr 0.75，其中 Two object、Counting、Position 列**最佳**。
- **DPG-Bench Overall 83.72**，高于 OmniGen2(83.57)/UniWorld-V1(81.38)/OmniGen(81.16)，略低于 BAGEL(85.07)；Relation 项 93.35 为该表最佳。
- CLIPScore 用于消融（DALL-E3 式，前 1K COCO prompt），主表未单列最终值。

**图像编辑**：
- **ImgEdit-Bench Overall 4.00**（811 对，GPT 评分），超所有开源对手（OmniGen2 3.44、UniWorld-V1 3.26、BAGEL 3.2），逼近 GPT-4o(4.2)；Extract 2.98、Replace 4.45、Remove 4.06 为该表最佳。
- **GEdit-Bench-EN Avg 6.420**（606 对），与 OmniGen2 持平（Table 3 记两者同为 6.42），但**略低于 BAGEL(6.519)**（即未超 BAGEL；论文也未声称超 BAGEL）；Background Change 7.486 为该表最佳；弱项 Motion Change(4.790)、Text Modification(4.482)。GPT-4o(7.534)、Doubao(6.754) 仍领先。注：GEdit-EN 基线引自 step1x-edit 排行榜的早期版本。

**关键消融**：
1. **统一训练增强理解**（Table 10）：相对不做统一训练的 Ovis 基线，Avg 从 63.33→64.47（**+1.14**），验证 Stage 1–2 用生成任务帮视觉编码器对齐的价值。
2. **统一训练增强生成**（Table 11/12）：生成能力随阶段递进提升（Stage1→4→5）；Stage 5 引入编辑数据使 DPG-Bench **+0.77**。
3. **refiner 设计**（Table 9，~10M/~50M 数据）：T5+CLIP 基线最强但需 CLIP；用 LLM 时**单用最后一层特征会掉点**（V1: DPG 80.97），**拼接倒二+最后层**恢复到基线水平（V2: 81.48），换 image-text 对齐过的 Ovis2 特征再升（V3 DPG 82.37）；clip-free 方案里 **[CLS] token（V7）在 50M 数据上 DPG 达 83.81**，超基线 82.97——支撑「去 CLIP 用 [CLS]」可行，但作者指出 clip-free 仍需更大数据才能充分发挥。

## 创新点与影响
**核心贡献**：
1. **从 LLM 起步的统一训练**：不冻结/不直接套用现成 MLLM，而从 Qwen3-1.7B 联合训理解+生成，使理解分**高于**不做统一训练的基线——挑战「统一模型理解必弱于其 MLLM 底座」的普遍现象。
2. **双向 token refiner + clip-free 条件设计**：跨层（倒二+最后层）特征拼接 + 可学习 [CLS] token 替代 CLIP，作为 LLM→diffusion 解码器的条件桥梁。
3. **小生成端高效统一**：仅 1B 从零训的 MMDiT 解码器 + 冻结 SDXL VAE，在 3B 量级把理解/文生图/编辑三任务做到接近或领先同期开源 SOTA，开源（Apache-2.0）+ 权重 + Space demo。
4. **统一训练的双向增益实证**：理解↔生成、编辑↔文生图 互相反哺的量化消融。

**影响**：作为 Ovis unified 系列首版，给「小参数量统一模型」提供了一条可复现路线（FLUX 式 MMDiT + Ovis 结构化嵌入 + 多阶段统一训练）。后续 Ovis-Image-7B（2025/11 发布）延续该线。

**已知局限**（作者自陈 + 数据可见）：
- **缺 RL/偏好对齐**，是明确的下一步。
- 小生成端（1B）易有 artifact/幻觉，作者计划扩参数。
- 编辑弱项：Motion Change、Text Modification 明显落后 GPT-4o/Doubao。
- 训练数据总量、配比、算力 infra 均**未披露**，复现需自行配数据与算力。
- 视觉编码器/解码器未针对编辑做细节保真专门设计（计划改进 encoder-decoder 结构保留输入细节）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2506.23044
- arxiv_pdf: https://arxiv.org/pdf/2506.23044
- hf_model: https://huggingface.co/AIDC-AI/Ovis-U1-3B
- github: https://github.com/AIDC-AI/Ovis-U1
- hf_space (demo): https://huggingface.co/spaces/AIDC-AI/Ovis-U1-3B

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2506.23044.pdf
- ../../../sources/omni/2025/ovis-u1--hf-readme.md
- ../../../sources/omni/2025/ovis-u1--github-readme.md
