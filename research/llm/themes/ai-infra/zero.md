---
title: "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models"
org: Microsoft (DeepSpeed)
country: US
date: 2019-10
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/1910.02054
pdf_url: https://arxiv.org/pdf/1910.02054
github_url: https://github.com/deepspeedai/DeepSpeed
downloaded: [zero-1910.02054.pdf]
---

## 一句话定位
DeepSpeed 的核心算法 ZeRO（Zero Redundancy Optimizer），通过在数据并行各 rank 间分片优化器状态/梯度/参数，消除显存冗余，使数据并行也能训练超大模型。

## 摘要（3-6 句）
传统数据并行在每张卡上复制完整模型状态，显存浪费严重。ZeRO 将模型状态（优化器状态、梯度、参数）切分到所有数据并行设备上，每卡只持有一份分片，按需通信。三个阶段分别为 ZeRO-1（切优化器状态）、ZeRO-2（再切梯度）、ZeRO-3（再切参数），显存可线性随设备数下降。论文称 ZeRO 可在 400 张 GPU 上训练 100B+ 模型，吞吐超线性扩展，并展望训练万亿参数。后续 DeepSpeed 用其训练了 17B 的 Turing-NLG。

## 关键技术细节
- 三类模型状态分片：Pos（优化器状态，4x 显存收益）、Pos+g（加梯度，8x）、Pos+g+p（加参数，与 Nd 成正比，Nd=DP 度）。
- 在 Adam + 混合精度下，单参数模型状态约 16 bytes（fp32 参数+动量+方差 + fp16 参数/梯度），ZeRO 把这部分按 DP 度均分。
- ZeRO-DP 与 ZeRO-R（激活分片、固定大小缓冲、显存碎片整理）配合。
- 实验：64 DGX-2（1024 V100）训练 100B 模型，38 TFLOPs/GPU，吞吐随卡数超线性扩展。

## 原始链接
- url: https://arxiv.org/abs/1910.02054
- pdf_url: https://arxiv.org/pdf/1910.02054
- github_url: https://github.com/deepspeedai/DeepSpeed

## 一手源存档（sources/）
- [zero-1910.02054.pdf](https://arxiv.org/pdf/1910.02054)  （arXiv 原文 PDF，不入 git）
