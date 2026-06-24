---
title: Linformer — Self-Attention with Linear Complexity
org: Meta / Facebook AI
country: US
date: 2020-06
type: paper
categories: [架构]
url: https://arxiv.org/abs/2006.04768
pdf_url: https://arxiv.org/pdf/2006.04768
github_url:
downloaded: [arxiv-2006.04768.pdf]
---

## 一句话定位
Linformer 证明自注意力矩阵是低秩的，可用线性投影把 key/value 序列长度压缩到一个常数维度，从而把注意力复杂度从 O(n²) 降到 O(n)。

## 摘要（3-6 句）
Linformer 从理论与实证两方面证明 softmax 自注意力矩阵近似低秩，因此可用两个线性投影把长度为 n 的 key 与 value 序列投影到固定的小维度 k，使注意力的时间与空间复杂度都降为 O(n)。在标准 NLP 基准上，Linformer 在大幅提速省内存的同时保持与标准 Transformer 相当的性能。

## 关键技术细节
- 核心观察：注意力矩阵低秩，谱集中在前若干奇异值。
- 方法：对 key、value 各加一个 n×k 线性投影矩阵，把序列长度 n 压到常数 k；复杂度 O(nk) ≈ O(n)。
- 可在多头/多层间共享投影矩阵以进一步省参数。
- 性能：在 RoBERTa 风格预训练 + GLUE/IMDB 等下游任务上与标准注意力相当，序列越长加速越明显。
- 与稀疏注意力（局部/全局）思路不同，走的是低秩压缩路线。

## 原始链接
- url: https://arxiv.org/abs/2006.04768
- pdf_url: https://arxiv.org/pdf/2006.04768

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2006.04768.pdf
