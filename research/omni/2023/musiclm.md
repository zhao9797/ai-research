---
title: "MusicLM: Generating Music From Text"
org: Google Research
country: US
date: "2023-01"
type: paper
category: audio
tags: [text-to-music, audio-generation, discrete-tokens, autoregressive, audiolm, soundstream, mulan, hierarchical]
url: "https://arxiv.org/abs/2301.11325"
arxiv: "https://arxiv.org/abs/2301.11325"
pdf_url: "https://arxiv.org/pdf/2301.11325"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://google-research.github.io/seanet/musiclm/examples/"
downloaded: [musiclm--paper-fulltext.md, musiclm--project-page.md, arxiv-2301.11325.pdf]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
MusicLM 把文生音乐建模成**层级离散 token 的多阶段自回归序列到序列任务**（在 [[audiolm]] 的语义+声学 token 框架上嵌入文本条件），用 [[mulan]] 联合音乐-文本嵌入**消解配对数据稀缺**（训练只需纯音频，文本条件仅在推理时替换），能从复杂文本描述生成 24 kHz、连续数分钟保持一致的高保真音乐；在自家发布的 MusicCaps 上 FAD_VGG=4.0、MCC=0.51，人评 Wins=312 显著优于 Mubert(97)/Riffusion(158)，并支持哼唱/口哨**旋律条件**与长达 5 分钟、可换文本的 story mode 生成。

## 背景与定位
- **要解决的问题**：文生音乐相比文生图有两大障碍——(1) 音频要同时做到**高保真**与**长时一致性**（前作如 Jukebox 有可闻 artifact，PerceiverAR 高质量但长程一致性差）；(2) **配对音乐-文本数据极度稀缺**，且为音乐写描述远难于给图片配字幕（音乐沿时间维度展开，单条 caption 是很弱的标注）。早期文生音频（DiffSound、AudioGen）只能在 AudioSet/AudioCaps 不到 5k 小时配对数据上生成几秒钟、少数声学事件的简单声学场景，无法生成有长程结构和多声部的音乐片段。
- **技术脉络中的位置**：直接继承 [[audiolm]]（把音频生成建成离散表示上的语言建模，用"语义 token + 声学 token"两级 token 兼顾长程结构与高保真）。MusicLM 在 AudioLM 上加了三件事：(1) 用文本/旋律做条件；(2) 把生成对象从钢琴扩展到 drum'n'bass / 爵士 / 古典等各种长音乐；(3) 用 [[mulan]] 把"音频域训练、文本域推理"打通。
- **相对前作的关键改进**：思路上类比 [[dall-e-2]]——DALL·E 2 用 CLIP 做文本编码、用 diffusion 解码；MusicLM 用 MuLan 做"音乐-文本"联合嵌入，但解码器是 AudioLM 自回归而非 diffusion，且**省掉了 text→audio 的 prior**：因为 MuLan 把音频和文本投到同一空间，训练时喂音频侧 embedding、推理时直接换成文本侧 embedding 即可，于是解码器可在**纯音频语料**上训练。基线对比：相对 Mubert（检索音乐设计师预录音色拼接）和 Riffusion（在 mel 频谱上微调 Stable Diffusion）在质量和文本贴合度上全面领先。

## 模型架构
整体是"**三个独立预训练并冻结的表示模型** + **两/三阶段 decoder-only Transformer 自回归生成**"。

**三类 token（表示层，均独立预训练后冻结）**：
- **声学 token A（SoundStream）**：24 kHz 单声道 SoundStream 神经音频编解码器，striding=480 → 50 Hz embedding；RVQ（残差矢量量化）**12 个量化器，每个码本大小 1024**，码率 6 kbps，即**1 秒音频 = 600 个声学 token**。RVQ 的层级性（粗层对高保真重建更关键）天然适配"粗到细"生成。
- **语义 token S（w2v-BERT）**：**600M 参数**的 w2v-BERT，取其 MLM 模块**第 7 层**中间表示，对该 embedding 做 **k-means（1024 个簇）** 离散化，采样率 25 Hz，即**1 秒 = 25 个语义 token**。语义 token 负责长程结构/旋律骨架。
- **条件 token M（MuLan）**：MuLan 是音乐-文本联合嵌入模型，两塔结构（**文本塔 = 预训练 BERT，音频塔 = ResNet-50**），对比学习投到 **128 维**共享空间。MuLan 只吃 10 秒音频，长音频按 **10 秒窗、1 秒 stride** 算 embedding 再平均；再用 **RVQ（12 量化器 × 1024 码本）** 离散化得 **12 个 MuLan token**——训练用音频侧 M_A，推理用文本侧 M_T（同一个 RVQ 量化）。把条件也做成离散 token 是为了"音频与条件同构"，便于后续研究自回归地建模条件本身。

**生成层（Transformer）**：每个阶段是一个独立的 **decoder-only Transformer**，结构共享：**24 层、16 注意力头、embedding 维度 1024、FFN 维度 4096、dropout 0.1、相对位置编码（T5 式）**，**每阶段约 430M 参数**。

**层级建模流程**（Figure 2）：
1. **语义建模阶段**：以 MuLan token 为条件预测语义 token，建模 p(S_t | S_<t, M_A)。
2. **声学建模阶段**：以 MuLan token + 语义 token 为条件预测声学 token，建模 p(A_t | A_<t, S, M_A)。沿用 AudioLM 把声学阶段再拆为**粗声学（建 SoundStream RVQ 前 4 层）** 和 **细声学（建剩余 8 层）**，以避免单一序列过长。
推理时只需把 M_A 换成从文本算出的 M_T，依次跑各阶段，最后用 **SoundStream 解码器**把声学 token 还原成波形。

**分辨率/时长策略**：自回归天然支持外推，训练 30 秒、推理时以 15 秒为 prefix、15 秒 stride 滚动生成，可连贯数分钟（demo 含 5 分钟片段）。

## 数据
- **生成模型主训练集**：**500 万段音频片段、共 280k 小时、24 kHz 音乐**（纯音频、**无文本标注**）。tokenizer 与语义/声学自回归模型均在此训练，多轮 pass。这是 MusicLM 相对前作能 scale 的核心——靠 MuLan 把音频侧 embedding 当条件，训练完全不需要 caption。
- **SoundStream 与 w2v-BERT** 训练于 **Free Music Archive（FMA）** 数据集。
- **训练裁剪**：语义阶段用 **30 秒**随机裁剪，（粗）声学阶段 **10 秒**，AudioLM 细声学阶段 **3 秒**。
- **MuLan**：在弱关联的音乐-片段/文本标注对上对比学习预训练（本文直接用 Huang et al. 2022 的冻结模型，未在本文重训）；论文称 MuLan 对训练数据质量要求很弱，能从弱关联对中学跨模态对应。
- **清洗/过滤/配比/re-captioning/合成数据**：除上述外，正文**未披露**数据来源细节、版权来源、清洗与配比策略（仅在 Broader Impact 提到训练数据偏置与文化挪用风险）。**旋律条件**用到了**合成数据**：用同一曲目的不同版本（翻唱、伴奏、人声）+ 采集的真人哼唱/演唱，构造"旋律相同、声学不同"的音频对来训旋律嵌入模型。
- **评测数据集 MusicCaps（本文发布）**：从 AudioSet 取 **5,521 段** 10 秒音乐片段（其中 **2,858 来自 AudioSet eval、2,663 来自 train**），由 **10 位专业音乐人**写英文描述：每段含 (1) 平均约 4 句的自由文本 caption；(2) 平均约 11 条的 music aspect 列表（流派、情绪、速度、人声、配器、不和谐度、节奏等）。另提供 **1k 流派均衡子集**（全部取自 AudioSet eval split），用于人评。公开于 Kaggle。

## 训练方法
- **训练目标**：纯**自回归 next-token 预测**（softmax 交叉熵）on 离散 token——没有 diffusion / flow matching；这是与同期 Riffusion（diffusion on 频谱）、AudioLDM 路线的根本区别。三个阶段（语义 / 粗声学 / 细声学）各自独立训练一个 decoder-only Transformer。
- **多阶段**：表示模型（SoundStream / w2v-BERT / MuLan）先各自独立预训练并**冻结**，再训练自回归生成阶段。无 SFT / 偏好对齐 / RLHF / DPO（2023 年初的工作，纯预训练式生成）。
- **蒸馏 / 加速**：**未使用**任何 consistency / LCM / ADD / 步数蒸馏（自回归非 diffusion，不存在"步数"概念）。
- **推理采样关键超参（temperature sampling）**：语义阶段 **T=1.0**，粗声学 **T=0.95**，细声学 **T=0.4**——按主观试听在多样性与时间一致性之间取折中。
- **旋律条件训练（Appendix C）**：旋律嵌入模型是个小 **ViT（12 层、6 头、维度 512、FFN 1024）**，输入是 mel 频谱的时间帧，用 **semi-hard triplet loss** 学习"对旋律敏感、对乐器/声学不变"的 **192 维 / 每 4 秒** 嵌入；训练时 10 秒输入、3 秒 hop 取 3 个嵌入，各用 **RVQ（24 量化器 × 512 码本）** 离散化，再与 MuLan token **拼接**作为条件。推理时从输入音频（哼唱/口哨）算旋律 token 与 M_T 拼接。
- **长生成 / story mode**：靠自回归外推，15 秒 prefix + 15 秒 stride 滚动，条件文本可每 15 秒切换（story mode），过渡 tempo 一致、语义平滑。

## Infra（训练 / 推理工程）
- 论文**几乎未披露**训练算力工程细节：未给 GPU/TPU 型号与数量、GPU·时、并行/分布式方案、混合精度、吞吐等任何数字。仅可知规模量级——5M 片段 / 280k 小时、每阶段 430M 参数、多轮 pass。
- **推理形态**：三阶段串行自回归采样（语义→粗声学→细声学）+ SoundStream 解码；600 token/秒的声学序列意味着推理是较重的自回归解码，论文未报推理延迟/吞吐/量化部署等。
- **未发布权重/代码**：论文明确表示出于版权/滥用风险**暂不发布模型**（"we have no plans to release models at this point"），只公开 MusicCaps 评测集。（后续 Google 以 MusicLM 为基础推出了 AudioTest/AI Test Kitchen 实验产品，但本文不含。）

## 评测 benchmark（把效果讲清楚）
**指标**：FAD（Fréchet Audio Distance，参考无关的音质代理，分别用 **Trill**(语音域) 与 **VGGish**(音频事件域) 两个 embedding 模型计算，↓更好）；KLD（用 LEAF/AudioSet 多标签分类器对生成与参考算类别分布 KL，衡量文本贴合度，↓更好）；MCC（MuLan Cycle Consistency，文本嵌入与生成音乐嵌入的平均余弦相似度，↑更好）；人评 Wins（A/B 5 点 Likert，统计被偏好次数，↑更好）。

**主结果（MusicCaps，Table 1）**：

| 模型 | FAD_Trill ↓ | FAD_VGG ↓ | KLD ↓ | MCC ↑ | Wins ↑ |
| --- | --- | --- | --- | --- | --- |
| Riffusion | 0.76 | 13.4 | 1.19 | 0.34 | 158 |
| Mubert | 0.45 | 9.6 | 1.58 | 0.32 | 97 |
| **MusicLM** | **0.44** | **4.0** | **1.01** | **0.51** | **312** |
| MusicCaps（真值） | - | - | - | - | 472 |

- **音质**：MusicLM FAD_VGG=4.0 大幅优于 Mubert(9.6)/Riffusion(13.4)；FAD_Trill=0.44 与 Mubert(0.45) 持平、优于 Riffusion(0.76)。论文指出能达到与"靠音乐人预录音色"的 Mubert 相当的音质。
- **文本贴合**：KLD=1.01、MCC=0.51 均为最佳。
- **人评**：共收集 **1200 条评分**（每个 source 参与 600 次两两比较），MusicLM Wins=312 明显优于两基线，但与真值(472)仍有差距；细分（Appendix B）显示 MusicLM 甚至在 **27%** 的对比中被认为比真值更贴合 caption，post-hoc Wilcoxon 符号秩检验（Bonferroni 校正 p<0.01/15）显示排序均显著。真值被偏好优于 MusicLM 的样本集中在：caption 极度详细（>5 件乐器、含非音乐元素如"风声/人说话"）、描述时间先后顺序、使用否定——这三类 MuLan 捕捉不好。

**关键消融**：
- **语义 token 的作用**：去掉语义阶段、直接由 MuLan token 预测粗声学 token，FAD 基本不变（0.42 / 4.0），但 **KLD 从 1.01 升到 1.05、MCC 从 0.51 降到 0.49**，且长程结构退化——说明语义 token 主要贡献"文本贴合 + 长程一致"。
- **token 信息分工**：固定文本 token + 语义 token、只重采声学阶段 → 样本同流派/节奏/主旋律，仅在混响/失真/相近音色乐器上有差异；只固定文本 token、重采语义+声学 → 旋律与节奏多样性大增但仍贴合文本。
- **记忆化分析**（对语义阶段，借鉴 Carlini et al. 2022）：即使用 10 秒 prompt 续 5 秒，**精确匹配始终 <0.2%**；用 Sinkhorn 最优传输做近似匹配（阈值 τ=0.85，假阳<0.01%），近似匹配比例随 prompt 变长而升，约 **1%** 样本可找到近似匹配，且这些多是 token 多样性极低的片段（125 个语义 token 平均熵 4.6 bits，而匹配分数<0.5 的近似匹配样本熵降到 ~1.0 bit）。

## 创新点与影响
- **核心贡献**：(1) 文生音乐的**层级离散 token 多阶段自回归**范式——把 [[audiolm]] 的语义/声学双级 token 框架嵌入文本条件，首个能从复杂自由文本生成 24 kHz、连续数分钟、多声部音乐的系统；(2) 用 [[mulan]] 联合嵌入**绕开配对数据稀缺**（训练纯音频、推理换文本 embedding，省掉 text→audio prior），使训练可 scale 到 280k 小时；(3) 发布 **MusicCaps**（5.5k 专家标注音乐-文本对），成为文生音乐领域长期的标准评测集；(4) 把条件扩展到**旋律**（哼唱/口哨）并演示 5 分钟长生成与 story mode；(5) 系统化的音乐生成**记忆化/版权风险研究**方法（精确+近似匹配 via 最优传输）。
- **影响**：奠定了"离散 token + 自回归"这条文生音乐主线，直接启发了同年 Meta 的 [[musicgen-audiocraft]]（单阶段 Transformer + EnCodec token 的延续与简化）等工作；MusicCaps 成为后续 MusicGen、AudioLDM2、Stable Audio 等普遍引用的评测基准；与同期 diffusion 路线（Riffusion、AudioLDM）形成两大技术分支的对照。后续 Google 将其产品化进 AI Test Kitchen / MusicFX。
- **已知局限**：(1) 继承 MuLan 的缺陷——**误解否定、不遵守描述的精确时间顺序**；(2) MCC 评测本身基于 MuLan，对自家方法有利，量化评测仍需改进；(3) 未建模 intro/verse/chorus 等**高层曲式结构**，无歌词/人声内容；(4) 24 kHz 采样率、自回归推理较重；(5) 出于版权与滥用风险**不发布模型权重**，训练数据来源/版权细节未公开，存在训练数据偏置与文化挪用担忧。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2301.11325
- arxiv_pdf: https://arxiv.org/pdf/2301.11325
- project_page (demo): https://google-research.github.io/seanet/musiclm/examples/
- dataset (MusicCaps): https://www.kaggle.com/datasets/googleai/musiccaps

## 一手源存档（sources/）
- [paper-fulltext.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/musiclm--paper-fulltext.md)  （ar5iv 全文 HTML→markdown，含正文+附录 A/B/C，精读所用）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/musiclm--project-page.md)  （官方 demo 页快照）
- [arxiv-2301.11325.pdf](https://arxiv.org/pdf/2301.11325)  （arXiv 官方 PDF v1，6 页；已直连 curl 下载校验，PDF 按规则不入 git、备份 HF bucket）
