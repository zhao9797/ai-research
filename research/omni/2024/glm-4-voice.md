---
title: "GLM-4-Voice: Towards Intelligent and Human-Like End-to-End Spoken Chatbot"
org: "Zhipu AI / Tsinghua University"
country: China
date: "2024-12"
type: tech-report
category: audio
tags: [speech-lm, spoken-chatbot, speech-tokenizer, flow-matching, interleaved-pretraining, streaming, end-to-end, glm]
url: "https://arxiv.org/abs/2412.02612"
arxiv: "https://arxiv.org/abs/2412.02612"
pdf_url: "https://arxiv.org/pdf/2412.02612"
github_url: "https://github.com/THUDM/GLM-4-Voice"
hf_url: "https://huggingface.co/THUDM/glm-4-voice-9b"
modelscope_url: "https://modelscope.cn/models/ZhipuAI/glm-4-voice-9b"
project_url: ""
downloaded: [arxiv-2412.02612.pdf, glm-4-voice--readme.md, glm-4-voice--readme-en.md, glm-4-voice--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
GLM-4-Voice 是智谱 AI + 清华推出的端到端中英双语语音对话模型：核心是把 ASR 模型（whisper-large-v3）改造成 **12.5Hz / 175bps 单码本监督语义 tokenizer**，让 LLM（GLM-4-9B）直接以 next-token 方式建模语音 token，并用「流式思考（Streaming Thoughts）」模板交替输出文本与语音 token 实现低延迟。在 1T token 的语音-文本预训练后，spoken-QA 显著超过 Moshi（Llama Questions S→T 64.7 vs 62.3、Web Questions 32.2 vs 26.6），对话评测（ChatGPT Score）以 General QA 5.40 / Knowledge 5.20 全面领先 Llama-Omni / Mini-Omni / Moshi。

## 背景与定位
传统语音助手是 **ASR → LLM → TTS** 级联管线，延迟高、误差累积、且无法表达情感/语调等副语言信息。端到端语音语言模型（SpeechLM）是更优路线，但面临核心矛盾：**语音数据相对文本语料极度稀缺**，导致直接在语音上预训练的模型「智商」上不去；而另一类做法（给现成 LLM 接 speech encoder + TTS，再用 spoken-QA 数据微调，如 [[llama-omni]]、Freeze-Omni）缺乏专门的语音预训练，无法生成真正拟人、有表现力的语音。

GLM-4-Voice 的定位：用「**预训练-微调**」范式正面解决这两个难题——
- 用合成的**交错（interleaved）语音-文本数据**把文本 LLM 的知识高效迁移到语音模态，绕开真实语音-文本平行语料稀缺的瓶颈；
- 用**单码本 12.5Hz tokenizer** 把语音表示成与文本等价的离散 token 序列，对自回归 transformer 架构改动最小，从而保住 LLM 的智商。

技术脉络上承接 GSLM（语义 token 上做 next-token）、AudioLM（语义+声学 token）、TWIST（从文本 LLM 热启动）、Spirit-LM（加入交错数据）、Moshi（7M 小时语音 scale-up + 全双工）。tokenizer/decoder 沿用 [[cosyvoice]] 的「监督语义 tokenizer + flow-matching 解码器」思路。本文的语音 tokenizer、decoder、交错数据合成方法实际来自其姊妹篇 **Zeng et al. 2024（arXiv 2411.17607,《Scaling Speech-Text Pre-training with Synthetic Interleaved Data》）**，本报告在此之上聚焦于「构建拟人对话机器人」的预训练配比与 SFT。

## 模型架构
GLM-4-Voice 由三个解耦组件组成，**对自回归 transformer 改动最小**（关键设计理念：单码本 + 输入输出统一表示）：

**1. GLM-4-Voice-Tokenizer（语音→离散 token）**
- 基座：**whisper-large-v3 的 Encoder**，在其中间插入一个 **pooling 层** 降采样 + 一个 **vector quantization（VQ）层**，构成单码本量化瓶颈。
- 帧率 **12.5Hz**（每秒音频仅 12.5 个离散 token），码率 **175bps**（超低）。降采样率越低，码本规模相应增大以补偿信息损失。
- 码本用 **EMA 更新**（decay 0.99），并对平均使用率低于阈值的码字用量化前的连续表示随机重置，以对抗码本坍缩（codebook collapse，沿用 Dhariwal/Jukebox 做法）。
- **流式因果化**：把 encoder 前的卷积换成 causal convolution，把 encoder 内的双向注意力换成 **block causal attention**，使输入语音可流式编码（处理当前 block 即可，与总时长无关）。

**2. GLM-4-Voice-Decoder（离散 token→波形）**
- 沿用 [[cosyvoice]] 的解码器结构：**speech token encoder + 条件流匹配（Conditional Flow Matching）模型 + HiFi-GAN vocoder**。
- 流式推理：训练时混入截断音频样本（前 n·b 秒），推理时用前 (n-1)·b 秒语音作 prompt、预测 (n-1)·b 到 n·b 秒的内容。block size **b=0.8 秒**，意味着**最少 10 个语音 token 即可开始生成首段音频**。

**3. GLM-4-Voice-9B（语音 LLM）**
- 基座 **GLM-4-9B-Base**，**扩充词表**加入语音 token，输入输出用统一的语音表示，从而能对语音做 next-token prediction。
- 这是「Chat Model」主体，承担语音理解与生成。

**条件注入 / 模态融合**：语音与文本被压成同一离散 token 空间，靠扩充词表 + 自回归建模天然融合，无需额外的跨模态 adapter。

## 数据
**Tokenizer 微调数据**（语义信息靠 ASR 准确率间接监督）：
- 有监督 ASR 数据集：LibriSpeech、GigaSpeech、MLS-Eng、WenetSpeech、CommonVoice、AISHELL-1，外加 **10k 小时自有中文 ASR 数据**。
- **700k 小时无监督语音**，伪标签由 whisper-large-v3（英）和 paraformer-large（中）生成。
- 监督样本:伪标签样本 = **1:3**；从 whisper-large-v3 微调 **2 epoch**，batch 4096，lr 1e-5；commitment loss 系数 10.0。

**Decoder 训练数据**：两阶段——预训练阶段用全部无监督语音（多说话人、多质量）；微调阶段用**单一说话人的高质量语音**。

**Stage 1 预训练语料配比（共 1T token，Table 2）**：
| 类型 | Speech token | Text token | Epochs |
|---|---|---|---|
| Speech-Text（交错） | 455B | 279B | 0.90 |
| Speech-Only（无监督，700k 小时） | 31B | — | 2.10 |
| ASR + TTS（监督） | 11B | 3.5B | 2.07 |
| Text-only（保智商） | — | 10T | 0.03 |

- 固定 **30% 文本数据**采样比；无监督语音、监督语音各跑 1 epoch；其余由**合成交错语音-文本数据**填充。
- **交错数据合成**：用一个 text-to-token LM 把现有文本预训练语料转换成语音 token，与文本 token 交错排布——这是绕过真实平行语料稀缺、规模化迁移文本知识的关键。

**Stage 2 SFT 数据**：
- **多轮对话语音**：主要源自文本对话数据，严格过滤；**剔除代码/数学内容**（不适合口语），缩短长文本、去掉不宜口播的输出；再合成对应语音；标注员另录多样化语音输入以贴近真实语音聊天场景。
- **语音风格可控对话**：针对语速、情感、方言等特定风格要求的高质量多轮口语对话。

## 训练方法
**整体范式：预训练（Stage 1）→ SFT（Stage 2）**，从文本 LLM 热启动而非从零训语音。

**Stage 1 — 联合语音-文本预训练**
- 从 GLM-4-9B-Base 初始化，扩词表；在 **1T token** 上做 next-token prediction。
- 优化器 AdamW（β1=0.9, β2=0.95），序列长 8192，lr 从 6e-5 线性衰减到 6e-6。
- 同时混入文本预训练数据保持文本性能。
- 三类语音数据（交错 / 无监督 / 监督 ASR+TTS）各司其职，分别负责跨模态知识迁移、真实语音建模、基础语音任务。

**核心推理/训练机制 —— 解耦 + 流式思考**
- 把 speech-to-speech 解耦成两子任务：**Speech-to-Text**（据用户语音 Qs 生成文本回复 At）+ **Speech-and-Text-to-Speech**（据 Qs 和 At 生成语音 As）。先文本后语音，让语音生成被文本引导以保质。
- 直接「先全文本后全语音」会带来很高的首 token 延迟。故设计 **Streaming Thoughts 模板**：交替输出文本 / 语音 token。基于 12.5Hz tokenizer，**交替生成 13 个文本 token + 26 个语音 token（1:2 比例）**——保证文本生成始终快于语音，使语音 token 总有文本上下文可参照。

**Stage 2 — 监督微调**
- 沿用解耦 + 流式思考模板。每个对话轮包含 Qs / Qt / At / As。
- 观察到两子任务学习曲线不同：**文本输出学得比语音输出快**。故把每条样本拆成两份——一份 mask 语音 loss（专学文本输出），一份 mask 文本 loss（专学语音输出）。
- **语音输出训 20 epoch，文本输出训 4 epoch**；lr 从 1e-5 衰减到 1e-6；weight decay 0.1，隐层 dropout 0.5，梯度裁剪到 1.0（抑制过拟合）。

**蒸馏/加速**：未使用 consistency/LCM 等扩散蒸馏；低延迟主要来自 tokenizer 与 decoder 的流式因果化设计 + Streaming Thoughts 交错模板，而非步数蒸馏。

## Infra（训练 / 推理工程）
- **算力规模 / GPU·时 / 并行策略 / 吞吐：未披露**（报告未给出训练卡数、训练时长、分布式并行方案）。
- 训练精度等细节报告未列；HF/README 提供推理部署形态：`model_server.py` 支持 **bfloat16** 与 **int4** 量化两种 dtype（int4 用于低显存场景），官方提供 docker 镜像 `zhipuai/glm-4-voice:0.1`。
- **延迟分解（理论建模）**：首段语音波形总延迟 = Tspeech_tokenize（流式分块，仅与 block 相关）+ Tllm_prefill（≈ 12.5 × 用户语音秒数 的 token 数）+ Tllm_decode（首响应需 13 文本 + 10 语音 = **23 个 token**）+ Tspeech_decode（10 个语音 token 生成首块音频）。即首音频最低只需 **LLM 解出约 20 个 token** 即可起播。
- 部署形态：开源 9B chat model + tokenizer + decoder 三件套（HF / ModelScope），Web Demo 支持语音/文本输入并返回语音+文本。

## 评测 benchmark（把效果讲清楚）
**1. Tokenizer / Decoder（Table 1，语义保真 & 重建质量）**
- 12.5Hz / 175bps 变体的**语义保真**（微调后 ASR 准确率间接度量）：LibriSpeech LS-clean **WER 2.10** / LS-other 4.90、AISHELL-1 **CER 3.02**（基座 whisper-large-v3 自身 50Hz 为 2.50 / 4.53 / 9.31，量化后语义信息基本保住）。
- 同一 12.5Hz 变体的**重建质量**：重建 **WER 8.43**、**VisQOL 2.52**、**MOSNet 3.39**——VisQOL 低于 50Hz/25Hz 高码率变体，但在 175bps 超低码率下仍维持可用质量，综合码率-质量权衡后选为最终配置。

**2. Base — Speech Language Modeling（Table 3，likelihood 选续写）**
| 模型 | 模态 | Topic-StoryCloze | StoryCloze |
|---|---|---|---|
| TWIST 7B | S→S | 66.6 | 53.3 |
| Spirit-LM 7B | S→S | 82.9 | 61.0 |
| Spirit-LM 7B | S→T | 88.6 | 64.6 |
| Moshi 7B | S→S | 83.0 | 60.8 |
| **GLM-4-Voice 9B** | **S→T** | **93.6** | **76.3** |
| **GLM-4-Voice 9B** | **S→S** | 82.9 | **62.4** |

**3. Base — Spoken Question Answering（Table 4）**
| 模型 | 模态 | Web Q | Llama Q | TriviaQA |
|---|---|---|---|---|
| Moshi 7B | S→T | 26.6 | 62.3 | 22.8 |
| Moshi 7B | S→S | 9.2 | 21.0 | 7.3 |
| **GLM-4-Voice 9B** | **S→T** | **32.2** | **64.7** | **39.1** |
| **GLM-4-Voice 9B** | **S→S** | **15.9** | **50.7** | **26.5** |
- 全面超过 Moshi；S→T 恒优于 S→S（文本引导仍必要），但本文显著缩小了二者差距（尤其 Llama Questions）。

**4. Base — ASR / TTS（Table 5）**
- ASR：LibriSpeech test-clean **WER 2.82** / test-other 7.66；AISHELL-1 **CER 2.46**（whisper-large-v3 baseline 为 2.50 / 4.53 / 9.31，GLM-4-Voice 在 AISHELL-1 上反超）。
- TTS：LibriTTS WER **5.64**；Seed-TTS test-en **2.91** / test-zh **2.10**（CosyVoice baseline 对应 LibriTTS 3.17、Seed-TTS 3.39 / 3.10，GLM-4-Voice 在 Seed-TTS 上更优、LibriTTS 略逊）。

**5. Chat 模型评测（Table 6，最亮眼）**——GPT-4o（gpt-4o-2024-05-13）打分，UTMOS 测语音自然度，ASR-WER 测文本-语音对齐：
| 模型 | General QA↑ | Knowledge↑ | UTMOS↑ | ASR-WER↓ |
|---|---|---|---|---|
| SpeechGPT | 1.40 | 2.20 | 3.86 | 66.57 |
| Mini-Omni | 2.44 | 1.10 | 3.17 | 25.28 |
| Llama-Omni | 3.50 | 3.90 | 3.92 | 9.18 |
| Moshi | 2.42 | 3.60 | 3.90 | 7.95 |
| **GLM-4-Voice** | **5.40** | **5.20** | **4.45** | **5.74** |
- GLM-4-Voice 在对话质量、知识正确率、语音自然度、文本-语音一致性四项全面领先。

**关键消融/结论**：① S→T 恒优 S→S → 文本引导对智商不可或缺，故采用解耦 + Streaming Thoughts；② 缺乏语音预训练的 Mini-Omni（直接 instruction 微调）文本与语音质量都严重受限，印证大规模语音预训练的必要性。

## 创新点与影响
**核心贡献**
1. **单码本 12.5Hz / 175bps 监督语义 tokenizer**：把 ASR 模型（Whisper）加 VQ 瓶颈改造成超低码率单码本 tokenizer，既保语义又支持高质量重建，避免多码本 RVQ 带来的并行预测/架构复杂化，最大程度保住 LLM 文本能力。
2. **合成交错语音-文本数据**：用 text-to-token LM 把海量文本语料转成语音 token 做交错预训练，绕开真实平行语料稀缺，规模化（1T token）把文本知识迁移到语音模态——这是本工作智商领先 Moshi 的关键。
3. **Streaming Thoughts 模板**：13:26（1:2）文本-语音 token 交替，兼顾「文本引导保质」与「低延迟起播（约 20 token）」，调和了端到端建模与高智商的矛盾。
4. **开源**：tokenizer + 9B chat model + decoder 三件套全开源，成为中文社区端到端语音对话的代表性开源基线。

**影响**：作为 2024 年中文开源端到端语音对话的标杆，其「ASR 模型改 tokenizer + 交错数据预训练 + 流式思考」范式被后续中文 omni/语音工作广泛参照；tokenizer 与交错数据方法（姊妹篇 2411.17607）成为可复用的基础设施。

**已知局限**
- S→S 仍弱于 S→T，纯语音到语音对话的智商有差距，依赖文本中介。
- 训练算力 / 并行 / GPU·时等 infra 细节完全未披露。
- decoder 微调用单一说话人高质量语音，音色多样性受限。
- 评测中 GLM-4-Voice 为双语模型、有时用中文回英文问，为公平对比英文 baseline 需强制限定英文输出。
- 未做 RLHF/DPO 等偏好对齐（仅 SFT），对齐手段相对简单。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2412.02612
- pdf: https://arxiv.org/pdf/2412.02612
- github: https://github.com/THUDM/GLM-4-Voice
- hf (chat 9b): https://huggingface.co/THUDM/glm-4-voice-9b
- hf (tokenizer): https://huggingface.co/THUDM/glm-4-voice-tokenizer
- hf (decoder): https://huggingface.co/THUDM/glm-4-voice-decoder
- modelscope: https://modelscope.cn/models/ZhipuAI/glm-4-voice-9b
- 姊妹篇（tokenizer/decoder/交错数据来源）: https://arxiv.org/abs/2411.17607

## 一手源存档（sources/）
- [arxiv-2412.02612.pdf](https://arxiv.org/pdf/2412.02612)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/glm-4-voice--readme.md)
- [readme-en.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/glm-4-voice--readme-en.md)
- [hf-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/glm-4-voice--hf-modelcard.md)
