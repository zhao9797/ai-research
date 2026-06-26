---
title: Memory-Efficient Pipeline-Parallel DNN Training (PipeDream-2BW)
org: Microsoft Research / Stanford / Carnegie Mellon
country: US
date: 2020-06
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2006.09503
pdf_url: https://arxiv.org/pdf/2006.09503
downloaded: [pipedream-2bw-2006.09503.pdf]
---

## 一句话定位
PipeDream 的内存高效版（2BW = double-buffered weights），用 1F1B 调度 + 仅两份权重版本，在保持高吞吐的同时大幅降低流水线并行显存，并自动划分 stage。

## 摘要（3-6 句）
异步流水线（PipeDream）吞吐高但需缓存多份权重版本，显存代价大。PipeDream-2BW 用 double-buffered weight updates，只维护两份权重版本即可保证梯度一致性，显存远低于 GPipe 重计算方案。它采用 1F1B（one-forward-one-backward）稳态调度填满流水线，并提供 planner 自动选择最优 stage 划分与并行配置。在 GPT/BERT 量级模型上相比 GPipe/Megatron 实现更高吞吐与更省显存。1F1B 调度成为后续 Megatron/DeepSpeed 流水线的默认。

## 关键技术细节
- 2BW：仅保留 2 个权重版本（double buffering），用 weight stashing 保证前后向版本一致，显存低。
- 1F1B 稳态调度：每设备交替执行一次前向一次反向，bubble 与 GPipe 同阶但显存更优。
- planner：自动搜索层划分 + 数据/流水并行配置（含 PipeDream-Flush 变体）。
- 影响：1F1B 成为 Megatron-LM / DeepSpeed 流水线并行的基础调度。

## 原始链接
- url: https://arxiv.org/abs/2006.09503
- pdf_url: https://arxiv.org/pdf/2006.09503

## 一手源存档（sources/）
- [pipedream-2bw-2006.09503.pdf](https://arxiv.org/pdf/2006.09503)  （arXiv 原文 PDF，不入 git）
