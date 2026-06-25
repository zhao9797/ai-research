---
title: "AudioLM: a Language Modeling Approach to Audio Generation"
org: Google Research
country: US
date: "2022-09"
type: paper
category: audio
tags: [audio, speech, music, neural-codec, semantic-tokens, autoregressive, soundstream, w2v-bert, textless-nlp]
url: "https://arxiv.org/abs/2209.03143"
arxiv: "https://arxiv.org/abs/2209.03143"
pdf_url: "https://arxiv.org/pdf/2209.03143"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://google-research.github.io/seanet/audiolm/examples/"
downloaded: [arxiv-2209.03143.pdf, audiolm--blog.md, audiolm--project.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
AudioLM 把音频生成重铸成「在离散 token 空间上做语言建模」的任务，提出 **语义 token（w2v-BERT + k-means）+ 声学 token（SoundStream RVQ）** 的混合分层分词，再用三段级联的 decoder-only Transformer 自回归生成，从而在**完全无文本/无符号标注**的前提下同时拿到长程结构一致性与高保真音质；其语音续写在主观盲测中 51.2% 辨识率（与随机 50% 无统计差异），并把 sBLIMP 零样本语法判断刷到 64.7%（相对前 SOTA CPC-BERT 提升约 8% 相对）。

## 背景与定位
音频信号（语音/音乐/环境声）具有多尺度结构：局部是音素/音符，全局是句法、语义、和声、节奏。过往高保真音频合成（WaveNet/WaveRNN、MelGAN/HiFi-GAN 等对抗式、DiffWave/WaveGrad 扩散式）在**没有强条件**（文本、MIDI）时只能生成"babbling"般无结构的音频；而 textless-NLP 路线（GSLM / Lakhotia et al. 2021）虽能无文本建模语音，但音质受限、只能单说话人干净场景，Jukebox 的音乐有明显伪影。

AudioLM 的核心洞察：把 NLP 语言模型对**长程结构**的建模能力迁移到音频，但需克服两大障碍——(1) 音频数据率远高于文本（一句话音频是几十万个采样值），序列太长；(2) 文本到音频是一对多（同一句话可由不同说话人、风格、录音条件渲染）。解法就是上面的混合 token 化：语义 token 重压缩抓长程结构、声学 token 补细节保真。它直接成为 [[musiclm]]（文本到音乐）与 neural-codec-LM TTS 路线（VALL-E）的方法学基础。技术脉络上承 SoundStream 神经编解码器、w2v-BERT 自监督表征与 GSLM 的 textless 思想。

## 模型架构
**整体：三段级联 decoder-only Transformer，全自回归 next-token 预测，分词器/反分词器预训练后冻结。**

三大组件抽象：
- **tokenizer** `enc(x)`：把单通道波形 x∈R^T 映射为离散 token 序列，T′≪T（token 数比采样点少 2–3 个数量级，是把上下文做长的关键）。
- **decoder-only Transformer LM**：在 token 上最大化 ∏ p(h_t | h_<t)，推理时自回归采样。
- **detokenizer** `dec(ĥ)`：把预测 token 解回波形。

**两种 token（图 1）：**
- **声学 token — SoundStream 神经编解码器**：卷积 encoder 把 16 kHz 波形降到 50 Hz 嵌入（每 20 ms 一帧，采样率降 320 倍），每帧经 **残差向量量化 RVQ**（Q 级量化器、每级 N 词表）离散化。实测配置 12 级 RVQ、每级 1024 词表、4 个卷积块 stride (2,4,5,8)，bitrate 6000 bps（每秒 600 token）。RVQ 的层级性使**粗层量化器**承载说话人身份/录音条件，**细层**只剩声学细节。
- **语义 token — w2v-BERT**：用 0.6B 参数的 Conformer-based w2v-BERT XL（MLM + 对比双自监督目标），取 **MLM 模块第 7 层** 的中间表征（1024 维、25 Hz / 每 40 ms 一帧），先把每维标准化为零均值单位方差（显著提升音素可分性），再训 **K=1024 的 k-means**，用质心索引当 token，bitrate 约 250 bps。提取方式类似从 HuBERT 取 token。

**三段建模（图 2）：**
1. **Semantic modeling**：自回归建 p(z_t | z_<t)，抓长程结构。
2. **Coarse acoustic modeling**：以全部语义 token 为条件，预测 SoundStream 粗 Q′ 层声学 token（实测 Q′=4）。用 row-major flatten 处理 RVQ 的层级结构。基于条件独立假设 p(z_t | z_<t, y_<t)≈p(z_t | z_<t)，语义先全序列建好再当条件，避免交错序列的超长长度。
3. **Fine acoustic modeling**：用粗 Q′ token 为条件补细 Q−Q′ 层（第 2000→6000 bps），去除二阶段残留压缩伪影。第三段假设细节由粗 token 局部决定，故在**不重叠的 3 秒音频块**上批处理、且可忽略语义 token，从而独立于目标音频长度扩展、能用更多 RVQ 层。

**LM 规格**：三段都用**结构相同**的 decoder-only Transformer——12 层、16 头、embedding 1024、FFN 4096、dropout 0.1、T5 相对位置编码，**每段 0.3B 参数**（合计约 0.9B）。注意：因为每个语义 token 对应 2Q′ 个二阶段声学 token、2(Q−Q′) 个三阶段 token（因子 2 来自 SoundStream 50 Hz 是 w2v-BERT 25 Hz 的两倍）。

## 数据
**语音**：AudioLM 全部组件（SoundStream、w2v-BERT、k-means 量化器、三段 Transformer）都在 **Libri-Light 的 unlab-60k 分片（6 万小时英语语音）** 上训练。值得注意：以往 textless 工作（GSLM 等）只用 Libri-Light 的 6k 小时 clean 子集训语言模型，而 AudioLM 在更多样、更嘈杂的 unlab-60k 上反而表现强——说明对训练数据质量更鲁棒，降低数据准备成本。定量评测用 LibriSpeech dev-clean（ABX/模型选择）与 test-clean（ASR/说话人分类/主观盲测），说话人分类器另在 train-clean-100 上训练；论文正文定量结果未用 test-other（官方 demo 页另放了 test-other 的续写听感样例）。

**音乐**：在**内部 4 万小时钢琴数据集**上重训全部组件，玩家水平从初学到专家、声学条件多样、内容从音阶练习到名曲。推理用 MAESTRO 数据集 test split 的 4 秒 prompt 起头。

数据清洗/过滤/re-captioning：本工作是**无文本、无标注**的纯音频建模，没有 captioning 流程；除上述外未披露额外的美学/安全过滤细节。

## 训练方法
- **训练目标**：纯 **next-token 自回归**（cross-entropy / 极大似然），三段各自独立训练，每段在「该段全部 ground-truth 历史 token」上做下一 token 预测。无扩散、无 flow matching。
- **分词器先冻结**：SoundStream 用重建+对抗损失端到端预训练；w2v-BERT 自监督预训练；二者训完即冻结，再训语言模型——解耦分词器与 LM，简化训练。
- **关键 trick**：(1) **去重**——前两段沿用 GSLM 做法，移除语义 token 的连续重复；(2) **随机裁剪**到等效输入长度 30s / 10s / 3s 分别对应三段；(3) 标准化 w2v-BERT 嵌入再聚类以提升音素可分性。
- **层/簇数选择**：通过 ABX、sWUGGY、sBLIMP（LibriSpeech dev-clean）扫描 + 少量主观试听，定下 w2v-BERT 第 7 层 + K=1024。
- **音乐特例**：钢琴版超参与语音版相同，但声学生成只用 **3 层量化、每层词表 2^14（16384）** 即达高重建质量，故**省去第三段**、直接在二阶段预测 3 层声学 token。
- 未使用 RLHF/DPO/偏好对齐，也未做步数蒸馏/一致性蒸馏（自回归 LM 范式，无扩散加速概念）。

## Infra（训练 / 推理工程）
- **训练算力**：每段（三段独立训练，相同配方）在 **16 块 TPUv4** 上、batch size 256、训 **1M steps**（原文只给单段配置，未披露三段合计算力/总卡时）。
- **推理**：三段都用 **temperature sampling**，温度分别 0.6 / 0.8 / 0.6（在多样性与语义一致性间折中）。语音续写用 3 秒 prompt：截断样本、抽 w2v-BERT 与 SoundStream token 当条件，再依次跑三段、最后送 SoundStream decoder 重建波形。
- **工程取舍**：把声学拆成粗/细两段是为限制单次处理的序列长度；第三段在 3 秒非重叠块上批处理，使其计算独立于目标音频总长。
- 未披露：GPU·时总量、并行/分布式细节、混合精度、吞吐 token/s、推理延迟与量化部署形态。官方明确**仅作研究用途、当时无更广泛发布计划**。

## 评测 benchmark（把效果讲清楚）
**1) Token 性质对比（表 I，LibriSpeech dev-clean；ABX 越低越好，ViSQOL 越高越好）**
| 分词 | bitrate | ABX 内/跨说话人(↓) | 重建 ViSQOL(↑) |
|---|---|---|---|
| 语义 (w2v-BERT) | 250 bps | 6.7 / 7.6 | 1.1 |
| 语义 (w2v-BERT) | 6000 bps | 5.6 / 6.2 | 1.4 |
| 声学 (SoundStream) | 2000 bps | 22.4 / 28.7 | 3.3 |
| 声学 (SoundStream) | 6000 bps | 17.8 / 26.6 | 3.9 |

结论：声学 token 重建质量高（ViSQOL 3.3–3.9）但音素可分性差；语义 token 反之——印证混合分词的必要性。

**2) 语义 token 是否承载语言内容（表 II，对 ground-truth 语义 token 做声学生成后 ASR）**
| | CER | WER |
|---|---|---|
| 原始音频 | 0.8 | 2.5 |
| SoundStream 重建 | 0.9 | 2.6 |
| **AudioLM 声学生成** | 3.4 | 6.0 |
| GSLM unit-to-speech | 2.9 | 6.6 |

低 CER/WER 说明语义 token 完整保留了语言内容；AudioLM 与 GSLM 相当（但 GSLM 只能合成单一干净嗓音）。

**3) 声学 token 承载说话人身份（表 III，说话人分类准确率 %）**
| SoundStream 重建 | 仅给语义 token 的声学生成 | 带 prompt 的续写 |
|---|---|---|
| 100.0 | 3.2 | 92.6 |

只给语义 token 时说话人准确率仅 3.2%（≈随机，语义 token 几乎不含说话人信息）；带声学 prompt 续写则 >92%（强保留说话人身份）。

**4) 零样本语言学探针（表 IV，sWUGGY/sBLIMP 成功率 %，无文本监督模型中加粗为最佳；"–" 为原表未报告）**
| 模型 | 类型 | sWUGGY all | sWUGGY in-vocab | sBLIMP |
|---|---|---|---|---|
| 文本上界 Forced alignment [13] | topline | 92.2 | – | 63.7 |
| 文本上界 Phone [13] | topline | 97.9 | – | 66.8 |
| BERT baseline [13] | non-causal | 67.7 | 75.6 | 56.1 |
| HuBERT-only [59] | non-causal | 70.9 | 79.8 | 59.5 |
| Harwath et al. [60] | non-causal | 67.6 | 75.4 | 56.7 |
| CPC-BERT [59] | non-causal | – | 80.0 | 59.9 |
| van Niekerk et al. [62] | causal | 64.3 | 72.3 | 54.0 |
| GSLM [14] | causal | – | 68.7 | 57.1 |
| **AudioLM** | causal | **71.5** | **83.7** | **64.7** |

注：原表只把 sWUGGY 拆成 all / in-vocab 两列、并区分 non-causal（非因果，不适合生成）与 causal（因果，可做生成）基线；AudioLM 是因果模型。AudioLM 在无文本监督模型中 sWUGGY（两列）与 sBLIMP 全面最佳，sBLIMP 相对前 SOTA（CPC-BERT 59.9）提升约 8% 相对，**甚至超过 forced-alignment 文本上界（63.7）**；若不做长度归一化 sBLIMP 达 67.5，超过 phone 上界（66.8）。

**5) 主观盲测（语音续写真假辨别）**：100 个样本、10 名英语熟练 rater、共 1000 次评分，给 3 秒原始 prompt + 7 秒续写（共 10 秒），原始样本也用 SoundStream 压缩以消除伪影线索。正确辨别率 **51.2%**，二项检验 p=0.23，与随机 50% **无统计显著差异**——续写几乎不可辨。

**6) 合成检测**：用同架构卷积网做二分类，平衡测试集准确率 **98.6%**——人耳难辨但机器易测（用于风险缓解）。

**7) 钢琴音乐**：完整 AudioLM vs 仅声学 token 模型，15 对 20 秒续写、10 名 rater，**83.3% 偏好完整 AudioLM**——证明语义 token 对旋律/时间结构一致性的关键作用。

**消融关键结论**：去掉语义 token（仅声学 LM）会保留说话人/录音条件但语言内容沦为 babbling（语音）/失去旋律连贯（音乐）——语义 token 是长程一致性的来源。

## 创新点与影响
**核心贡献**：
1. 首次系统性提出 **「语义 token + 声学 token」混合分层分词 + 多段自回归 LM** 的音频生成范式，把长程结构与高保真音质这对矛盾解耦。
2. 实证 w2v-BERT 语义 token 与 SoundStream 声学 token 在音素可分性/重建质量上互补，并给出层选择/聚类数等可复现配方。
3. 无文本即可生成句法语义连贯、保说话人/韵律/录音条件的语音续写，并延伸到无符号表示的钢琴音乐续写。
4. 负责任 AI：随框架提供 98.6% 准确率的合成语音检测器。

**对后续的影响**：直接奠定 **[[musiclm]]**（文本到音乐）与 **neural-codec-LM TTS**（VALL-E 用 EnCodec/SoundStream 声学 token + LM 做零样本 TTS）的方法学；"semantic→acoustic 级联 + RVQ flatten" 成为 SoundStorm、AudioGen、UniAudio 等一批工作的通用骨架；把 textless-NLP 推进到高保真。

**已知局限**：(1) 仅英语语音与钢琴单一乐器，未做多语种/复调；(2) 纯自回归三段级联，推理需逐 token 串行、未做加速；(3) 续写而非文本条件生成，需后续套 encoder-decoder 才能做 TTS/语音翻译；(4) 对欠表示群体的口音/方言一致性可能不足，并存在说话人冒充等滥用风险（作者明确不广泛发布）。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2209.03143
- paper PDF (TASLP v2, 2023-07): https://arxiv.org/pdf/2209.03143
- official blog (Google Research): https://research.google/blog/audiolm-a-language-modeling-approach-to-audio-generation/ （原 ai.googleblog.com/2022/10/audiolm-language-modeling-approach-to.html 重定向）
- project / audio examples: https://google-research.github.io/seanet/audiolm/examples/

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2209.03143.pdf
- ../../../sources/omni/2022/audiolm--blog.md
- ../../../sources/omni/2022/audiolm--project.md
