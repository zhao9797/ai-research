---
title: "MusicGen / AudioCraft: Simple and Controllable Music Generation"
org: Meta AI
country: US
date: "2023-06"
type: paper
category: audio
tags: [music-generation, text-to-music, audio-lm, encodec, rvq, codebook-interleaving, autoregressive, transformer, open-source]
url: "https://arxiv.org/abs/2306.05284"
arxiv: "https://arxiv.org/abs/2306.05284"
pdf_url: "https://arxiv.org/pdf/2306.05284"
github_url: "https://github.com/facebookresearch/audiocraft"
hf_url: "https://huggingface.co/facebook/musicgen-large"
modelscope_url: ""
project_url: "https://ai.meta.com/blog/audiocraft-musicgen-audiogen-encodec-generative-ai-audio/"
downloaded: [arxiv-2306.05284.pdf, musicgen-audiocraft--readme.md, musicgen-audiocraft--musicgen-doc.md, musicgen-audiocraft--hf-model-card.md, musicgen-audiocraft--meta-blog.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
MusicGen 是 Meta AI 提出的**单阶段自回归 Transformer 文本/旋律到音乐**模型：在 32 kHz EnCodec RVQ token（4 个码本、50 Hz）上，用**码本交错（delay）模式**把 4 个并行码本流压缩到每秒仅 50 个自回归步、一遍生成，省去 MusicLM 式语义 token 与级联多模型。3.3B 模型在 MusicCaps 上人评质量 OVL=84.8/100（最强基线 MusicLM 80.5），FAD=3.8、KL=1.22，代码（MIT）与权重（CC-BY-NC 4.0）随 **AudioCraft** 框架全部开源，是开源音频生成的代表作。

## 背景与定位
文本到音乐的核心难点：音乐需用全频谱（44.1/48 kHz，远高于语音 16 kHz），含和声/旋律的长程复杂结构，人耳对失谐极敏感。主流做法把音频压成离散 token 再用生成模型建模，但 RVQ 会产生**多条并行依赖的 token 流**，如何联合建模是关键问题。

此前工作各有代价：
- **MusicLM**（[[musiclm]]，Agostinelli 2023）用「语义 token + 声学 token」两层级联多个自回归 decoder，依赖自监督语义表征，且把所有码本展平（flatten），自回归步数 = `d·fr·K`，开销大。
- **VALL-E**（Wang 2023）分两阶段：先建模第一条流，再用后处理网络非自回归地补齐其余流。
- **Mousai / Noise2Music / Riffusion** 走 latent diffusion 或微调 Stable Diffusion 频谱图路线。

MusicGen 的定位是**「Simple and Controllable」**：用**单一单阶段 LM**（不要语义表征、不要级联、不要上采样链），通过一个统一的「码本交错模式」框架同时表达 flatten/parallel/delay 等所有方案，并以 delay 模式把步数压回原始帧率级别；同时引入**无监督 chromagram 旋律条件**做可控生成。相关音频/扩散工作见 [[encodec]] [[audioldm-2]] [[latent-diffusion-ldm]]。

## 模型架构
**整体 = EnCodec 音频 tokenizer + 自回归 Transformer decoder LM**（条件于 text 或 melody）。

**1) 音频 tokenizer（EnCodec）**
- 非因果 5 层卷积自编码器，stride=640 → 帧率 **50 Hz**；初始 hidden 64，每层翻倍。
- 隐空间用 **RVQ（Residual Vector Quantization）** 量化：**K=4 个码本**，每个码本大小 **M=2048**。
- RVQ 中每个量化器编码前一级的残差，故各码本**非独立**，第 1 个码本信息最粗、最重要。
- 32 kHz 单声道，采用对抗重构损失，按 1 秒随机裁剪训练（沿用 [[encodec]]）。

**2) 码本交错模式（核心创新，Figure 1）**
RVQ 每个时间步有 K 个码本，如何排成单一自回归序列是关键。论文形式化为「pattern」P=(P₀…P_S)，对码本-时间对集合 Ω 的一个划分，每步并行预测 P_s 内全部位置（条件于此前所有步）：
- **Flattening（展平）**：S=d·fr·K，精确分解，效果最好但步数 ×K（30 s → 6000 步），计算昂贵。
- **Parallel（并行）**：同一时间步 4 码本一起出，步数最少但「inexact」分解（假设码本条件独立，误差随 t 累积），质量最差。
- **Delay（延迟，最终选用）**：码本 k 相对错开 k−1 步，4 码本仍并行推进，30 s → **1500 步**，质量≈flatten 而成本仅 1/4。这是把语音 token 的 delay 思想（Kharitonov 2022）推广到音乐。
- 还有 Coarse-first、Partial-delay、Partial-flattening 变体（见消融）。
- **每秒音频仅 50 个自回归步**（delay 下），是 MusicGen「快」的根本原因。

**3) Transformer decoder**
- L 层、维度 D；每层 = 因果自注意力 + **cross-attention（注入条件 C）** + FFN（D→4D，ReLU，4D→D），残差 + pre-norm LayerNorm。
- 输入端：按当前 pattern step 取出对应码本值，各码本经独立 learned embedding 表（N 项、维度 D）求和；缺席码本用 special token；再加正弦位置嵌入。
- 输出端：每个码本一个独立线性头（D→N）出 logits。
- 用 **Flash Attention（xFormers）** 处理长序列以省显存/提速。

**4) 条件注入**
- **Text**：实验 T5 / FLAN-T5 / CLAP 三种编码器，**最终用 T5 encoder**（cross-attention 注入）；CLAP 训练用音频 embedding、推理用文本 embedding，并加 RVQ（12 量化器×码本 1024）量化以缩小训练/推理 gap。
- **Melody（无监督 chromagram）**：先用 **Demucs** 分离去掉 drums/bass，对残差取 chromagram（窗口 2¹⁴、hop 2¹²），每时间步取主导 bin 的 argmax 做**信息瓶颈**（防止直接复述原曲过拟合）；melody 条件作为 **prefix** 拼到 Transformer 输入前。无需 MusicLM 那种监督专有数据。

**5) 规模**：3 档 — **300M / 1.5B / 3.3B**（dim 1024/1536/2048，heads 16/24/32，depth 24/48/48）。两类变体：纯文本到音乐 与 文本+旋律引导。

## 数据
- **训练集 20K 小时持牌音乐**，约 **40 万条录音**（含文本描述与元数据：genre、BPM、tags）：
  - 内部 10K 高质量曲目 + **ShutterStock 25K** + **Pond5 365K**（后两者为纯乐器曲目）。
  - 全部为合法持牌数据（与 ShutterStock 有版权协议），32 kHz 全长曲目，默认下混为单声道。
- **文本预处理/增强**：condition-merging（把 key/tempo/乐器等元数据并入文本，概率 0.25；并 text-dropout 0.5）+ word-dropout 0.3；最终模型用 condition-merging + word-dropout（消融见下）。
- **评测集**：主结果用 **MusicCaps**（5.5K 专家标注 10 s 片段，1K genre-balanced 子集）；旋律评测与消融用内部 held-out 528 曲（与训练集无 artist 重叠）。
- **数据偏置（官方坦承）**：以西方风格音乐为主，文本/元数据仅英文；Dance/EDM 体裁占比最高（也是生成最好的体裁），尝试过采样少数体裁反而整体变差。
- **公开权重的数据处理**：HF 发布的 checkpoint 额外用 **HT-Demucs 音源分离**只保留乐器部分（故公开模型客观指标与论文略有差异）。

## 训练方法
- **目标**：标准 next-token，对 EnCodec 离散 token 做自回归交叉熵；非扩散、非 flow-matching。
- **优化**：AdamW，β=(0.9,0.95)，decoupled weight decay 0.1，grad clip 1.0，batch 192，**1M 步**；cosine LR + 4000 步 warmup；EMA decay 0.99。
- **混合精度**：用 **float16**（bfloat16 在其设置下导致不稳定）。
- **300M 用 D-Adaptation 自动步长**改善收敛；但 1.5B/3.3B 上 D-Adaptation 反而变差（train/valid 都退化），故大模型不用。
- **训练时长 30 s 随机裁剪**；分类器自由引导（CFG）：训练以 0.2 概率丢条件，推理 guidance scale=3.0。
- **采样**：top-k=250，temperature=1.0。
- **立体声（fine-tune）**：从单声道预训练模型出发，对左右声道各自跑 EnCodec → 8 码本/帧，再 fine-tune **200K batch**；用「stereo delay」或「stereo partial delay」两种码本错排，**无额外计算开销**即可生成立体声。
- 模型训练时间窗：2023 年 4–5 月（HF model card）。

## Infra（训练 / 推理工程）
- **训练算力**：300M / 1.5B / 3.3B 分别用 **32 / 64 / 96 块 GPU**（论文未给具体 GPU 型号与总 GPU·时），混合精度 float16。
- **长序列优化**：Flash Attention + xFormers 降低显存与提速。
- **推理形态**：开源库 **AudioCraft**（PyTorch，需 Python 3.9、PyTorch 2.1）；提供 small/medium/large/melody/melody-large 及全套 `musicgen-stereo-*` 共约 10 个预训练权重；medium（~1.5B）推理需 **≥16 GB 显存** GPU。
- **生成成本特性**：delay 模式下每秒音频仅 50 个自回归步；EnCodec 50 Hz 帧率比 DAC 86 Hz **推理快约 40%**（同样时长音频）。
- 提供 HF Space、Colab、Gradio、Jupyter 等多种交互；权重存于 HF（`AUDIOCRAFT_CACHE_DIR` 可改缓存）。
- 未披露：总 GPU·时、训练吞吐、并行分布式细节、量化/蒸馏推理加速。

## 评测 benchmark（把效果讲清楚）
**指标**：FAD（VGGish 特征，越低越好）、KL（AudioSet 分类器 / 公开模型用 PaSST 标签分布散度，越低越好）、CLAP score（音文对齐，越高越好）、人评 OVL（整体质量 1–100）、REL（文本相关性 1–100）。

**主结果（MusicCaps，论文 Table 1）**：

| 模型 | FAD↓ | KL↓ | CLAPscr↑ | OVL↑ | REL↑ |
|---|---|---|---|---|---|
| Riffusion | 14.8 | 2.06 | 0.19 | 79.31 | 74.20 |
| Mousai | 7.5 | 1.59 | 0.23 | 76.11 | 77.35 |
| MusicLM | 4.0 | — | — | 80.51 | 82.35 |
| Noise2Music | 2.1 | — | — | — | — |
| **MusicGen 300M** | 3.1 | 1.28 | 0.31 | 78.43 | 81.11 |
| **MusicGen 1.5B** | 3.4 | 1.23 | 0.32 | 80.74 | 83.70 |
| **MusicGen 3.3B** | 3.8 | 1.22 | 0.31 | **84.81** | 82.47 |
| MusicGen 1.5B w. random melody | 5.0 | 1.31 | 0.28 | 81.30 | 81.98 |

→ 人评上 MusicGen 在质量与文本贴合度均超所有基线（OVL 84.8 vs MusicLM 80.5）；Noise2Music FAD 最低（2.1），但作者指出 MusicCaps 含大量被标注为「noisy」的样本，质量越过某阈值后 FAD 反而失效（FAD 与主观评分不再相关）。加旋律条件略损客观指标但几乎不影响人评。

**码本模式消融（30 s，内部测试集，Table 4）**：

| 模式 | 步数 | FAD↓ | KL↓ | CLAPscr↑ |
|---|---|---|---|---|
| Delay（选用） | 1500 | 0.96 | 0.52 | 0.35 |
| Partial delay | 1500 | 1.51 | 0.54 | 0.32 |
| Parallel | 1500 | 2.58 | 0.62 | 0.27 |
| Partial flattening | 3000 | 1.32 | 0.54 | 0.34 |
| Coarse first | 3000 | 1.98 | 0.56 | 0.30 |
| Flattening | 6000 | 0.86 | 0.51 | 0.37 |

→ **Flattening 最好但步数 6000（×4 成本）；Delay 用 1/4 成本即逼近其质量**，Parallel 最差——这是「inexact 分解」误差累积的实证。

**模型规模消融（Table 5）**：300M→1.5B→3.3B 客观指标（PPL 56.1→48.4→46.1，FAD 0.96→0.86→0.82）单调改善；但**主观质量在 1.5B 饱和**，3.3B 主要赢在更好地贴合文本 prompt。

**旋律条件（Table 2，1.5B）**：用 Text+Chroma 训练并在测试也给 chroma 时，melody 相似度 SIM=0.66、人评 MEL=72.9（仅文本时 SIM=0.10）；且推理时丢掉 chroma 仍稳定（OVL/REL 基本不变）。

**立体声（Table 3，1.5B）**：Stereo Partial Delay OVL=86.73 > Mono Delay 84.95，立体声整体优于单声道，partial-delay 略优于 delay。

**Tokenizer 消融（附录 A.3）**：把 EnCodec 换 DAC（44.1 kHz、9 码本、86 Hz）——MusicCaps 上 FAD 改善但 KL 与主观更差，内部集更差；且 DAC 帧率高 40%，更慢。→ 选 EnCodec。

**文本编码器消融（附录 A.1）**：T5 与 FLAN-T5 客观接近（T5 OVL 略高），**CLAP 除 CLAP score 外全面更差**，故主模型用 T5。

**文本增强（附录 A.2）**：condition-merging 提升 FAD/KL；text-normalization 与 word-dropout 不改善客观指标（但 word-dropout 文本相关性最佳，故仍并用）。

**记忆性研究**：仅看第一码本流，2 万训练样本做 5 s greedy 续写，统计精确/80% 部分匹配比例，随 prompt 长度变化——用于评估过拟合/版权记忆风险。

## 创新点与影响
**核心贡献**
1. **单阶段单模型**做高质量 32 kHz 文本到音乐，**抛弃语义 token 与级联/上采样链**（相对 MusicLM 大幅简化）。
2. **码本交错模式统一框架** + **delay 模式**：一遍并行生成 4 码本、每秒仅 50 步，质量逼近 flatten 而成本约 1/4；并能零成本扩展到立体声。
3. **无监督 chromagram 旋律条件**：去 drums/bass + argmax 信息瓶颈，实现可控旋律生成，无需 MusicLM 式监督专有数据。
4. **AudioCraft 开源生态**：代码 MIT、权重 CC-BY-NC 4.0，连同 EnCodec / AudioGen / MAGNeT / MusicGen-Style / JASCO 等成为开源音频生成事实标准基座，给社区首次提供完整可复现训练栈。

**影响**：MusicGen 成为后续可控/快速音乐生成（如 MAGNeT 非自回归、MusicGen-Style 风格条件、JASCO 和弦/鼓轨条件、Stable Audio 等）的对照基线与方法源头；delay/码本交错思想被广泛沿用；EnCodec+AR-LM 的「neural codec language model」范式在音乐域被坐实。

**已知局限（官方）**
- 对条件的「贴合程度」缺乏细粒度控制，主要靠 CFG；音频条件的数据增强仍待研究。
- 仅英文文本/元数据，非英语表现差；数据集以西方音乐为主、体裁不均衡，存在文化偏置。
- 仅供研究用途，下游应用前需进一步风险评估与缓解（model card 明示）。
- 主观质量在 1.5B 后饱和，更大模型边际收益主要在文本理解。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2306.05284
- arxiv_pdf: https://arxiv.org/pdf/2306.05284
- github: https://github.com/facebookresearch/audiocraft
- github_musicgen_doc: https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md
- hf_model_card: https://huggingface.co/facebook/musicgen-large
- meta_blog: https://ai.meta.com/blog/audiocraft-musicgen-audiogen-encodec-generative-ai-audio/

## 一手源存档（sources/）
- [arxiv-2306.05284.pdf](https://arxiv.org/pdf/2306.05284)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/musicgen-audiocraft--readme.md)
- [musicgen-doc.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/musicgen-audiocraft--musicgen-doc.md)
- [hf-model-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/musicgen-audiocraft--hf-model-card.md)
- [meta-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/musicgen-audiocraft--meta-blog.md)
