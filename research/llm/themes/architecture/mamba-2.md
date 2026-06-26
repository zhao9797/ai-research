---
title: "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality (Mamba-2)"
org: Princeton University / Carnegie Mellon University
country: US
date: 2024-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2405.21060
pdf_url: https://arxiv.org/pdf/2405.21060
github_url: https://github.com/state-spaces/mamba
downloaded: [mamba2.pdf]
---

## 一句话定位
Mamba-2 提出 State Space Duality (SSD) 理论，证明 SSM 与注意力是结构化半可分矩阵的两种分解，由此设计的 SSD 层比 Mamba 快 2-8 倍。

## 摘要（3-6 句）
论文揭示 SSM（如 Mamba）与注意力变体本质上紧密相关，可通过「结构化半可分矩阵」(structured semiseparable matrices) 的不同分解联系起来，称为 State Space Duality (SSD) 框架。基于该框架，作者把 Mamba 的选择性 SSM 改造为 SSD 层，核心计算可写成矩阵乘形式，从而充分利用张量核（tensor cores），比 Mamba 的 selective scan 快 2-8 倍，同时在语言建模上仍与 Transformer 竞争。SSD 也让更大的状态维度成为可能。

## 关键技术细节
- SSD（State Space Duality）：把 selective SSM 表示为半可分矩阵，可用 block 分解（对角块走二次注意力、块间走线性递归）高效计算。
- 速度：SSD 核心层比 Mamba-1 的 selective scan 快 2-8×，主要因为能用矩阵乘 / tensor cores。
- 允许更大 state size（如 N=64→256），提升记忆容量，质量随之提升。
- 揭示线性注意力、Mamba、softmax 注意力在同一矩阵框架下的统一视角，对后续混合架构设计有指导意义。
- 作者：Tri Dao、Albert Gu。

## 原始链接
- url: https://arxiv.org/abs/2405.21060
- pdf_url: https://arxiv.org/pdf/2405.21060
- github_url: https://github.com/state-spaces/mamba

## 一手源存档（sources/）
- mamba2.pdf  （PDF 不入 git，走 HF bucket）
