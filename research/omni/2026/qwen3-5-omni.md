---
title: "Qwen3.5-Omni Technical Report"
org: "Alibaba Qwen"
country: China
date: "2026-04"
type: tech-report
category: omni
tags: [omni, audio, audio-visual, speech, asr, tts, moe, thinker-talker, streaming, agent, multilingual]
url: "https://qwen.ai/blog?id=qwen3.5-omni"
arxiv: "https://arxiv.org/abs/2604.15804"
pdf_url: "https://arxiv.org/pdf/2604.15804"
github_url: "https://github.com/QwenLM/Qwen3-Omni"
hf_url: "https://huggingface.co/spaces/Qwen/Qwen3.5-Omni-Online-Demo"
modelscope_url: "https://modelscope.cn/studios/Qwen/Qwen3.5-Omni-Online-Demo"
project_url: "https://www.alibabacloud.com/help/en/model-studio/qwen-omni"
downloaded: [arxiv-2604.15804.pdf, qwen3-5-omni--blog.md, qwen3-5-omni--predecessor-qwen3-omni-github-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Qwen3.5-Omni 是阿里 Qwen 的新一代「原生全模态」旗舰大模型——把 [[qwen3-omni]] 的 Thinker–Talker 架构从 30B-A3B 扩到数千亿参数（Plus/Flash/Light 三档）、上下文 32k→256k（>10 小时音频 / 400 秒 720P@1FPS 音视频），Thinker 与 Talker 双双换成 Hybrid-Attention MoE；最关键的两项创新是 **ARIA（Adaptive Rate Interleave Alignment）流式语音对齐** 与 **Hybrid-MoE 的 Gated Delta Net 长序列加速**。Qwen3.5-Omni-Plus 在 215 项音频/音视频子任务与 benchmark 上拿到 SOTA，通用音频理解/推理/识别/翻译/对话全面超越 Gemini-3.1 Pro、音视频理解整体追平 Gemini-3.1 Pro，同时文本/视觉不掉点（与同尺寸 Qwen3.5-Plus 持平）。

## 背景与定位
人类与世界的交互天然是「全模态 + agentic」的：同时整合视觉、听觉、语言，并以文本、语音、工具动作作出回应。过去的多模态模型多停留在「被动感知—响应」范式，缺乏可扩展的 agentic 行为、实时交互、自主工具调用与跨模态推理。

Qwen3.5-Omni 在 [[qwen2-5-omni]] 首创的 Thinker–Talker 框架、[[qwen3-omni]] 的工程化基础上，定位为「原生 omni agent 模型」——不仅跨模态感知与推理，还能自主拉起 WebSearch、执行复杂 FunctionCall、生成语音、做实时流式交互。相对 Qwen3-Omni 的五项关键升级（官方原文）：

1. Thinker 与 Talker **均改为 Hybrid-Attention MoE**，长序列推理高效；
2. 长上下文 **32k → 256k**（>10 小时音频 / 400 秒 720P@1FPS）；
3. 语音生成端用 **多码本（multi-codebook）codec 表征**，实现单帧即时合成；
4. Talker 引入 **ARIA** 动态对齐文本与语音单元，提升自然度与鲁棒性；
5. 多语言大幅扩展：语音识别 **113 种语种/方言**、语音合成 **36 种**。

由此衍生三项新能力：(1) 可控音视频 captioning（自动切片 + 时间戳打标 + 人物-音频关系的剧本级细粒度描述）；(2) 全面实时交互（语义打断 / turn-taking 意图识别、端到端语音控制音量·语速·情绪、用户样本音色克隆）；(3) 原生全模态 agentic 行为（自主 WebSearch、复杂 FunctionCall、以及涌现出的 **Audio-Visual Vibe Coding**——直接从音视频指令生成可执行代码）。

> 说明：Qwen3.5-Omni 目前**仅通过 API 开放**（阿里云百炼 Offline/Realtime API），尚未开源权重；本页一手源为 arXiv 技术报告（2604.15804，2026-04-22）与官方博客（qwen.ai，2026-03-29）。开源的是上一代 [[qwen3-omni]]（30B-A3B，arXiv 2509.17765）。

## 模型架构
延续 **Thinker–Talker** 双模块架构（Thinker 出文本，Talker 出流式语音 token）。整体 backbone 为 **Hybrid Mixture-of-Experts（Hybrid-MoE）**，相比上一代纯 MoE 更好地平衡容量与效率。报告给出的模块清单（Table 1）：

| 模块 | 架构 | 是否流式 |
|---|---|---|
| Audio Encoder | AuT | ✓ |
| Vision Encoder | SigLIP2 | – |
| Thinker | Hybrid MoE Transformer | ✓ |
| Talker | Hybrid MoE Transformer | ✓ |
| MTP | Dense Transformer | ✓ |
| Code2Wav | ConvNet | ✓ |

**AuT（Audio Transformer）音频编码器**：从零训练的 attention encoder-decoder，消耗 **4000 万小时** 由 Qwen3-ASR 生成的音频-文本对；用 4 个 Conv2D block 把 filter-bank 特征 **16 倍下采样**，再过 self-attention，输出 **6.25 Hz token rate**（每帧≈160 ms 原信号）。相比 Qwen3-Omni 编码器，更多多语种数据（>20 语言），中/英/多语配比 **3.5 : 3.5 : 3**；采用**动态注意力窗口大小**训练，兼顾实时 prefill 缓存与离线理解。

**感知（Perception）**：
- 文本用 Qwen3.5 tokenizer，**byte-level BPE，词表 150k→250k**，多数语言编解码效率提升 10–60%；
- 音频 16 kHz、128 通道 mel（25 ms 窗 / 10 ms hop）经 AuT；
- 视觉用 Qwen3.5 的 vision encoder（图像+视频混训），视频按**动态帧率**采样；
- **音视频时间戳**：**仍沿用 [[qwen3-omni]] 的 TM-RoPE**（temporal ID 显式锚定绝对时间，做音视频同步）；但报告发现「直接把绝对时间编进 temporal position ID」对长视频会产生过稀疏索引、削弱长程时序建模、且要求大规模均匀帧率样本（抬高数据构造成本）。**改进做法**：在每个视频/音视频时间片**前置一个「秒为单位的格式化文本时间戳字符串」**让模型更自然地学习 timecode，音频序列还**随机间隔插入时间戳**对齐——是在 TM-RoPE 之上叠加文本 timecode，而非弃用 TM-RoPE。音频每 160 ms 一个时序 ID，视频帧按实际时间戳动态调整保持 160 ms/ID 的一致分辨率；多模态位置编号连续递增避免冲突。这一设计支持任意时长的流式输入。

**语音生成（Talker）**：直接在 Qwen3.5-Omni-Audio-Tokenizer 产生的 **RVQ tokens** 上工作（用 RVQ 替代繁重的 DiT 运算）；用 **MTP（multi-token prediction）模块** 建模残差码本（residual codebooks）做细粒度声学控制，配 **causal ConvNet（Code2Wav）** 逐帧增量合成波形，低延迟高保真。两点区别于 Qwen3-Omni：
- 为 Talker 设**专用 system prompt** 指定目标音色，支持零样本音色克隆与可控语音生成（比传统 speaker embedding 能编码更丰富的文本描述+codec 序列线索）；
- **ARIA（Adaptive Rate Interleave Alignment）**：把传统**双轨（dual-channel）**生成统一成**单轨交错（single-channel interleaved）**。不依赖 MFA 强制对齐或固定交错率，而是施加**自适应率约束**——对生成序列的任意前缀，累计「语音:文本」token 比不得超过该条目级全局比。设计简单但能在不同语言（含编码效率低的语言）灵活对齐文本-语音，自然支持「任意文本前缀 + 连贯语音续写」。

**Hybrid-MoE + Gated Delta Net（GDN）**：Hybrid-MoE 含 GDN 模块，对长音视频序列建模特别有效，**显著降低长上下文推理的 KV-cache I/O 开销**，提升吞吐与服务并发。

**变体**：博客披露 Plus / Flash / **Light** 三档 Instruct（技术报告主要评测 Plus 与 Flash）。**各档具体参数量、激活参数、专家数、层数、隐藏维度等数字均未在技术报告/博客披露**（仅定性称「扩到数千亿参数」）。

## 数据
**预训练总配比（S2 阶段约 4T tokens，Table）**：text 0.92T、audio 1.99T、image 0.95T、video 0.14T、video-audio 0.29T——可见**音频占比最高（近一半）**，与 omni 旗舰的音频/音视频导向一致。整体在「海量文本 + 视觉 + 超过 **1 亿小时**音视频数据」上原生多模态预训练。覆盖模态：image-text、video-text、audio-text、video-audio、video-audio-text、纯文本。沿用 Qwen3-Omni 的「更宽的自然语言 prompt」增强泛化与指令跟随；早期预训练阶段即同时引入单模态与跨模态数据。

**AuT 编码器数据**：4000 万小时音频-文本对（由 Qwen3-ASR 生成），>20 语言，中/英/多语 = 3.5:3.5:3。

**Talker 数据**：General 阶段 **>2000 万小时**多语种语音 + 多模态上下文，含 instruction-following 语音生成等多样任务；Long-Context 阶段经专门 curation pipeline 做数据质量分层、在高质量子集上做 CPT，并借 Qwen3-Omni-Captioner 缓解初始预训练噪声引入的幻觉。

**语言覆盖（Plus，Table 3）**：文本 201 种、语音输入 113 种（74 语言 + 39 中文方言）、语音输出 36 种（29 语言 + 7 中文方言）。

> 数据来源/清洗过滤/re-captioning/美学与安全过滤等更细的工程细节**未披露**。

## 训练方法
**预训练三阶段**：
- **S1 编码器对齐**：锁住 LLM（用 Qwen3.5 初始化），vision encoder 取自 Qwen3.5、audio encoder 用 AuT 初始化；两编码器在固定 LLM 上分别训练，先训各自 adapter 再训编码器，用海量 audio-text / image-text 对增强语义理解；
- **S2 通用阶段**：解冻全部参数，约 4T tokens（配比见上），序列长 32,768；
- **S3 长上下文阶段**：序列长 **32,768 → 262,144**，提高长音频/长视频比例。

**后训练（Thinker，三阶段）**，语料用 ChatML 格式（纯文本 / 视觉 / 音频 / 混合模态对话）：
- **Stage 1 专家蒸馏（Specialist Distillation）**：先用独立 SFT + RL 训一组领域专家 teacher（文本 agentic/coding/推理，以及 vision、audio 专家），均从 Qwen3.5 base 微调；teacher 生成领域数据，蒸馏进单一统一模型；
- **Stage 2 On-Policy Distillation（OPD）**：补「音频 query 回答质量 << 文本 query」的差距——对每个 audio-text 配对 query，先取文本条件下的（更高质量）回答，作为对应音频条件 query 的蒸馏目标，使音频条件输出对齐文本条件行为；
- **Stage 3 交互对齐 RL（Interaction-Aligned RL）**：针对多轮对话中的语言串码（code-switching）、人格不一致、长上下文指令跟随退化等问题，构造多轮交互轨迹并围绕用户体验目标设计 reward，优化交互稳定性与一致性。报告称 OPD + 交互对齐 RL 还正向提升了指令跟随（IFBench 反超基线）。

**后训练（Talker，四阶段）**，ChatML 格式与 Thinker 一致、便于音色克隆：
- **General**：>2000 万小时多语种语音 + 多模态上下文预训练；
- **Long-Context**：数据质量分层 + 在高质量子集 CPT（借 Qwen3-Omni-Captioner 降幻觉），上下文扩到 **64k**；
- **RL**：用 **DPO**（人工标注多语种偏好对）做偏好对齐，并加入 rule-based reward、采用 **GSPO** 提升整体能力与训练稳定性；
- **Speaker Fine-tuning**：轻量说话人微调，忠实捕捉目标说话人特征，进一步提升自然度/表现力/可控性。

> 训练目标为 next-token（AR）+ 偏好优化（DPO/GSPO）；扩散/flow-matching/步数蒸馏等不适用（语音走 RVQ codec + MTP + ConvNet 路线，非 DiT）。具体学习率/batch/step 等超参未披露。

## Infra（训练 / 推理工程）
**流式与并发（Table 1/2）**：
- 端到端**首包延迟**（Plus）：音频输入 435 ms、视频输入 651 ms；（Flash）音频 235 ms、视频 426 ms；
- 保留 **Chunked Prefilling**（音/视频编码器沿时间维输出 chunk），显著降低 Thinker/Talker 的 TTFT；
- Hybrid-MoE 的 **GDN** 模块降 KV-cache I/O，提升长上下文吞吐与并发；
- ARIA 把双轨生成重组为单轨交错流，减少两路同步开销、利于 token 调度。

**推理栈**：理论首包延迟在**内部 vLLM** 上评测，MTP 模块与 codec decoder 启用 **torch.compile + CUDA Graph** 加速。Table 2 给出不同并发（1/4/8）下的 Thinker TTFT、Talker TTFC、TPOP、TPS 与 Generation RTF——例如 Flash 1 并发音频/视频 TTFT 80/255 ms、整体延迟 235/426 ms；Plus 1 并发整体 435/651 ms；随并发提升延迟与解码效率保持稳定，低 RTF 给流式音频留足余量。Flash 与 Plus 因规模差异采用不同部署期资源分配与并行策略，两者延迟/吞吐**不宜横向严格对比**。

**部署形态**：阿里云百炼 Offline API（qwen-omni）+ Realtime API（WebSocket，`qwen3.5-omni-plus-realtime` 等，24 kHz PCM 输出，支持 region cn/intl）。

> 训练算力规模 / GPU·时 / 并行分布式拓扑 / 混合精度 / 量化等**均未披露**。

## 评测 benchmark（把效果讲清楚）
> 数字来自技术报告 Tables 4–12 与官方博客对应表（两源一致）。Plus / Flash 为本作两档；基线为同尺寸 Qwen3.5-Plus 与 Gemini-3.1 Pro。文本/视觉对照用 **Qwen3.5-Plus-NoThinking**（同 no-thinking 设定）。

**215 项 SOTA 拆解（博客）**：3 个音视频 benchmark + 5 个音频 benchmark + 8 个 ASR benchmark + 156 个面向语种的 S2TT 任务 + 43 个面向语种的 ASR 任务。

**Audio → Text（vs Gemini-3.1 Pro，Table 5；↑越高越好，ASR 为 WER↓）**：
- 音频理解：MMAU **82.2**（Gemini 81.1 / Flash 80.4）；MMAR 80.0（Gemini 83.7，略低）；MMSU **82.8**（81.3）；RUL-MuchoMusic **72.4**（59.6，大幅领先）；
- 对话：VoiceBench **93.1**（88.9，显著超越）；WildSpeech-Bench 75.4（76.3，接近）；
- S2TT（top59）：xx⇄zh **30.2**、xx⇄en **35.4**、混合 **32.8**，均超 Gemini（29.5/34.6/32.1）；
- ASR（WER↓）：Fleurs(top60) **6.55**（Gemini 7.32）、CV15-en **4.83**（8.73）、LibriSpeech clean/other **1.11/2.23**（3.36/4.41）、WenetSpeech net/meeting **4.30/5.84**（11.53/14.21）、KeSpeech **3.46**（23.67）——ASR/翻译全面领先。

**Audio-Visual → Text（vs Gemini-3.1 Pro，Table 7）**：
- DailyOmni **84.6**（Gemini 82.7，SOTA）；AVUT 85.0（85.6，接近）；WorldSense 62.8（65.5）；AV-SpeakerBench 71.3（75.1）；VideoMME w/audio 83.7（89.0）；
- Audio Query QA：Qualcomm IVD **68.5**（66.2，实时交互场景大幅领先）；
- Caption：Omni-Cloze **64.8**（57.2）；
- Agent/工具：OmniGAIA **57.2**（Gemini 68.9 更高；用 DeepSeek-V3.2-Thinking 当 judge）。
- 结论：整体音视频理解追平 Gemini-3.1 Pro，实时音视频交互（IVD）领先。

**Text → Text（vs Qwen3.5-Plus-Instruct/NoThinking，Table 4）**：Plus 基本与纯文本同尺寸持平——MMLU-Pro 85.9（基线 86.8）、MMLU-Redux 94.2、SuperGPQA 66.4、C-Eval 92.0、GPQA 83.9、LiveCodeBench v6 65.6、HMMT Nov25 84.4、IMOAnswerBench 65.5、BFCL-V4 63.3、TAU2Bench 81.0；**IFBench 52.6 略超基线 51.1**（归功于 OPD + 交互对齐 RL）。

**Vision → Text（Table 6）**：Plus 与同尺寸文本视觉模型相当，**视频理解更强**——VideoMME(w/o sub) 81.9（基线 81.0）、MLVU 86.8（85.1）、MVBench 79.0（76.7）、LVBench 71.2（68.6）、MME-VideoOCR 77.0（74.2）；MMMU 80.1、MathVision 73.0、OCRBench 91.3、RefCOCO 95.0、SLAKE 84.7。

**X → Speech（语音生成）**：
- 零样本 TTS（SEED-TTS，WER↓，Table 8）：Plus test-zh/test-en = **0.99 / 1.26**，test-en 取得最佳；优于 Qwen3-Omni-30B-A3B（1.07/1.39）、CosyVoice 3（0.71/1.45）、MiniMax-Speech（0.83/1.65）、F5-TTS（1.56/1.83）等；
- 多语种 TTS（Table 9/10）：29 种语言可生成，**22/29 种语言取得最低 WER**，超 MiniMax-Speech 与 ElevenLabs，且 speaker similarity（SIM↑）多数语种最高；
- 跨语种音色克隆（Table 11，mixed error rate↓）：12 个方向中 **10 个取得最佳**；zh→ko 从 CosyVoice3 的 14.4 降到 **4.03（约 -72%）**；
- 自定义音色（Table 12，vs ElevenLabs / Gemini-2.5 Pro-TTS / GPT-Audio / MiniMax，2026-03 经官方 API 测）：仅单语数据微调却能迁移到 29 种语言，**10 种语言 WER 最佳**，日语 3.306 / 韩语 1.309 等难语种优势明显。
- 博客补充稳定性表：Seed-hard WER 6.24（ElevenLabs 27.70 / Gemini-2.5 Pro 11.57 / GPT-Audio 8.19 / MiniMax 8.62）；音色克隆 Public-Multilingual-avg(20 lang) WER 1.87、SIM 0.79。

**关键设计/结论**（报告为定性陈述，未给出严格消融对照表）：(1) 在 TM-RoPE 基础上叠加「文本时间戳字符串 + 音频随机插入时间戳」，缓解纯绝对时间 temporal ID 在长视频上的稀疏索引、长程时序更稳、降数据构造成本；(2) OPD 让音频条件回答质量逼近文本条件；(3) 偏好优化（DPO + 规则奖励 + GSPO）后语音生成稳定性/自然度进一步提升（SEED test-en 1.26）。

## 创新点与影响
**核心贡献**：
1. **ARIA（Adaptive Rate Interleave Alignment）**——以「前缀累计语音:文本比 ≤ 全局比」的自适应率约束，把双轨语音生成统一为单轨交错流，免 MFA/固定交错率，解决跨语言（尤其低编码效率语言）流式合成的漏读/误读/数字发音模糊，是本作最显著的方法创新；
2. **Hybrid-Attention MoE + GDN** 同时用于 Thinker 与 Talker，把 omni 旗舰推到 256k 上下文（>10h 音频 / 400s 720P 视频）并保持高并发低延迟；
3. **多码本 codec + MTP + causal ConvNet** 的单帧即时语音合成路线（以 RVQ 替代 DiT），低延迟高保真；
4. **在 TM-RoPE 之上叠加「文本时间戳字符串」**（而非弃用 TM-RoPE）：缓解纯绝对时间 temporal ID 在长视频上的稀疏索引问题，提升长视频时序鲁棒性、降数据构造成本；
5. **原生全模态 agentic**：自主 WebSearch / 复杂 FunctionCall，以及涌现的 **Audio-Visual Vibe Coding**（从音视频指令直接生成可执行代码）；
6. 113 语种语音识别 / 36 语种语音合成的大规模多语言扩展 + 零样本音色克隆。

**影响**：把「原生 omni + 实时交互 + agentic」整合进单一旗舰系统，证明原生全模态 scaling 能在不牺牲文本/视觉的前提下，让模型「既感知推理、又实时交互与行动」，为通用全模态 agent 提供了一条工程可落地的范式；ARIA 对流式 TTS 社区有直接借鉴价值。

**已知局限**：
- **仅 API 开放、未开源权重**，各档参数量/专家配置等架构数字未披露，第三方难复现；
- Agent 工具使用 OmniGAIA（57.2）仍落后 Gemini-3.1 Pro（68.9）；部分音视频文本-query 任务（WorldSense / AV-SpeakerBench / VideoMME-w/audio）相对 Gemini 仍有差距；
- 训练算力/GPU·时/并行/数据清洗细节均未公开。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2604.15804
- arxiv_pdf: https://arxiv.org/pdf/2604.15804
- blog (官方一手): https://qwen.ai/blog?id=qwen3.5-omni
- HF demo space: https://huggingface.co/spaces/Qwen/Qwen3.5-Omni-Online-Demo
- ModelScope demo: https://modelscope.cn/studios/Qwen/Qwen3.5-Omni-Online-Demo
- API 文档（阿里云百炼）: https://www.alibabacloud.com/help/en/model-studio/qwen-omni
- 预代码 GitHub（上一代 Qwen3-Omni，开源）: https://github.com/QwenLM/Qwen3-Omni

## 本地落盘文件
- ../../../sources/omni/2026/arxiv-2604.15804.pdf
- ../../../sources/omni/2026/qwen3-5-omni--blog.md
- ../../../sources/omni/2026/qwen3-5-omni--predecessor-qwen3-omni-github-readme.md
