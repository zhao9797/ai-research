---
title: "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality (Mamba-2)"
org: Princeton / Carnegie Mellon
country: US
date: 2024-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2405.21060
pdf_url: https://arxiv.org/pdf/2405.21060
github_url: https://github.com/state-spaces/mamba
downloaded: [2405.21060.pdf]
---

## 一句话定位
Mamba-2 / SSD：建立 SSM 与注意力之间的理论对偶（structured state space duality），据此设计核心层比 Mamba 快 2-8 倍且仍与 Transformer 竞争。

## 摘要
Transformer 是语言建模成功的主架构，但 Mamba 等状态空间模型（SSM）近来在中小规模上已能匹敌或超越 Transformer。作者证明这两类模型其实密切相关，并通过对一类研究充分的结构化半可分矩阵（structured semiseparable matrices）的不同分解，建立 SSM 与注意力变体之间丰富的理论联系。这套 state space duality（SSD）框架使他们设计出新架构 Mamba-2，其核心层是对 Mamba 选择性 SSM 的改良，速度快 2-8 倍，同时在语言建模上仍与 Transformer 竞争。

## 关键技术细节
- SSD 理论：SSM 计算 ≡ 一种带结构掩码的注意力；半可分矩阵分解统一两者。
- Mamba-2 核心层：比 Mamba（Mamba-1）选择性 SSM 快 2-8×（用更大 state、矩阵乘形式利用 Tensor Core）。
- 并行/硬件友好：SSD 算法以 block 矩阵乘实现，远比线性扫描更适配 GPU。
- 可与 Transformer 混合（如配少量 attention 层）进一步提升。
- 与 attention 对偶让 multi-head / GQA 等技巧可迁移到 SSM。

## 原始链接
- url: https://arxiv.org/abs/2405.21060
- pdf_url: https://arxiv.org/pdf/2405.21060
- github: https://github.com/state-spaces/mamba

## 一手源存档（sources/）
- [2405.21060.pdf](https://arxiv.org/pdf/2405.21060)  （arXiv 原文 PDF，不入 git）
