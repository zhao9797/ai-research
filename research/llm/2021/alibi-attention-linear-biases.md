---
title: "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation (ALiBi)"
org: University of Washington / Facebook AI Research / Allen Institute for AI
country: US
date: 2021-08
type: paper
categories: [架构]
url: https://arxiv.org/abs/2108.12409
pdf_url: https://arxiv.org/pdf/2108.12409
github_url:
downloaded: [arxiv-2108.12409.pdf]
---

## 一句话定位
ALiBi（Attention with Linear Biases）：不加位置嵌入，而是按 query-key 距离给注意力分数加线性惩罚，让模型"训练短、测试长"——开创长度外推（length extrapolation）研究方向。

## 摘要（3-6 句）
论文先指出 Transformer 在推理时对超过训练长度的序列外推能力差。ALiBi 不向词嵌入加位置编码，而是按 query 与 key 的距离对注意力分数加一个成比例的线性偏置（penalty），即可实现高效长度外推。在 1.3B 模型上，训练长度 1024、测试长度 2048 时，ALiBi 的困惑度优于在 2048 上训练的 sinusoidal 模型，同时训练更快、用更少内存。

## 关键技术细节
- 核心：注意力 logit 加 -m·|i-j| 的线性距离惩罚（每个 head 有不同斜率 m），不使用任何位置嵌入。
- 长度外推：train 短（如 1024）→ test 长（如 2048+）困惑度仍优，无需重训。
- 效率：相对 sinusoidal/rotary 训练更快、更省内存。
- 验证规模：最大 1.3B 参数。
- 影响：被 BLOOM、MPT 等采用，与 RoPE 并列为 2021 年两大位置编码新方向。
- 发表于 ICLR 2022。

## 原始链接
- url: https://arxiv.org/abs/2108.12409
- pdf_url: https://arxiv.org/pdf/2108.12409

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2108.12409.pdf
