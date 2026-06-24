---
title: "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation (ALiBi)"
org: University of Washington / Facebook AI / Allen Institute for AI
country: US
date: 2021-08
type: paper
categories: [架构]
url: https://arxiv.org/abs/2108.12409
pdf_url: https://arxiv.org/pdf/2108.12409
github_url: https://github.com/ofirpress/attention_with_linear_biases
downloaded: [alibi.pdf]
---

## 一句话定位
提出 ALiBi（Attention with Linear Biases）：不用任何位置嵌入，而是在注意力分数上按 query-key 距离加一个线性负偏置，从而让模型「短训练、长推理」，实现强长度外推。

## 摘要（3-6 句）
作者指出 sinusoidal、rotary、T5-bias 等位置方法在推理序列长于训练序列时外推能力有限。ALiBi 不向 word embedding 加位置信息，而是给每个 head 的注意力分数加一个与 query-key 相对距离成正比的负偏置（斜率 m 为每个 head 固定的几何序列）。这样在更长序列上推理时不需重训。实验中，在 1024 长度训练的 ALiBi 模型推理到 2048 长度，效果与在 2048 上训练的 sinusoidal 模型相当，且训练更快、内存更省。

## 关键技术细节
- 机制：softmax 前对 query i、key j 的分数加 −m·(i−j)，m 是 head-specific 斜率，取等比数列（如 1/2^(8/n_heads)）。
- 无可学习位置参数、无位置嵌入；纯静态偏置。
- 外推：训练长度 L 上训练，推理可显著超过 L 且困惑度不崩，解决了 sinusoidal/learned 位置嵌入的外推失败问题。
- 效率：相比 sinusoidal 基线，训练同等效果省约 11% 时间与 11% 内存。
- 后被 BLOOM、MPT 等模型采用；与 RoPE 并列为两大主流相对位置方案。
- 作者：Ofir Press、Noah A. Smith、Mike Lewis。

## 原始链接
- url: https://arxiv.org/abs/2108.12409
- pdf_url: https://arxiv.org/pdf/2108.12409
- github_url: https://github.com/ofirpress/attention_with_linear_biases

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/alibi.pdf
