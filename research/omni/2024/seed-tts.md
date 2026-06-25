---
title: "Seed-TTS: A Family of High-Quality Versatile Speech Generation Models"
org: ByteDance
country: China
date: "2024-06"
type: tech-report
category: audio
tags: [tts, speech-synthesis, zero-shot, voice-cloning, autoregressive, diffusion, dit, rl, voice-conversion, in-context-learning]
url: "https://arxiv.org/abs/2406.02430"
arxiv: "https://arxiv.org/abs/2406.02430"
pdf_url: "https://arxiv.org/pdf/2406.02430"
github_url: "https://github.com/BytedanceSpeech/seed-tts-eval"
hf_url: ""
modelscope_url: ""
project_url: "https://bytedancespeech.github.io/seedtts_tech_report/"
downloaded: [arxiv-2406.02430.pdf, arxiv-2406.02430.txt, seed-tts--demo-page.md, seed-tts--eval-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Seed-TTS 是字节跳动 Seed 团队推出的大规模**自回归 TTS 基础模型家族**：以"语音 tokenizer + token 语言模型 + token 扩散模型 + 声码器"四件套，借海量数据（"比以往最大 TTS 系统大数个数量级"）实现**零样本音色克隆（in-context learning）**，并配套自蒸馏音色解耦与 RL 后训练；其零样本 ICL 在主观 CMOS 测试中达到 EN −0.07 / ZH −0.08（绝对值 < 0.1 即与真人**不可区分**），是首个在 in-the-wild 提示下"主观上与真人语音无法区分"的 TTS 系统。

## 背景与定位
此前 LM-based TTS（VALL-E、BASE-TTS、Mega-TTS 等）与 diffusion/NAR-based TTS（NaturalSpeech 3、Voicebox、E3-TTS 等）在零样本场景仍与真人有明显差距——报告称早期对这些系统做同口径主观评测时 CMOS 普遍 < −1。Seed-TTS 的核心命题是**把"文本 LLM 的 scaling 配方搬到语音"**：用数量级更大的数据与模型规模训练一个语音基座，让零样本音色克隆、跨语种、情感可控、语音风格迁移等能力作为"涌现能力"出现，逼近人类水平。

报告同时系统性地对比了语音生成的两大范式（LM-based vs diffusion-based），并给出三项扩展：自蒸馏音色解耦、RL 偏好对齐、纯扩散变体 Seed-TTS_DiT。相关脉络可参见 [[ddpm]] [[latent-diffusion-ldm]]（扩散）与基于神经 codec 的语言模型式 TTS（VALL-E 路线）。注意：本报告为**纯技术报告，不开源代码与权重**（仅出于 AI 安全考虑开放客观测试集），多数工程超参与精确数字刻意未披露。

## 模型架构
**整体为自回归 transformer 系统，推理管线四件套（Figure 1）：**

1. **语音 Tokenizer**：把语音波形转成语音 token 序列。报告同时探究了**连续 token 与离散 token 两种 tokenizer**，并强调"tokenizer 的设计对整个系统性能至关重要"（但未公开具体码本/帧率/RVQ 层数等细节）。
2. **Token 语言模型（自回归 transformer）**：在"文本 token + 语音 token"配对序列上训练，方法类似 Betker(2023, TorToiSe)、BASE-TTS、VALL-E。推理时基于条件文本与参考语音**自回归生成语音 token**。本报告聚焦语音生成，故**文本序列的 loss 被 mask 掉**。backbone 参考 LLaMA / 原始 Transformer 设计。
3. **Token 扩散 Transformer（Diffusion Transformer）**：以生成的语音 token 为条件，**由粗到细（coarse-to-fine）地生成连续语音表征**，补足声学细节。部署时采用**因果扩散架构（causal diffusion）**以支持流式处理、降低首包延迟。
4. **声学声码器（Acoustic Vocoder）**：单独训练，把扩散输出的连续表征还原为高质量波形；设计参考 Improved RVQGAN（DAC）、BigVGAN、Glow-WaveGAN、Basis-MelGAN。

**Seed-TTS_DiT（纯扩散非自回归变体）**：去掉扩散模型与声学 tokenizer 之间的依赖，**直接从高斯噪声、仅以输入文本为条件预测声码器的 latent 表征**，端到端处理。与以往 NAR-TTS 最大不同——**不依赖预估的音素时长（duration predictor）**：报告实验发现额外的 duration 预测模块会降低自然度，因此 DiT 改为**只预估整句总时长**、并优化"音频与文本的局部对齐（local alignment）"，从而动态调整每个音素时长。训练时给定音频 prompt、目标文本、与总时长等长的高斯噪声 clip，预测同等总时长的语音 latent，再由声码器转波形。该设计天然支持内容编辑与语速编辑（非流式）。

参数量 / 隐藏维度 / 层数 / 分辨率（采样率）等具体规模**均未披露**，仅定性说明"模型规模比以往语音生成模型大数个数量级"。

## 数据
- **规模**：仅定性表述——预训练使用的**数据量与模型规模"比以往最大的 TTS 系统大数个数量级"**，以最大化场景与说话人覆盖、建立稳健的通用语音建模骨干。**精确小时数、说话人数、语种配比、来源、清洗/过滤/标注流程均未披露**（与 BASE-TTS 公开"10 万小时"形成对比，Seed-TTS 刻意不给数字）。
- **语种**：至少覆盖英文（EN）与中文普通话（ZH），并支持跨语种生成（cross-lingual TTS）。
- **数据增强**：稳健性的提升来源之一是"数据增强"，但具体方法未展开。
- **自蒸馏合成数据**：在音色解耦扩展中，**用 Seed-TTS 自身生成"内容/韵律相同、音色不同"的合成语音对**（Sori 与 Salt），作为再训练扩散模型的数据（详见训练方法）。
- **评测集（已开放）**：客观测试集取自公开语料——**Common Voice 1,000 条 + DiDiSpeech-2 2,000 条**（EN/ZH）；主观集为内部 100 条 EN/ZH，含丰富口音、方言、情感、风格，因版权未释放。配置已开源于 seed-tts-eval。

## 训练方法
**三阶段（对齐文本 LLM 范式）：预训练 → 微调 → 后训练。**

- **预训练**：最大化场景与说话人覆盖，建立通用语音建模骨干；语言模型在文本+语音 token 配对序列上做 next-token 预测（文本部分 loss masked）。
- **微调**：分两类——
  - **Speaker fine-tuning (SFT)**：在选定说话人组上微调，并引入一个**说话人 index token** 在推理时选目标音色。实验中 5 个说话人共 20 小时数据，相对零样本 ICL 客观指标相近、主观 CMOS **+0.37**。
  - **Instruction fine-tuning (IFT)**：提升可控性与交互性，可灵活控制表现力、语速、风格、情感等。情感控制示例见 benchmark。
- **后训练（RL）**：用 **REINFORCE**（基于外部 reward model）在零样本 ICL 模型上微调出两个版本：
  - `RL-SIM-WER`：以 SIM 与 WER 客观指标为奖励，提升说话人相似度与稳健性；
  - `RL-SER`：以语音情感识别（SER）模型准确率为奖励，提升情感可控性。
  报告还对比了"有外部 reward 的 PPO/REINFORCE"与"无外部 reward 的 DPO"：两者皆有效，前者能精确控制特定语音属性、后者实现更简单（本报告主展前者）。明确观测到 **reward hacking**——为降 WER 模型倾向放慢、念得过于清晰而牺牲自然度，需仔细调参权衡。

**扩展一：自蒸馏音色解耦（speech factorization by self-distillation）。** 不靠 feature engineering / 专门 loss / 改网络结构，而是**构造"大部分信息相同、仅目标属性不同"的可控语音对**。具体：在扩散模块生成时引入**说话人扰动（speaker perturbation）**，得到内容与韵律一致但音色偏移的 Salt 与原始 Sori。再训练扩散模型时**以 Salt 的 token 为输入、以 Sori 的音色参考为条件，优化恢复 Sori 的声码器 embedding**——网络被迫忽略 token 里携带的音色、仅依赖外部音色参考，从而实现高质量音色解耦，直接用于零样本语音转换（VC）。

**加速/蒸馏（部署）**：扩散侧用 **consistency distillation** + **改进的 flow matching（Esser et al. 2024，SD3 路线）** 降低扩散计算成本；并采用因果扩散支持流式。

## Infra（训练 / 推理工程）
- **训练算力 / GPU·时 / 并行策略 / 精度 / 吞吐：未披露。**
- **推理与部署优化**（重点工程贡献，定性披露技术清单）：
  - 扩散侧：**因果扩散架构**（流式、降首包延迟）+ **consistency distillation** + 改进 flow matching（降步数/算力）。
  - 语言模型侧：**GQA（grouped-query attention）**、**paged attention（vLLM 路线）**、**flash attention**、**模型量化**降显存与算力。
- **部署效果（Table 5）**：相比离线模型，部署模型 **延迟降至 0.028×、RTF 降至 0.132×**，而 **WER（1.518）与 SIM（0.763）保持不变**，CMOS **−0.02**（与离线无显著差异）。即在质量几乎无损下大幅压低延迟与实时率。
- **部署形态**：仅以 ByteDance 产品内提供语音生成能力，不开源权重。

## 评测 benchmark（把效果讲清楚）
**评测协议**：WER 用 Whisper-large-v3（EN）/ Paraformer-zh（ZH）；SIM 用 WavLM-large 微调的说话人验证模型算 cos 相似度；主观用 CMOS（−2~+2，绝对值 < 0.1 视为两系统无显著差异）。

**零样本 ICL vs 真人（Table 1，客观集 + 主观集）**：
| 系统 | 语种 | WER↓ | SIM↑ | CMOS vs 真人↑ |
|---|---|---|---|---|
| Seed-TTS | EN | 2.249 | 0.762 | −0.07 |
| Vocoder 重合成 | EN | 2.165 | 0.702 | −0.08 |
| 真人 | EN | 2.143 | 0.730 | — |
| Seed-TTS | ZH | 1.115 | 0.796 | — |
| Vocoder 重合成 | ZH | 1.342 | 0.733 | — |
| 真人 | ZH | 1.254 | 0.750 | — |

（注：CMOS 列原报告仅对 EN 主观集给出 −0.07 / −0.08；ZH 主观 CMOS 与 Vocoder 重合成的 CMOS 报告未列具体数。）

→ Seed-TTS 的 WER 与真人接近，**SIM 显著高于真人**（因真人 GT 与参考音在风格/环境上仍有差异，而模型更忠实复刻参考）；主观上**与真人不可区分**（首次）。报告指出更低 WER 不必然带来更高主观相似度（过低 WER 往往是"标准化"语音、丢失口音与表现力）。

**vs 传统 speaker-finetune TTS（Figure 2）**：零样本 ICL（15s prompt）vs FastSpeech 路线（每人约 5 小时数据微调）。"普通"说话人组上 ICL 被偏好 **47.9%**，自然度与表现力优势明显；"困难"说话人组（强口音/夸张风格）传统微调更强。

**语音理解侧验证（Table 2）**：用 Seed-TTS 合成 LibriSpeech 960h（"text-wave shuffling"策略）训 ASR（12 层 Squeezeformer 编码器 + 3 层双向 transformer 解码器，WeNet）——clean 集（dev_clean/test_clean：合成 2.59/2.76 vs 真实 2.26/2.45）几乎持平，noisy 集（dev_other/test_other：合成 7.78/7.58 vs 真实 5.97/5.98）分别落后 1.81%/1.6% 绝对 WER（推测因生成时降噪导致噪声鲁棒性差）。另用 VoxCeleb1 25 说话人做 t-SNE（Figure 3），合成与真实嵌入同说话人可靠聚类。说明合成语音可用于语音理解，推动"理解-生成统一"。

**Speaker fine-tuning（Table 3）**：SFT vs ICL：WER 2.83 vs 3.15、SIM 0.789 vs 0.779、**CMOS +0.37**（SFT 更佳，捕捉更细微韵律与句尾发音）。

**情感可控（Table 4，IFT）**：无显式控制信号时 SFT 已有中等准确率（angry 0.69 / happy 0.4 / sad 0.37 / surprise 0.22）；加控制信号后 IFT **angry 1.0 / happy 0.85 / sad 1.0 / surprise 0.98**。

**RL（Table 7–9）**：`RL-SIM-WER` vs ICL——ZH WER 1.002 vs 1.115、EN 1.945 vs 2.249、Hard 6.423 vs 7.585，SIM 全面小升；主观 CMOS **+0.14**（Win 44.1% / Tie 25% / Loss 30.9%）。`RL-SER` vs ICL 情感准确率：angry 0.91 vs 0.46、happy 0.8 vs 0.44、sad 0.78 vs 0.53、surprise 0.82 vs 0.13。

**零样本语音转换（Table 6，自蒸馏）**：EN 非平行——Seed-TTS w/ self-distillation **WER 2.121 / SIM 0.753**，远超 HierSpeech++（5.469 / 0.387）与 DiffVC（16.861 / 0.311）；自蒸馏使 SIM 从 0.491（无自蒸馏）跃升至 0.753。ZH 非平行 WER 1.216 / SIM 0.791。

**Seed-TTS_DiT（Table 10，纯扩散零样本 TTS）**：EN WER **1.733** / SIM **0.790**、ZH WER 1.178 / SIM **0.809**，**SIM 优于 ICL 版、WER 相近**，显示扩散对序列建模的强能力。语音编辑：内容编辑在 0%–60% mask 比例下 WER/SIM 稳健（Figure 6）；语速编辑 0.7×–1.3× 速率下保持高相似度，速率过高时 WER 略降（Figure 7）。

## 创新点与影响
**核心贡献**：
1. **首个达到"与真人不可区分"的零样本 TTS**：把 LLM scaling 配方迁移到语音基座，零样本 ICL 主观 CMOS 进入 ±0.1 区间。
2. **自蒸馏音色解耦**：不改结构/loss，用模型自产的"控制变量"语音对实现高质量音色解耦，VC SOTA。
3. **RL 后训练系统化用于 TTS**：REINFORCE + 外部 reward（SIM/WER/SER）整体提升稳健性、相似度、情感可控性，并诚实报告 reward hacking。
4. **Seed-TTS_DiT**：摆脱 duration predictor 的端到端纯扩散 NAR，仅预测总时长 + 局部对齐，原生支持内容/语速编辑。
5. **开放 seed-tts-eval 客观测试集**（Common Voice + DiDiSpeech-2，含 ZH hardcase），为零样本 TTS 设立可复现 benchmark。

**影响**：Seed-TTS 是字节 Seed 语音线的基座，后续 Seed 系列（如后续语音/对话与 codec 工作）与产品落地的起点；其"LM+扩散两段式 + 自蒸馏解耦 + RL"范式被语音社区广泛参考，开放测试集成为零样本 TTS 的常用评测基准。

**已知局限**：①不开源代码与权重；②精确数据规模/参数量/算力刻意未披露，复现性受限；③不擅长唱歌、含背景音乐/强噪声的 prompt（常忽略音乐）；④长文本生成韵律变化少于真人（拟用 multi-shot ICL 缓解）；⑤"困难"强口音说话人零样本仍弱于传统微调；⑥RL 存在 reward hacking 需调参权衡。安全上采用多步说话人/内容核验 + 多层强制水印。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2406.02430
- arxiv_pdf: https://arxiv.org/pdf/2406.02430
- project_page (官方 demo/技术报告页): https://bytedancespeech.github.io/seedtts_tech_report/
- github (官方客观测试集 seed-tts-eval): https://github.com/BytedanceSpeech/seed-tts-eval

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2406.02430.pdf
- ../../../sources/omni/2024/arxiv-2406.02430.txt
- ../../../sources/omni/2024/seed-tts--demo-page.md
- ../../../sources/omni/2024/seed-tts--eval-readme.md
