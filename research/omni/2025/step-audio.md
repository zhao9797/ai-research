---
title: "Step-Audio: Unified Understanding and Generation in Intelligent Speech Interaction"
org: "阶跃星辰 StepFun"
country: China
date: "2025-02"
type: tech-report
category: audio
tags: [speech, audio-llm, voice-chat, tts, dual-codebook, rlhf, open-source, multimodal]
url: https://arxiv.org/abs/2502.11946
arxiv: https://arxiv.org/abs/2502.11946
pdf_url: https://arxiv.org/pdf/2502.11946
github_url: https://github.com/stepfun-ai/Step-Audio
hf_url: https://huggingface.co/stepfun-ai/Step-Audio-Chat
modelscope_url: https://modelscope.cn/models/stepfun-ai/Step-Audio-Chat
project_url: https://yuewen.cn
downloaded: [arxiv-2502.11946.pdf, step-audio--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Step-Audio 是阶跃星辰 2025-02 开源的「首个生产可用」中文语音交互框架：在 130B 文本 LLM（Step-1）上做音频持续预训练，配双码本（dual-codebook）语音 tokenizer + flow-matching 语音解码器，统一了语音理解与生成，并用「生成式数据引擎」蒸馏出可控的 3B TTS。在自建端到端口语 benchmark StepEval-Audio-360 的 GPT-4o 评测中聊天分 4.11（GLM-4-Voice 3.49），在 LLaMA Question 等公开集上较开源最优平均提升 9.3 分。

## 背景与定位
解决的问题：当时开源语音交互系统存在三大短板——(1) 理解与生成分离、级联 ASR→LLM→TTS 误差累积、端到端难以集成；(2) 高质量纯语音对话数据稀缺、人工录制成本极高，难以快速复刻音色/方言；(3) 缺乏对情感、语速、方言、工具调用的精细动态控制。闭源系统（GPT-4o、豆包）已突破，但开源侧（Qwen2-Audio、Llama 3、wavLLM、GLM-4-Voice、Moshi）各有偏科：GLM-4-Voice 偏低延迟、Moshi 偏音质，没有同时兼顾情感感知、对话自然度与实时知识接入。

技术脉络位置：属于「离散音频 token 建模 + LLM」一脉（对位 Moshi、GLM-4-Voice、Mini-Omni、SpiritLM、MinMo、CosyVoice2），但 Step-Audio 没走纯端到端语音→语音，而是工程上选择了 **AQTA（Audio-input, Text-output）+ TTS** 框架做实时对话。理由有二：纯语音对话数据稀缺限制端到端训练效率；加 TTS 模块换来对音色/音高等输出参数的灵活可控。底座沿用自家 [[step-1]] 130B 文本 LLM，并把 Step-Audio 定位为更大计划 Step-Omni（语音+图像+文本三模态统一）的一个组成部分。相关前置工作：CosyVoice 语义 token、Paraformer 编码器、SpiritLM 交错建模、Demucs 人声分离。

## 模型架构
三大组件：speech tokenizer → LLM → speech decoder。

- **双码本 tokenizer（dual-codebook）**：并行两路离散化，灵感来自 ARCON，交错方式借鉴 SpiritLM。
  - 「linguistic」路：用 **Paraformer** 编码器输出，token 率 **16.7 Hz**，码本大小 **1024**，编码音素/语言学等结构化高层表示。
  - 「semantic」路：用 **CosyVoice** 的 tokenizer，token 率 **25 Hz**，码本大小 **4096**，编码语义 + 粗粒度声学细节。
  - 两路按 **2:3 时间对齐交错**（每 2 个 linguistic token 配 3 个 semantic token），合并成单一序列喂给 LLM。整体采样等效 41.6 Hz。
  - 注：论文正文把 16.7Hz/1024 这一路叫 "linguistic"、25Hz/4096 叫 "semantic"；而 GitHub/HF README 里把 1024 路称 "semantic"、4096 路称 "acoustic"（语义/声学）。命名口径不一致，但所指的两路码本参数（16.7Hz-1024 与 25Hz-4096、2:3 交错）完全一致。
- **LLM**：基于 130B 参数的 **Step-1** 文本 LLM，做音频持续预训练实现语音-文本对齐。注意力是 **ALiBi 的变体**（README 明确：官方 flash-attention 不兼容，需用其自带的 custom flash attention 库 `OPTIMUS_LIB_PATH`）。多轮对话里历史音频先经 ASR 转写成文本再入上下文以省算力，但架构保留按需直接处理音频 token 作历史的能力。
- **speech decoder（语音解码器）**：3B 参数的语言模型 + **flow-matching 模型** + **mel-to-wave vocoder**，把离散 token（语义+声学）还原为连续时域波形。训练用「双码交错」方式保证可懂度与自然度；作者观察到把解码器参数放大后涌现出更强的生成能力。
- **实时推理管线**：Controller 统筹状态机；子系统含 VAD、Streaming Audio Tokenizer（两路并行、定长切片，再 2:3 合并）、Step-Audio LM、Speech Decoder、Context Manager。状态机 Silence→UserSpeaking→UserPaused→BotReplying。
- 工具调用：异步 ToolCall——文本线程处理工具调用，音频生成线程并行产语音流，利用文本与音频比特率差消除工具调用时的等待。

## 数据
多模态预训练数据三大类（音频 / 文本 / 图像），合计约 3.3T tokens：

- **音频**：音频续写（continuation）数据 **1.1T tokens / ~730 万小时**；TTS 合成语音 **113B tokens / ~70 万小时**；ASR 数据 **105B tokens / ~65 万小时**；音频-文本交错数据 **350B tokens / ~200 万小时**。
- **文本**：**800B tokens**（网页、书籍、代码、自有材料）。
- **图像**：**800B tokens** 图文配对/交错数据（为 Step-Omni 三模态准备）。

**TTS 后训练「生成式数据引擎」**（核心创新，绕开人工录音）：三步——(1) 用 **Step-2** LLM 生成语言多样、语义丰富的文本并改写/翻译到目标语言/方言；(2) 选一个加了 audio-token cooldown 的 Step-Audio 预训练 checkpoint，直接生成特定说话人/语言/方言音频；(3) 微调该 checkpoint 得到 **Audio-Edit 模型**，专门生成细腻情感/风格。
- 语言/方言：用少量母语者种子音频+文本做 `[system prompt; prompt text; target text; prompt code; target code]` 续写，快速批量造母语级数据；并用「目标说话人」二次重生成提纯音色一致性。
- 情感/风格：把复杂情感/风格描述转成「对比对」构造——同说话人同文本的中性 vs 情感样本，只用 (中性 token, 情感/风格 token) 对 SFT 得 Audio-Edit；可迭代产不同强度数据。
- 歌唱/RAP：采集 **10000+ 小时**带 LyRiCs 时间戳的歌/RAP，Demucs 提纯人声 + VAD 去静音，按时间戳切分对齐歌词；清洗三步（RAP 分离、音质过滤、CER 对齐校验），最终保留段落仅占原曲时长 **17.8%**。
- 质控：ASR 准确率、VAD、说话人分离、情感识别一致性、DNS 降噪等多指标客观评估。

## 训练方法
**预训练（Step-Omni，三阶段持续预训练）**，统一 speech/image/text，基于预训练文本模型 + 图像编码器：
- Stage1：扩词表加 **5120 个 audio token** + 接入预训练图像编码器组成 Step-Omni。文本 backbone 学习率压低到 **2e-5**，新加的 embedding 和 LM head 学习率设为 backbone 的 5 倍以加速收敛；图像编码器全程冻结。音/文/图配比 **2:1:1**，音频仅纯续写任务。训练 1.2T tokens。
- Stage2：加入音频-文本交错数据，续写:交错 = **1:1**，音/文/图仍 2:1:1。训练 800B tokens。
- Stage3：再加 ASR + TTS 数据，续写:交错:ASR:TTS = **1:1:1:1**，音/文/图调整为 **4:3:3**；embedding/LM head 学习率与 backbone 同步，cosine 从 2e-5 降到 5e-6。

**消融——为什么用双码本**：单用 semantic token，PPL 低、语义连贯好，但丢声学信息导致 vocoder 还原音色/韵律差；单用 linguistic token，音质好但 PPL 高、语义连贯差；双码本交错后，两路 PPL 都比单码本下降（semantic 降得更明显），ASR CER 从 **25.5 → 18.4**（同等音频训练量、3B 验证模型）。2:3 分组交错还能加速 loss 收敛。

**后训练（task-specific）**：
- **TTS**：3B 模型，chat 式 LLM 范式，SFT 1 epoch，lr 2e-5→2e-6 cosine。SFT 用两轮对话格式 `system prompt + human input + assistant response`；指令标签分两类——descriptive tags（语言、方言、人声、风格，由 Step-Audio clone 造数据，含日/韩/粤/川/萌音/RAP/唱）与 comparative tags（情感、语速分级控制，由 Audio-Edit 造数据，喜怒哀+快慢各 5 个层级）。
- **AQTA（对话）= SFT + RLHF(PPO)**，产出 Step-Audio-Chat：
  - SFT 数据类型：TQTA（大量文本 QA）、AQTA（音入文出）、TAQTA（增强文-音一致性，文本 Q 既作输入不计 loss 又作输出计 loss）、以及 AQAA / VAQTA 等增加多样性；并掺 ASR 格式数据增强鲁棒性。单轮做文本长度过滤+口语化改写；多轮把历史语音换成文本、只算最后一轮 loss。SFT 1 epoch，lr 5.656e-5→5.656e-6。
  - **奖励模型**：两阶段——先 TQTA 单模态偏好预训练，再 AQTA 跨模态微调；各 1 epoch，lr 1.24e-5→6e-6，Bradley-Terry loss，从 SFT 模型初始化，人类偏好测试集 pair-wise 准确率 **70.51%**。偏好对由 4 个采样响应经人工 1-5 打分 + LLM-as-a-Judge 对客观题判 0/1 正误共同构造。
  - **PPO**：critic 先 warmup 80 步；clip ε=0.2，lr 1e-6→2e-7 cosine，KL 系数 β=0.05。
  - **特有的 reward hacking——"deaf hacking"**：仅用人工 AQTA 偏好数据训练的 RM 会对"我没听清"类回复无脑给高分（因训练数据里只有"没听清"作 chosen、缺对应 rejected）。缓解：用被 hack 的 PPO 模型对清晰音频生成响应，若出现 hacking 行为则构造为 rejected 补进 RM 数据；未来计划引入 rule-based reward。

## Infra（训练 / 推理工程）
- 训练：**数千张 H800 GPU**，MFU **35%**。除常规定制 GPU kernel + 通信 overlap 外，两项创新：
  - **StarWeaver**：基于 RPC 的分布式数据处理库，把 CPU 密集的多模态数据预处理搬到远端进程，避免与训练 job 抢资源拖慢训练；并借全局负载信息做 data-parallel 维度的负载均衡。
  - **Disaggregated Model Placement（解耦模型放置）**：针对 LLM + 模态编码器异构问题，为各子模型分配专用资源 + 定制并行策略，减少异构带来的流水线气泡（详见 DistTrain, arXiv:2408.04275）。
- 推理：
  - **Speculative Response Generation（投机响应）**：UserPaused 时预生成响应，约 **40%** 投机响应被采纳，每响应延迟较非投机降约 **500ms**。
  - **文本化上下文管理**：用 ASR 文本而非原始音频 token 存历史，文本:音频 token 约 **1:14** 压缩，支持更长对话且质量影响极小。
  - **Streaming Audio Tokenizer**：两路并行定长切片流式 token 化，否则推理随音频长度显著变慢。
- 部署/资源（README）：Step-Audio-Tokenizer 最低 1.5GB；Step-Audio-Chat（130B）最低 **265GB** 显存（实测 4×A800/H800 80G）；TTS-3B 仅 8GB。推荐用 **vLLM + tensor parallel** 跑 130B Chat（官方 vLLM 不支持 Step-1，需用其 add-step1-model 开发分支；注意力为 ALiBi 变体需自带 flash-attention 库）。开源代码 Apache 2.0，权重另有 license。线上版在「跃问」App（yuewen.cn）。

## 评测 benchmark（把效果讲清楚）
**自建 StepEval-Audio-360**（137 条真实用户多轮中文 prompt，9 维：语音指令遵循/语音理解/逻辑推理/角色扮演/创意/唱/语言能力/情感控制/游戏交互，GPT-4o 判分）：

| 模型 | Factuality(%) | Relevance(%) | Chat Score(1-5) |
|---|---|---|---|
| GLM-4-Voice | 54.7 | 66.4 | 3.49 |
| Qwen2-Audio | 22.6 | 26.3 | 2.27 |
| Moshi* | 1.0 | 0 | 1.49 |
| **Step-Audio-Chat** | **66.4** | **75.2** | **4.11** |

（Moshi 不懂中文，*仅供参考）人评雷达图：Step-Audio 全 9 维 SoTA；相对开源最优，回复质量/相关性/事实准确分别 +19.2% / +23.7% / +43.2%，生成控制维（情感、语速、RAP、角色扮演）IF 与 MOS 分别 +29.8% / +27.1%。

**公开口语 QA（AQTA，GPT-4o 判正误）**：

| 模型 | Llama Q | Web Q | TriviaQA* | ComplexBench | HSK-6 |
|---|---|---|---|---|---|
| GLM4-Voice | 64.7 | 32.2 | 39.1 | 66.0 | 74.0 |
| Freeze-Omni | 72.0 | 44.7 | 53.9 | - | - |
| MinMo | 78.9 | 55.0 | 48.3 | - | - |
| Qwen2-Audio | 52.0 | 27.0 | 37.3 | 54.0 | - |
| **Step-Audio-Chat** | **81.0** | **75.1** | **58.0** | **74.0** | **86.0** |

全开源集最高，相对开源最优平均 **+9.3 分**（abstract 口径）。

**ASR（CER/WER，越低越好）**：离散 token 建模这一类里 Step-Audio Pretrain 平均 CER **4.64**（同类最佳，胜过隐特征类的 Whisper Large-v3 7.28；与隐特征类的 Qwen2-Audio 4.32 在整体 AVG 上略逊，但在 Aishell-1/2、Librispeech test-clean 等干净集上几乎持平：论文报 Step-Audio Pretrain 干净子集平均 CER 2.05 vs Qwen2-Audio 2.06，Aishell-1 低至 **0.87**）。对话模型 Step-Audio-Chat 平均 CER 5.89，仍强（GLM-4-Voice Chat 因不遵指令崩到 146.74）。双码本 vs 单码本 ASR CER 25.5→18.4。

**TTS（SEED 测试集，CER/WER↓、SS 说话人相似度↑）**：

| 模型 | test-zh CER | test-en WER |
|---|---|---|
| CosyVoice 2 | 1.45 | 2.57 |
| CosyVoice 2-S | 1.45 | 2.38 |
| Step-Audio-TTS-3B | 1.31 | 2.31 |
| **Step-Audio-TTS(130B)** | **1.17** | **2.0** |

3B 版在开源 LLM-based TTS 中 CER/WER SoTA；放大到 130B 进一步降 CER/WER（说明数据+参数继续 scale 有潜力）。内容一致性 Step-Audio test-zh CER 1.53 / test-en WER 2.71，优于 GLM-4-Voice、MinMo。

**音频指令遵循（GLM-4-Voice vs Step-Audio，IF 与音质各 1-5 MOS）**：Languages 1.9→3.8、Role-playing 3.8→4.2、Singing/RAP 2.1→2.4、Voice Control 3.6→4.4（IF）；音质同样全面领先（如 Singing/RAP 音质 2.4→4.0）。

## 创新点与影响
核心贡献：
1. **双码本语音 tokenizer**：linguistic(16.7Hz/1024)+semantic(25Hz/4096) 2:3 交错，同时兼顾语义连贯（低 PPL）与声学可还原（好音质），单一 LLM 内统一理解+生成。
2. **生成式 TTS 数据引擎**：用 130B Step-Audio + Step-2 改写 + Audio-Edit 对比对，几乎零人工录音地造出多语言/方言/情感/风格/唱-RAP 数据，并蒸馏出 8GB 可跑、指令可控的 Step-Audio-TTS-3B（开源）。
3. **指令驱动的精细语音控制**：descriptive/comparative 双类标签，方言、情感（喜怒哀×5 级）、语速（快慢×5 级）、RAP/唱/萌音可控。
4. **生产级工程**：投机响应（-500ms）、文本化上下文（1:14 压缩）、异步 ToolCall、StarWeaver、解耦模型放置；首个「production-ready」开源语音交互全栈，并附自建 StepEval-Audio-360 多维评测。

影响：作为 2025 年初代表性的中文全模态语音生成/交互开源工作，开源了 Step-Audio-Chat(130B)、Step-Audio-TTS-3B、Step-Audio-Tokenizer 及 StepEval-Audio-360 数据集，被后续工作作为开源 baseline 对照。其自身演进迅速：2025-06 出 Step-Audio-AQAA（音入音出，arXiv:2506.08967），2025-08 升级到端到端 Step-Audio 2 / 2-mini（arXiv:2507.16632），并衍生 Step-Audio-R1（语音推理）、Step-Audio-EditX（音频编辑），本仓库已停止维护并指向上述新版。

已知局限（作者自陈）：当前仅做到语音-文本跨模态，未原生三模态（视觉+语音+文本）；AQTA+TTS 而非纯端到端，AQAA 场景仍有中间跨模态转换开销；"deaf hacking" 类 reward hacking 待 rule-based reward 彻底解决；130B 推理显存门槛高（265GB / 4×80G）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2502.11946
- arxiv_pdf: https://arxiv.org/pdf/2502.11946
- github: https://github.com/stepfun-ai/Step-Audio
- hf (Step-Audio-Chat): https://huggingface.co/stepfun-ai/Step-Audio-Chat
- hf (Step-Audio-TTS-3B): https://huggingface.co/stepfun-ai/Step-Audio-TTS-3B
- hf (Step-Audio-Tokenizer): https://huggingface.co/stepfun-ai/Step-Audio-Tokenizer
- hf (StepEval-Audio-360 数据集): https://huggingface.co/datasets/stepfun-ai/StepEval-Audio-360
- modelscope (Chat): https://modelscope.cn/models/stepfun-ai/Step-Audio-Chat
- 线上产品「跃问」: https://yuewen.cn

## 一手源存档（sources/）
- [arxiv-2502.11946.pdf](https://arxiv.org/pdf/2502.11946)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/step-audio--readme.md)
