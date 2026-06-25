---
title: "Qwen2-Audio"
org: "Alibaba (Qwen Team)"
country: China
date: "2024-07"
type: tech-report
category: audio
tags: [audio-language-model, lalm, speech, asr, s2tt, voice-chat, dpo, whisper, qwen]
url: "https://qwenlm.github.io/blog/qwen2-audio/"
arxiv: "https://arxiv.org/abs/2407.10759"
pdf_url: "https://arxiv.org/pdf/2407.10759"
github_url: "https://github.com/QwenLM/Qwen2-Audio"
hf_url: "https://huggingface.co/Qwen/Qwen2-Audio-7B-Instruct"
modelscope_url: "https://modelscope.cn/models/qwen/Qwen2-Audio-7B"
project_url: "https://qwenlm.github.io/blog/qwen2-audio/"
downloaded: [arxiv-2407.10759.pdf, qwen2-audio--readme.md, qwen2-audio--hf-modelcard.md, qwen2-audio--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Qwen2-Audio 是阿里通义千问团队 2024 年 7 月发布的 **8.2B 大音频-语言模型（LALM）**，以 Whisper-large-v3 音频编码器 + Qwen-7B LLM 接一层 next-token 训练，统一处理语音/声音/音乐输入并直接输出文本；最大创新是**用自然语言 prompt 取代上一代复杂的层级标签**、并首次让模型**无需 ASR 模块直接听语音指令做"语音对话（Voice Chat）"**，配合 SFT + DPO，在 AIR-Bench 指令遵循基准上**超过 Gemini-1.5-pro**（Speech 7.18 / Sound 6.99 / Music 6.79 / Mixed 6.77）。

## 背景与定位
- 解决的问题：上一代 [[qwen-audio]]（2023.11）虽统一了多任务音频理解，但预训练依赖**层级化的特殊标签体系**（hierarchical tags）来区分任务/语言，与下游自然语言交互存在 gap，且指令遵循能力不足、不能直接做语音对话。Qwen2-Audio 的核心目标是**提升指令遵循（instruction-following）能力**并打通语音交互。
- 技术脉络位置：属于"音频编码器 + LLM"的 LALM 路线，与 SALMONN、SpeechVerse、Audio Flamingo、Pengi、SpeechGPT、Gemini-1.5-pro 同期竞争；本工作沿用 Qwen-VL/Qwen-Audio 把 Qwen LLM 扩展到更多模态的整体战略。
- 相对前置工作的改进：(1) 预训练**改用自然语言 prompt** 替代层级标签，提升泛化与指令遵循；(2) **扩大训练数据量**；(3) 后训练加入 **SFT + DPO** 对齐人类偏好；(4) 设计 **Voice Chat / Audio Analysis 两种交互模式且无需系统 prompt 切换**。
- 它是后续 [[qwen2.5-omni]] 全模态能力（含 Talker 音频生成）的前身理解组件；本身**只做音频理解、只输出文本，不生成音频**。

## 模型架构
- **整体**：audio encoder + LLM 两段式，训练目标是在音频表征条件下最大化下一个文本 token 概率 `Pθ(x_t | x_<t, Encoder_φ(a))`，即标准的 next-token prediction（θ、φ 分别为 LLM 与音频编码器的可训练参数）。
- **音频编码器**：基于 **Whisper-large-v3** 初始化（与 Qwen-Audio 不同，上一代不是基于 large-v3）。预处理：音频重采样到 **16 kHz**，转 **128 通道 mel-spectrogram**，窗长 **25 ms**、hop **10 ms**；编码器后接一个 **stride=2 的 pooling 层**压缩序列长度，使每帧输出约对应原始音频 **40 ms**。
- **LLM backbone**：沿用 **Qwen-7B**（Bai et al., 2023）作为基础语言模型。
- **总参数量**：**8.2B**（HF 模型仓库标注 7B 系列；论文给出 8.2B 含音频编码器）。
- **条件注入方式**：音频经编码器得到连续表征后与文本 token 序列拼接进 LLM；推理用 ChatML 对话格式，特殊 token `<|audio_bos|> <|AUDIO|> <|audio_eos|>` 标记音频片段位置。
- **两种交互模式（同一模型、联合训练、无需系统 prompt 区分）**：
  - **Audio Analysis**：用户给音频 + 文本指令做离线分析（语音/声音/音乐/混合音频均可），指令可来自文本或音频本身，模型自主辨别音频里哪段是指令。
  - **Voice Chat**：用户直接用语音对话、无需文字输入，模型像语音助手一样应答；可随时切到文字交互。
- 已知约束：模型**对 30 秒以内的音频片段表现最佳**（README / 博客明示）。
- 发布两款权重：**Qwen2-Audio-7B**（预训练 base）与 **Qwen2-Audio-7B-Instruct**（chat 模型）。

## 数据
- **预训练数据**：论文称在 Qwen-Audio 基础上**进一步扩大数据规模**，并将层级标签**改为自然语言 prompt** 来标注不同数据与任务（如 ASR 用 "Detect the language and recognize the speech:"、音频字幕用 "Generate the caption in English:"）。**各任务小时数仅以图（Figure 3 "Statistics (hours) of pre-training dataset"）形式给出，正文未列具体数值**——此处不臆造具体小时数。
- **任务覆盖**：ASR、音频字幕/AAC（Audio Captioning）、语音翻译、声音分类等多任务统一预训练。
- **多语言**：支持 **8 种以上语言与方言**——中文、英文、粤语、法语、意大利语、西班牙语、德语、日语（博客披露）。
- **SFT 数据**：强调 **SFT 数据的质量与复杂度对最终性能至关重要**，因此精心筛选了高质量 SFT 数据并施加严格质量控制；通过提升 SFT 数据的**数量、质量、复杂度**来增强人机交互对齐。具体规模/来源**未披露**。
- **DPO 偏好数据**：三元组 `(x, y_w, y_l)`，x 为含音频的输入，y_w / y_l 为**人工标注**的优/劣回答；规模与构造细节**未披露**。
- 数据去重/防泄漏：评测数据集被**严格排除出训练数据**以避免数据泄漏。

## 训练方法
**三阶段流水线（Pretrain → SFT → DPO，见 Figure 2）**：
1. **多任务预训练（Multi-Task Pre-training）**：以 next-token prediction 为目标做音频-语言对齐，用**自然语言 prompt** 代替层级标签。论文发现"语言 prompt 能带来更好的泛化能力与指令遵循能力"。
2. **监督微调（SFT / Instruction Tuning）**：在充分预训练得到的音频理解能力上做指令式微调，得到可交互的 chat 模型；Voice Chat 与 Audio Analysis 两种模式**联合训练**，用户使用时无感切换、不需要不同系统 prompt。
3. **直接偏好优化（DPO）**：用 DPO（Rafailov et al., 2024）进一步对齐人类偏好，loss 即标准 DPO 形式
   `L_DPO = -E[(x,y_w,y_l)] log σ( β·log(Pθ(y_w|x)/P_ref(y_w|x)) − β·log(Pθ(y_l|x)/P_ref(y_l|x)) )`，
   参考模型 `P_ref` 用 SFT 后的 `Pθ` 初始化；β 为温度超参（具体值未披露）。DPO 主要改善**事实性（factuality）与对期望行为的遵循**。
- **加速/蒸馏**：本工作**未涉及** consistency/LCM/ADD 等扩散加速（非扩散模型，是自回归 LALM）。
- 关键超参（学习率、batch、训练步数、β 等）论文**未披露**。

## Infra（训练 / 推理工程）
- **算力 / GPU·时 / 并行策略 / 混合精度 / 吞吐**：论文与博客**均未披露**任何训练 infra 数字（GPU 数量、卡时、并行方式、精度等都没给）。
- **推理 / 部署**：已并入 Hugging Face Transformers（`Qwen2AudioForConditionalGeneration`），支持 voice chat / audio analysis / batch 推理；提供 ModelScope（推荐国内用户）与 HF 权重、Web UI demo（`demo/web_demo_audio.py`）。
- 工程注记：README 指出**原始训练框架的初始模型分数**与**转换到 HuggingFace 框架后的分数有小幅波动**，两套数字都公开了（见下表）。
- 推理实践约束：**音频片段建议 < 30 秒**效果最佳。
- 许可证：**Apache-2.0**（HF 卡标注），商用无需额外申请。

## 评测 benchmark（把效果讲清楚）
评测覆盖 **13 个标准数据集**，任务含 ASR / S2TT / SER / VSC 与 AIR-Bench chat 指令遵循；评测集严格剔除出训练集。论文明确**以 AIR-Bench 为主评测**——团队称许多传统测试集（部分 SLU/SER）受限、难反映真实场景，而 AIR-Bench 分数"与真实用户交互体验更吻合"，传统 ASR/S2TT/SER/VSC 只作通用能力补充验证。下列数字均来自论文 Table 2 与 GitHub README（标注"论文初始框架"与"转 HF 后"两版）。

**ASR — WER↓**
- LibriSpeech（dev-clean | dev-other | test-clean | test-other）：Qwen2-Audio **1.3 | 3.4 | 1.6 | 3.6**（论文）/ **1.7 | 3.6 | 1.7 | 4.0**（转 HF 后）。优于 Qwen-Audio（1.8 | 4.0 | 2.0 | 4.2）、SpeechVerse（test-clean/other 2.1 | 4.4）、SALMONN 等。
- Common Voice 15（en | zh | yue | fr）：**8.6 | 6.9 | 5.9 | 9.6**（论文）vs Whisper-large-v3 的 9.3 | 12.8 | 10.9 | 10.8（注：Qwen2-Audio 非 zero-shot，Whisper 为 zero-shot）。
- Fleurs-zh（zero-shot）：**7.5**（论文）/ **7.0**（HF），优于 Whisper-large-v3 的 7.7。
- Aishell2（Mic | iOS | Android）：**3.0 | 3.0 | 2.9**（论文），与 Paraformer-large（iOS 2.9）相当并整体领先 Qwen-Audio。

**S2TT — BLEU↑（CoVoST2）**
- en-de | de-en | en-zh | zh-en：Qwen2-Audio **29.9 | 35.2 | 45.2 | 24.4**（论文），全面超过 Qwen-Audio（25.1 | 33.9 | 41.5 | 15.7）与 SALMONN / SpeechLLaMA / BLSP。
- es-en | fr-en | it-en：**40.0 | 38.5 | 36.3**（论文），优于 SpeechLLaMA（27.9 | 25.2 | 25.9）。
- 论文宣称在**全部 7 个翻译方向**上大幅领先 baseline。

**SER — ACC↑（Meld）**：Qwen2-Audio **0.553**（论文）/ 0.535（HF）；Qwen-Audio 0.557、WavLM-large 0.542（此项与 Qwen-Audio 互有高低）。

**VSC — ACC↑（VocalSound）**：Qwen2-Audio **0.9392**（论文）/ 0.9395（HF），SOTA；优于 Qwen-Audio 0.9289、Pengi 0.6035、CLAP 0.4945。

**AIR-Bench Chat（GPT-4 打分 0–10，↑）Speech | Sound | Music | Mixed-Audio**
- **Qwen2-Audio：7.18 | 6.99 | 6.79 | 6.77**（论文）/ 7.24 | 6.83 | 6.73 | 6.42（HF）。
- Qwen-Audio：6.47 | 6.95 | 5.52 | 6.08；**Gemini-1.5-pro：6.97 | 5.49 | 5.06 | 5.27**；SALMONN：6.16 | 6.28 | 5.95 | 6.08。
- 结论：Qwen2-Audio 在**全部四个子集**上取得 SOTA 指令遵循表现，**超过 Gemini-1.5-pro**（论文注：Gemini-1.5 因安全原因约 1/5 测试样本无法返回，样本数被相应缩减）。

**关键结论/消融**：论文的核心方法论结论是"**用自然语言 prompt 替代层级标签可提升泛化与指令遵循能力**"，以及"**SFT 数据的质量与复杂度对性能有决定性影响**"；但论文**未提供专门的消融对照表**来量化这两点（属定性陈述）。模型在**无任何 task-specific 微调**下即取得上述成绩。

## 创新点与影响
**核心贡献**
1. **自然语言 prompt 预训练**：抛弃 Qwen-Audio 的层级标签，简化预训练并缩小 pre/post-training gap，提升指令遵循与泛化。
2. **Voice Chat 模式**：首次让 LALM **无需独立 ASR 模块**直接听语音指令应答，且与 Audio Analysis 统一为一个模型、无需系统 prompt 切换。
3. **后训练对齐**：在音频 LALM 上引入 **SFT + DPO** 流水线，DPO 显著改善事实性与行为遵循——这是当时 LALM 较少采用偏好对齐的早期实践之一。
4. **开源开放权重**（Apache-2.0，base + instruct 两款），并入 HF Transformers，推动多模态社区。

**影响**
- 作为 **Qwen2.5-Omni** 全模态模型的音频理解前身组件，其编码器/对齐范式被后续 Qwen 全模态工作继承；语音指令直接交互的范式预示了 GPT-4o 式语音助手方向。
- AIR-Bench 上超过 Gemini-1.5-pro，确立了开源 LALM 在音频指令遵循上的竞争力标杆。

**已知局限**
- **只理解、不生成音频**（无 TTS/Talker，纯文本输出）；音频生成要到 Qwen2.5-Omni。
- **长音频受限**：建议 < 30 秒，长音频支持为未来工作。
- **训练 infra、数据小时数、SFT/DPO 数据规模与关键超参均未披露**，复现成本高。
- 论文偏短（technical report 体量），缺少系统化消融实验。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2407.10759
- arxiv_pdf: https://arxiv.org/pdf/2407.10759
- github: https://github.com/QwenLM/Qwen2-Audio
- blog (官方，一等公民): https://qwenlm.github.io/blog/qwen2-audio/
- hf model (Instruct): https://huggingface.co/Qwen/Qwen2-Audio-7B-Instruct
- hf model (base): https://huggingface.co/Qwen/Qwen2-Audio-7B
- modelscope: https://modelscope.cn/models/qwen/Qwen2-Audio-7B
- demo: https://huggingface.co/spaces/Qwen/Qwen2-Audio-Instruct-Demo

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2407.10759.pdf （论文全文，已精读；PDF 被 .gitignore 排除不入 git）
- ../../../sources/omni/2024/qwen2-audio--readme.md （GitHub README，含论文版 + HF 转换版双套 benchmark 数字）
- ../../../sources/omni/2024/qwen2-audio--hf-modelcard.md （HF Qwen2-Audio-7B-Instruct 模型卡）
- ../../../sources/omni/2024/qwen2-audio--blog.md （官方博客快照，含多语言/无 ASR/scaling 未来计划）
