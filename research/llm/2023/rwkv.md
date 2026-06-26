---
title: "RWKV: Reinventing RNNs for the Transformer Era"
org: EleutherAI / RWKV Foundation
country: US
date: 2023-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2305.13048
pdf_url: https://arxiv.org/pdf/2305.13048
github_url: https://github.com/BlinkDL/RWKV-LM
downloaded: [rwkv.pdf]
---

## 一句话定位
RWKV 把 RNN 改造成可并行训练、O(1) 推理的线性注意力架构，14B 是当时最大稠密 RNN。

## 摘要
Transformer 复杂度随序列二次增长；RNN 线性但难并行、难规模化。RWKV(Receptance Weighted Key Value) 结合 Transformer 的高效并行训练与 RNN 的高效推理：用线性注意力机制，可写成 Transformer(训练并行)或 RNN(推理恒定显存/算力)两种形态。规模化到 14B 参数(当时最大稠密 RNN)，性能与同尺寸 Transformer 相当。

## 关键技术细节
- 机制：Receptance、Weight、Key、Value(RWKV)；用 time-mixing + channel-mixing 替代注意力；线性注意力。
- 双形态：训练用并行(类 Transformer)，推理用串行 RNN，O(1)/token、恒定显存。
- 规模：最大 14B，当时最大稠密 RNN；另有 169M–7B 多档。
- 数据：The Pile 等公开数据。
- 结论：与同尺寸 Transformer 相当，调和效率与性能的权衡。

## 原始链接
- url: https://arxiv.org/abs/2305.13048
- pdf_url: https://arxiv.org/pdf/2305.13048
- github_url: https://github.com/BlinkDL/RWKV-LM

## 一手源存档（sources/）
- rwkv.pdf  （PDF 不入 git，走 HF bucket）
