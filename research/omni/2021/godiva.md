---
title: "GODIVA: Generating Open-DomaIn Videos from nAtural Descriptions"
org: "Microsoft Research Asia / Duke University"
country: China
date: "2021-04"
type: paper
category: video
tags: [text-to-video, autoregressive, vq-vae, sparse-attention, t2v, howto100m, msr-vtt]
url: "https://arxiv.org/abs/2104.14806"
arxiv: "https://arxiv.org/abs/2104.14806"
pdf_url: "https://arxiv.org/pdf/2104.14806"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [godiva--arxiv-abs.md, godiva--ar5iv-fulltext.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
GODIVA 是**首个开放域文生视频（T2V）自回归预训练模型**：用帧级 VQ-VAE 把视频离散成视觉 token，再用**三维稀疏注意力（时间/行/列）Transformer** 以语言为条件自回归生成这些 token。在 HowTo100M（1.36 亿文-视频对）上预训练、MSR-VTT 上微调后，自动指标 RM（新提出的 Relative Matching）达 93.48，配合 CLIP ranking 重排达 98.34（GT=100），并展现出对未见文本的零样本生成能力。

## 背景与定位
2021 年初，文生图侧 [[dall-e-1]]（DALL-E，VQ-VAE + 自回归 Transformer）刚证明"离散视觉 token + 自回归语言建模"能把开放域文本变成高质量图像；而文生视频（T2V）当时几乎全是 GAN 路线（T2V/Li 2018、TFGAN/Balaji 2019、IRC-GAN 2019），且只在小规模、单场景数据上实验，泛化能力很弱。视频比图像难在于：除了海量像素，还要保证帧间时空一致性。

GODIVA 的定位非常明确——**把 DALL-E 式"VQ-VAE 离散化 + 自回归生成"范式第一次搬到 T2V**。作者明确声明"As far as we know, this is the first paper that uses VQ-VAE for [text-to-video] task"，与并发的 VQ-VAE 视频预测工作（Latent Video Transformer、Predicting Video with VQVAE）区别在于：那些做的是 video-to-video 预测（给前几帧续后几帧），GODIVA 做的是纯文本到视频生成。它是后续 [[nuwa]]（NÜWA，同组 MSRA 工作，把 GODIVA 的 3D 稀疏注意力升级为 3D Nearby Attention 统一图像/视频）与 [[cogvideo]] 等自回归文生视频路线的直接先驱。关键脉络位置：DALL-E（T2I 离散自回归）→ **GODIVA（T2V 离散自回归首作）** → NÜWA → CogVideo → 后续扩散派（[[video-ldm]] / [[make-a-video]] 等）。

## 模型架构
两段式：**(1) 帧级 VQ-VAE 视觉 tokenizer + (2) 三维稀疏注意力自回归生成器**。

**1. 帧级 VQ-VAE（frame-wise video auto-encoder）**
- 逐帧（不做时间维压缩）把视频 $x\in\mathbb{R}^{L\times H\times W\times C}$ 的每帧 $x^{(l)}$ 编码、量化、解码重建。
- 编码器 $E$、解码器 $D$ 各仅用 **2 层 CNN**，kernel size = 4、stride = 2，因此每帧 $64\times64$ 像素被压成 $h\times w = 16\times16$ 的离散网格（每帧 256 个 token）。
- codebook $B\in\mathbb{R}^{K\times D}$：**K=10000** 个码字，latent 维度 $d_B=128$。量化即对每个区域取最近邻码字索引（Eq. 2），再经码本嵌入回 $b^{(l)}$ 送解码器（Eq. 3-4）。
- VQ-VAE 损失 = 重建损失 + codebook 损失 + commitment 损失（带 stop-gradient，权重 $\beta$），标准 VQ-VAE 目标（Eq. 5）。
- VQ-VAE 在 **ImageNet** 上预训练（lr=1e-3，batch=32）；在 Moving MNIST 实验时另训一个专用 VQ-VAE，作者发现这样生成更好。

**2. GODIVA 生成器（三维稀疏注意力 Transformer）**
- 文本端：词嵌入 + 位置嵌入，最大文本长度 **N=35**，词表大小 S（Eq. 6）。
- 视觉端：用冻结的 VQ-VAE encoder 把 ground-truth 视频编成 token 序列 $b\in\mathbb{R}^{M\times d_B}$，$M=L\times h\times w$；经 Linear 映射到与文本同维 + 视觉位置嵌入（Eq. 8）。生成 $64\times64\times10$ 帧时，**M=2560** 个视觉 token。
- 解码器以文本嵌入为条件、对视觉 token 做 **自回归**（Eq. 9）。核心创新是把标准全局自注意力替换为**三维稀疏注意力**：每个 token $(i,j,l)$（行 i、列 j、帧 l）只在三个轴上分别 attend——
  - 时间 $SA^{(T)}$：同一空间位置、之前各帧 $v^e_{i,j,<l}$；
  - 行 $SA^{(R)}$：同帧同列、之前各行 $v^e_{<i,j,l}$；
  - 列 $SA^{(C)}$：同帧同行、之前各列 $v^e_{i,<j,l}$（Eq. 10）。
- 三种注意力**交替堆叠** $[SA^{(T)},SA^{(R)},SA^{(C)},SA^{(T)},...]$（Eq. 11），把复杂度从全局的 $O((Lhw)^2)$ 降到 $O(Lhw(L+h+w))$——这正是让 2560-token 长序列在视频上可训的关键。
- 输出经 Linear 映射到 VQ-VAE 词表维度 K 求 softmax（Eq. 12），交叉熵训练（Eq. 13）。
- 生成器超参：维度 **D=1024**，**16 个注意力头**，**R=12 层**。

## 数据
- **预训练**：HowTo100M（Miech et al. 2019），论文称含 **超过 1.36 亿（136M）文-视频对**（来自 YouTube 教学类旁白视频，弱监督 ASR 字幕配对）。
- **下游微调/评测**：MSR-VTT（10000 个视频片段，每条 20 个人工 caption）。
- **从零训练对照集**：Moving MNIST 与 Double Moving MNIST（由 MNIST 自动合成）。原版 Moving MNIST 仅"上下/左右"两种运动，本文按 IRC-GAN 设定**额外加了 4 种方向**（左再右、右再左、上再下、下再上），用于测试组合泛化/零样本（如训练里没有"Digit 9 down then up"但能生成）。
- VQ-VAE tokenizer 的"数据"是 ImageNet 图像（逐帧重建，不依赖视频时序）。
- 数据清洗/配比/re-caption/美学与安全过滤等细节**未披露**（2021 年早期工作，沿用 HowTo100M 原始弱监督配对）。

## 训练方法
- **训练目标**：两阶段离散化 + 自回归。VQ-VAE 阶段用 L2 重建 + 码本/commitment 损失（Eq. 5）；生成器阶段是标准 **next-token 交叉熵**（Eq. 13，给定文本预测下一个视觉 token），无扩散、无 flow matching、无 GAN 判别器。
- **多阶段**：① 在 ImageNet 上预训练帧级 VQ-VAE；② 在 HowTo100M 上预训练 GODIVA 生成器；③ 在 MSR-VTT 上微调。无 RLHF/DPO/reward model/偏好对齐（2021 年尚无此范式）。
- **推理重排 trick（提升显著）**：沿用 DALL-E 做法，推理时按 top-10 概率**随机采样 32 次**得到 32 个候选视频，再用 **CLIP ranking** 选语义最匹配的一个。该重排把 RM 从 93.48 拉到 **98.34**，是论文里最大的单点增益。
- **关键超参**：生成器预训练/微调统一 batch=32、lr=5e-4；VQ-VAE lr=1e-3、batch=32。
- 无蒸馏/一致性模型/步数压缩（自回归逐 token 生成，2560 步，无加速蒸馏）。

## Infra（训练 / 推理工程）
- **算力**：GODIVA 生成器在 HowTo100M 上用 **64 张 V100** 预训练；在 MSR-VTT 上用 **8 张 V100** 微调。具体 GPU·小时数、吞吐、并行/分布式策略、混合精度等**未披露**。
- **推理**：自回归逐 token 解码，单视频 2560 个 token 顺序生成；论文未报告推理延迟/吞吐。CLIP-ranking 重排需为每条 prompt 生成 32 个候选（额外 32× 解码 + CLIP 打分开销）。
- 量化、KV cache、部署形态等工程细节**未披露**。代码与更多细节论文承诺"will come soon in Github"（未在论文中给出链接）。

## 评测 benchmark（把效果讲清楚）
评测在 **MSR-VTT**（HowTo100M 预训练 + MSR-VTT 微调）。指标含自动（**SIM** = 文本与各帧 CLIP 相似度求平均；**RM** = SIM(生成) / SIM(GT) 的相对匹配分，作者新提出，意在消去 CLIP 域偏差）和人评（**VR** 视觉真实度、**SC** 语义一致性，200 名评测员两两胜出率）。下列数值均 ×100（Table 1）：

| 模型设置 | SIM | RM | VR(人评) | SC(人评) |
| --- | --- | --- | --- | --- |
| GT（真值视频上限） | 24.23 | 100 | - | - |
| GODIVA (6 层) | 21.45 | 86.94 | 9.38 | 9.38 |
| GODIVA w/o Row Attention | 21.23 | 85.95 | 31.25 | 40.63 |
| GODIVA w/o Temporal Attention | 21.52 | 87.44 | 40.63 | 43.75 |
| GODIVA w/o Column Attention | 22.08 | 89.20 | 46.88 | 46.88 |
| **GODIVA（默认 12 层）** | **22.82** | **93.48** | **81.25** | **78.13** |
| **GODIVA w/ CLIP ranking** | **24.02** | **98.34** | **88.12** | **81.25** |

**关键消融结论**：
- **规模/层数**：12 层显著优于 6 层（RM 93.48 vs 86.94，VR 81.25 vs 9.38），作者强调"sufficient scale is crucial"。
- **三轴注意力的必要性**：去掉任一轴都掉点，其中**去掉 Row Attention 掉得最多**（RM 85.95，作者明确"Row Attention is the most important"）；去掉 Temporal / Column 次之。
- **CLIP-ranking 重排**最有效，把自动 RM 推到 98.34、SIM 逼近 GT 的 24.02（GT=24.23）。
- **定性结果**：① 零样本——同 prompt "Play golf on grass" 下，GODIVA 不仅生成相关内容，还能**自发切换场景/镜头**（草坪→运动员近景→挥杆动作），而 GAN 基线（T2V/TFGAN）帧间几乎不变、单一场景；② 组合泛化——在 Moving MNIST 上能生成训练集没出现过的运动组合（如"Digit 9 down then up"），说明学到了文-视频语义对齐而非检索式记忆，质量与 SOTA 的 IRC-GAN 相当甚至更清晰。
- 未报告 FID / FVD / VBench 等后来标准的视频生成指标（2021 年 T2V 评测尚无统一标准，这也是本文提出 RM 的动机）。

## 创新点与影响
**核心贡献**：
1. **首个开放域 T2V 自回归预训练模型**：把 DALL-E 的"VQ-VAE 离散化 + 自回归"范式第一次成功迁移到文生视频，并在亿级文-视频对（HowTo100M）上预训练，证明 T2V 可以走"大规模预训练 + 下游微调/零样本"路线。
2. **三维稀疏注意力（T/R/C）**：把全局注意力 $O((Lhw)^2)$ 降为 $O(Lhw(L+h+w))$，是让长视觉 token 序列在视频上可训的工程关键；这一"沿轴稀疏"思想被同组 NÜWA 升级为 3D Nearby Attention，并影响后续自回归视频生成的注意力设计。
3. **Relative Matching (RM) 指标**：用 CLIP 相似度相对真值归一化，缓解了 T2V 缺乏客观自动评测的痛点，是早期无参考 T2V 评测的有益尝试。

**影响**：作为 T2V 自回归路线的开山之作，直接铺垫了 NÜWA → CogVideo 一脉；"离散 token + 自回归 + 大规模预训练"的思路在后续（含扩散派之前）成为文生视频的主流之一。

**已知局限（作者自述）**：① 长视频 + 高分辨率仍是大挑战——仅 $64\times64\times10$ 帧就要 2560 token，序列随分辨率/时长平方级膨胀；② T2V 自动评测仍不成熟，作者建议未来用基于视频（而非逐帧）的 CLIP 指标；③ 作者承认 GAN 方法在 T2V 上仍有潜力，开放域泛化是开放问题。其它隐含局限：分辨率低（64/128）、帧数短（10）、逐帧 VQ-VAE 不压缩时间维导致 token 冗余、自回归 2560 步推理慢。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2104.14806
- arxiv_pdf: https://arxiv.org/pdf/2104.14806
- ar5iv 全文(HTML): https://ar5iv.org/abs/2104.14806

## 本地落盘文件
- ../../../sources/omni/2021/godiva--arxiv-abs.md
- ../../../sources/omni/2021/godiva--ar5iv-fulltext.md
