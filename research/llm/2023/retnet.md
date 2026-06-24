---
title: Retentive Network: A Successor to Transformer for Large Language Models
org: Microsoft Research
country: US
date: 2023-07
type: paper
categories: [架构]
url: https://arxiv.org/abs/2307.08621
pdf_url: https://arxiv.org/pdf/2307.08621
github_url: https://aka.ms/retnet
downloaded: [retnet.pdf]
---

## 一句话定位
微软 RetNet 用 retention 机制统一并行/循环/分块三种计算范式，号称 Transformer 的“不可能三角”继任者。

## 摘要
RetNet 作为大模型基础架构，同时实现训练并行、低成本推理、好性能。理论上推导循环与注意力的联系，提出 retention 机制，支持三种计算范式：parallel(训练并行)、recurrent(O(1) 推理，提升解码吞吐/延迟/显存而不损性能)、chunkwise recurrent(线性复杂度高效长序列，块内并行、块间循环汇总)。语言建模实验显示良好扩展、并行训练、低成本部署与高效推理。

## 关键技术细节
- retention 机制：用带衰减的状态保持替代 softmax attention。
- 三范式等价：parallel(训练)、recurrent(推理 O(1))、chunkwise recurrent(长序列线性)。
- 推理优势：解码恒定显存与延迟，吞吐显著优于 Transformer。
- 长序列：chunkwise 线性复杂度。
- 实验：在 LM 上随规模增长，6.7B+ 时性能与效率均超 Transformer；号称破解“训练并行 / 低成本推理 / 好性能”不可能三角。

## 原始链接
- url: https://arxiv.org/abs/2307.08621
- pdf_url: https://arxiv.org/pdf/2307.08621
- github_url: https://aka.ms/retnet

## 本地落盘文件
- ../../../sources/llm/2023/retnet.pdf
