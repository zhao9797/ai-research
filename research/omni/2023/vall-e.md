---
title: "VALL-E: Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers"
org: "Microsoft"
country: US
date: "2023-01"
type: paper
category: audio
tags: [tts, zero-shot, voice-cloning, neural-codec, audio-lm, in-context-learning, encodec, autoregressive]
url: "https://arxiv.org/abs/2301.02111"
arxiv: "https://arxiv.org/abs/2301.02111"
pdf_url: "https://arxiv.org/pdf/2301.02111"
github_url: "https://github.com/microsoft/unilm/tree/master/valle"
hf_url: ""
modelscope_url: ""
project_url: "https://www.microsoft.com/en-us/research/project/vall-e-x/"
downloaded: [arxiv-2301.02111.pdf, arxiv-2301.02111.txt, vall-e--unilm-readme.md, vall-e--msr-project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
VALL-E 是首个把 TTS 当成「神经 codec token 的条件语言建模」来做的框架：用现成神经音频 codec（EnCodec）把语音离散成 token，再训一个 GPT 风格的解码器 LM 来预测这些 token，从而**只用 3 秒目标说话人录音作为声学提示就能零样本克隆音色**，并涌现出文本 LM 那样的 in-context learning 能力。在 LibriSpeech 上相对当时 SOTA 零样本 TTS（YourTTS）取得 +0.12 CMOS（自然度）与 +0.93 SMOS（说话人相似度）的提升，并能保留提示音频的情绪与声学环境。

## 背景与定位
传统 TTS（FastSpeech、Tacotron 系）是**级联管线**：phoneme → mel 频谱 → 波形（vocoder），以连续信号回归为目标。它们依赖录音棚级别的干净数据，训练量通常只有几十~几百小时单/多说话人数据（论文给的对照是 ≤600 小时），对**未见说话人（unseen speaker）泛化差**，零样本场景下自然度和相似度都急剧下降。已有零样本方案靠 speaker adaptation（需微调）或 speaker encoding（需预训练 speaker encoder、复杂特征工程），都很笨重。

VALL-E 的核心立意是把文本 LLM 的成功范式（GPT-3：海量多样数据 + 自回归语言建模 + prompting 触发 in-context learning）**迁移到语音**。关键前置工作：
- [[encodec]]（Défossez 2022，本文的离散化 tokenizer），以及 [[soundstream]] 这类神经音频 codec —— 提供「波形↔离散 token」可逆映射，且 codec token 保留说话人身份与录音环境信息（这是相对 HuBERT/w2v-BERT 语义 token 的关键差异，后者丢失了音色）。
- AudioLM（Borsos 2022）—— 先把神经 codec token 用 LM 建模做语音续写；但 AudioLM 是 speech-to-speech、无法显式控制内容（文本），VALL-E 则是 TTS，可由 phoneme 显式控制内容。
- GPT-3（Brown 2020）—— in-context learning / prompting 的范式来源。

定位：**神经 codec LM TTS 的奠基工作**，开创了「audio codec code 作为中间表示 + LM 自回归生成」这条路线，直接催生后续 VALL-E X / VALL-E R / VALL-E 2 / MELLE 以及社区的大量 codec-LM TTS（如开源复现等）。

## 模型架构
整体 pipeline：**phoneme → discrete codec code → waveform**（取代传统 phoneme → mel → waveform）。

**Tokenizer（EnCodec）**：采用预训练的 EnCodec，卷积 encoder-decoder，24 kHz 音频输入输出。encoder 把 24 kHz 波形下采样到 75 Hz 的 embedding（320 倍下采样），每个 embedding 用 **残差矢量量化 RVQ** 量化为 **8 个层级量化器（quantizer）**、每个 codebook 1024 项 —— 对应 6 kbps 码率。于是一段 10 秒音频 = 750 × 8 的离散 token 矩阵 `C`（750 = 24000×10/320 帧，8 = 量化器数）。RVQ 的关键性质：**第一个量化器承载最主要的重建信息（含说话人身份等粗粒度声学属性），后续量化器逐级建模残差细节**——这是 VALL-E 分层建模设计的物理依据。

**两段式条件 codec LM（核心设计）**，利用 RVQ 的层级结构拆成 AR + NAR 两个模型：

1. **AR 模型（第一量化器）**：decoder-only 因果 Transformer，对第 1 层 codebook 的 token 序列 `c_{:,1}` 做自回归 next-token 预测，条件是 phoneme 序列 `x` 和声学提示 `C̃_{:,1}`。组成：phoneme embedding `W_x`、acoustic embedding `W_a`、Transformer 解码器、预测头；输出投影层与 acoustic embedding `W_a` **共享权重**。输入是 `x` 与 `c_{:,1}` 的拼接，各自后接 `<EOS>`，prompt 与输入分别计算正弦位置编码。训练是**纯因果 LM**——不显式切出 prompt 片段，任意前缀 `c_{<t,1}` 都被当成后续的 prompt（这正是 in-context learning 的来源）。

2. **NAR 模型（第 2~8 量化器）**：与 AR 同构 Transformer，但有 **8 个独立的 acoustic embedding 层**。每训练步随机采一个 stage `i∈[2,8]`，用前 1..i-1 层 token 之和作为输入、预测第 i 层 codebook。注意力是**全注意力（非因果）**，可一次并行生成整层。当前 stage `i` 通过 **Adaptive LayerNorm（AdaLN）** 注入：`AdaLN(h,i)=a_i·LayerNorm(h)+b_i`，`a_i,b_i` 由 stage embedding 线性投影得到。第 j 个预测层权重与第 (j+1) 个 acoustic embedding 层**共享**。声学提示 `C̃`（8 层 embedding 求和）用来约束说话人身份。

**为什么 AR + NAR 混合**：AR 负责第 1 层——因为生成语音的时长要和提示录音的语速一致，而不同说话人语速差异大、难训练长度预测器，自回归天然能灵活决定序列长度；NAR 负责后 7 层——输出槽位数已由第 1 层长度确定，可把时间复杂度从 O(T) 降到 O(1)。最终联合分布：`p(C|x,C̃)=p(c_{:,1}|C̃_{:,1},x;θ_AR)·∏_{j=2}^{8} p(c_{:,j}|c_{:,<j},x,C̃;θ_NAR)`。实际推理时 NAR 解码器被调用 7 次（生成 7 个量化器）。

**参数规模**：AR 与 NAR 均为 12 层 Transformer、16 注意力头、embedding 维度 1024、FFN 维度 4096、dropout 0.1。论文未给出总参数量数字（按此配置每个约 ~1.6 亿级别，但论文未明确报告）。

## 数据
- **训练集**：LibriLight（Kahn 2020）—— **60K 小时**英语有声书语音，约 **7000 个不同说话人**。原始数据是 audio-only（无转写）。
- **转写生成（半监督）**：因 LibriLight 无文本，作者在 960 小时有标注的 LibriSpeech 上按 Kaldi recipe 训练一个 **hybrid DNN-HMM ASR**，再对 60K 小时无标注语音解码，得到 **phoneme 级强制对齐路径**，帧移 30 ms。即文本侧用的是「伪 phoneme」而非人工转写。
- **离散化**：用 EnCodec 对全部 60K 小时音频生成 8 层声学 code 矩阵。
- **规模对比**：作者强调这比既有 TTS 训练数据（数十小时单说话人 / 数百小时多说话人）**大数百倍**；代价是数据更嘈杂、转写不精确，但说话人与韵律更多样，作者主张大规模数据能让模型对噪声鲁棒并良好泛化。
- **数据局限（作者自述）**：LibriLight 是有声书，多为**朗读风格**，口音说话人覆盖不足（这解释了在含多口音的 VCTK 上相似度更难做高）。
- 美学/安全过滤、再加注（re-captioning）等：TTS 任务不涉及图像 caption，论文**未涉及**额外的内容安全过滤流程（仅在 broader impact 讨论了滥用风险与检测模型设想）。

## 训练方法
- **训练目标**：纯**语言建模**——AR 部分是标准 next-token 交叉熵（最大化第 1 层 token 的下一个 token 概率）；NAR 部分是在随机采样的 stage i 上最大化该层 codebook token 的概率。**没有 diffusion / flow matching / mel 回归**，这是与同期扩散 TTS（Grad-TTS、Guided-TTS 等）的根本区别。
- **训练数据切片**：LibriLight 平均波形 60 秒；训练时**随机裁剪到 10~20 秒**之间的随机长度，对应 phoneme 对齐作为 phoneme prompt；强制对齐 phoneme 序列里**去掉连续重复**。NAR 的声学 prompt token 从同一条 utterance 里**随机取 3 秒**片段。
- **优化器/超参**：AdamW；学习率前 32k 步 warmup 到峰值 **5×10⁻⁴**，之后线性衰减；训练 **800k 步**，每 GPU batch = **6k 声学 token**。
- **多阶段 / 偏好对齐**：VALL-E 是**单阶段预训练**，**无 SFT、无 RLHF/DPO、无 reward model、无蒸馏/步数压缩**——这些在本工作中均未使用。
- **推理（in-context learning via prompting）**：
  - 文本→phoneme（G2P），录音→EnCodec 声学矩阵，构成 phoneme prompt 与 acoustic prompt，AR/NAR 都用。
  - AR 用**基于采样的解码**（不用 beam search，作者发现 beam search 会让 LM 陷入无限循环；采样还能显著增加输出多样性）；NAR 用 **greedy 解码**。
  - 最后用 EnCodec 解码器把 8 层 code 还原成 24 kHz 波形。
  - 两种 prompt 设置：**VALL-E**（把 enrolled 录音的转写 phoneme 前置到目标句 phoneme，并用 enrolled 录音第 1 层声学 token 作前缀）；**VALL-E-continual**（用整句转写 + 真值前 3 秒做 prompt，让模型续写，语义连续）。

## Infra（训练 / 推理工程）
- **算力**：**16 张 NVIDIA Tesla V100 32GB**，每卡 batch 6k token，训练 800k 步。论文未报告总 GPU·时、并行/分布式策略、混合精度细节与吞吐。
- **推理形态**：AR 逐 token 自回归生成第 1 层（O(T)），NAR 并行生成第 2~8 层（被调用 7 次，每次 O(1)），相对全自回归 8 层显著省时间；这是 AR+NAR 混合的工程动机之一。具体延迟/RTF、量化、缓存等推理加速数字**未报告**。
- **部署/开源**：VALL-E **未开源权重，也未提供可调用模型/HF checkpoint**——`microsoft/unilm` 下的 `valle/README.md` 仅含 demo 页链接与 preprint 链接，无代码与权重；项目以 demo 页（aka.ms/valle）+ MSR 项目页形式发布。（社区另有第三方非官方复现，但非本工作一手产物。）

## 评测 benchmark（把效果讲清楚）
评测集均为**训练中未见说话人**：LibriSpeech test-clean（与 LibriLight 无说话人重叠）、VCTK（108 说话人）。Baseline 为当时 SOTA 零样本 TTS **YourTTS**。自动指标：用 **WavLM-TDNN**（VoxSRC 2021/2022 冠军）算说话人相似度 SPK（[-1,1]）；用在 LibriSpeech 960h 上微调的 **HuBERT-Large CTC ASR** 算 WER 衡量鲁棒性。人评：CMOS（自然度，-3~+3）、SMOS（相似度，1~5）。

**LibriSpeech 客观（Table 2，WER↓ / SPK↑）**：
| 模型 | 类型 | WER | SPK |
|---|---|---|---|
| GroundTruth | — | 2.2 | 0.754 |
| GSLM | speech→speech | 12.4 | 0.126 |
| AudioLM* | speech→speech | 6.0 | —（未开源无法测 SPK） |
| YourTTS | TTS | 7.7 | 0.337 |
| **VALL-E** | TTS | **5.9** | **0.580** |
| **VALL-E-continual** | TTS | **3.8** | **0.508** |

VALL-E 在鲁棒性（WER 5.9 vs YourTTS 7.7）和相似度（SPK 0.580 vs 0.337）上都大幅领先 baseline；continual 设置因前 3 秒声学 token 来自真值，WER 进一步降到 3.8。作者归因：VALL-E 用 pseudo-phoneme（而非 HuBERT/w2v-BERT 语义 code）输入，与文本对齐质量更好，故 WER 优于 GSLM/AudioLM 这类 speech-to-speech LM。

**LibriSpeech 人评（Table 3，40 说话人，3 秒提示）**：
- SMOS：YourTTS 3.45 / **VALL-E 4.38** / GroundTruth 4.5 —— VALL-E 比 baseline **+0.93 SMOS**，已非常接近真值。
- CMOS（相对 VALL-E）：YourTTS −0.12（即 VALL-E **+0.12** 自然度优于 YourTTS），GroundTruth +0.17。

**VCTK 客观（Table 6，SPK，108 全说话人 / 11 未见说话人，3s/5s/10s 提示）**：VALL-E 全面优于 YourTTS——**即便 YourTTS 训练时见过 VCTK 的 97 个说话人，而 VALL-E 一个都没见过**。例：11 未见说话人 3s 提示下 VALL-E 0.389 vs YourTTS 0.331；提示越长相似度越高（VALL-E 11 unseen：3s 0.389 → 5s 0.528... 注：原表 5s/10s 数字随提示增长上升），符合直觉。
**VCTK 人评（Table 7，60 说话人，3 秒提示）**：SMOS YourTTS 3.70 / **VALL-E 3.81** / GroundTruth 4.29；CMOS（相对 VALL-E）YourTTS **−0.23**（VALL-E +0.23 优于 baseline）、GroundTruth **−0.04**——即 VALL-E 自然度与真人录音**无统计显著差异**（在 VCTK 上）。

**消融**：
- NAR prompt 消融（Table 4，输入用真值第 1 层 token）：无任何 prompt WER 19.6 / SPK 0.518 → 加 phoneme prompt WER 骤降到 3.0（phoneme 主要贡献内容）→ 双 prompt（phoneme+声学）SPK 升到 0.732（声学 prompt 贡献说话人身份）。
- AR prompt 消融（Table 5）：去掉 AR 的声学 prompt，SPK 从 0.585 跌到 0.236（WER 不变 5.9）——说明即便 NAR 能看到 prompt，AR 的声学 prompt 对说话人相似度仍极关键。

**定性发现**：(1) 多样性——采样解码使同一文本+说话人两次推理产出不同语速/重音/时长（传统 mel 回归 TTS 是确定性一对一映射），可用于为 ASR 造伪数据；(2) **声学环境保持**——提示有混响时合成也带混响（baseline 输出干净语音）；(3) **情绪保持**——用 EmoV-DB 含 5 种情绪的提示，零样本保留提示情绪，无需在情绪 TTS 数据上微调。

## 创新点与影响
**核心贡献**：
1. **首个把 TTS 形式化为「条件 codec 语言建模」**：用 audio codec code 取代 mel 频谱作中间表示，把任务从连续信号回归改为离散 token 的 next-token / masked-token 建模，从而能直接套用 GPT 式 prompting 与 in-context learning。
2. **3 秒提示零样本音色克隆**，无需微调、无需 speaker encoder、无需预设声学特征——把零样本 TTS 从「适配/编码」范式推向「大模型 prompting」范式。
3. **证明半监督数据 scaling 被严重低估**：用 60K 小时（前人数百倍）含噪 + 伪转写数据，反而得到强泛化与涌现的 in-context 能力。
4. **codec token 保留音色与录音环境**，使「情绪/声学环境零样本迁移」与「输出多样性」自然成立。

**影响**：奠定神经 codec LM TTS 路线，直接衍生 Microsoft 自家 **VALL-E X**（跨语言零样本 TTS）、**VALL-E R**（phoneme 单调对齐增强鲁棒性）、**VALL-E 2**（repetition-aware sampling + grouped code modeling，首次在 LibriSpeech/VCTK 达到零样本 TTS **human parity**）、**MELLE**（连续 mel token、去掉矢量量化）、**FELLE**（flow matching 连续 token）、**PALLE** 等系列；并广泛影响业界 codec-LM TTS（语义/声学 token + LM 的设计成为主流之一）。

**已知局限（作者自述）**：
- **鲁棒性**：因 AR 段是自回归、注意力对齐可能错乱，存在漏词/吐字不清/重复（vanilla Transformer-TTS 通病），未加显式约束；后续可用 NAR 或改注意力机制缓解（VALL-E R 即沿此方向）。
- **数据覆盖**：60K 小时仍覆盖不全所有人声尤其口音说话人，且风格偏朗读（VCTK 相似度逊于 LibriSpeech 即为佐证）。
- **结构**：用两个模型分别预测不同量化器，未来可考虑单一通用大模型或全 NAR 以加速。
- **滥用风险（broader impact）**：能保持说话人身份 → 可能被用于语音欺骗/冒充；作者提出可训练「合成语音检测模型」并遵循 Microsoft 负责任 AI 原则；这也是 Microsoft **未开源权重**的原因之一。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2301.02111
- arxiv_pdf: https://arxiv.org/pdf/2301.02111
- github (官方，仅 demo/preprint 链接，无代码权重): https://github.com/microsoft/unilm/tree/master/valle
- project_page (MSR，VALL-E Family 总览页): https://www.microsoft.com/en-us/research/project/vall-e-x/
- demo_page: https://aka.ms/valle

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2301.02111.pdf
- ../../../sources/omni/2023/arxiv-2301.02111.txt
- ../../../sources/omni/2023/vall-e--unilm-readme.md
- ../../../sources/omni/2023/vall-e--msr-project-page.md
