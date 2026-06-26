---
title: "Gated Linear Attention Transformers with Hardware-Efficient Training (GLA)"
org: MIT / MIT-IBM Watson AI Lab
country: US
date: 2023-12
type: paper
categories: [架构]
url: https://arxiv.org/abs/2312.06635
pdf_url: https://arxiv.org/pdf/2312.06635
github_url: https://github.com/fla-org/flash-linear-attention
downloaded: [gla.pdf]
---

## 一句话定位
GLA 给线性注意力加上数据相关的门控，并配套 FlashLinearAttention 硬件高效算法（chunkwise），让线性注意力既表达力强又跑得比 FlashAttention-2 快。

## 摘要（3-6 句）
线性注意力可并行训练、可写成 2D 矩阵隐状态的 RNN（线性推理），但通常弱于 softmax 注意力，且现有实现缺乏 I/O 感知、速度慢。本文先给出硬件高效的线性注意力算法（FlashLinearAttention，chunkwise 形式），在 1K 长度作为独立层就比 FlashAttention-2 快；再推广到带数据相关门控的更强变体 GLA。GLA 在中等规模语言建模上与强 Transformer 及 Mamba 竞争，并具更好的长度外推与回忆能力。

## 关键技术细节
- 门控线性注意力：在线性注意力的矩阵隐状态上加数据相关的（per-channel）衰减/门控，提升表达力与遗忘控制。
- FlashLinearAttention：chunkwise 算法，块内用矩阵乘（并行），块间用递归传状态，I/O 感知，比 FlashAttention-2 更快（即使短序列）。
- 衍生的 flash-linear-attention (fla) 库成为后续大量线性注意力/Mamba2/DeltaNet 工作的通用训练后端。
- 作者：Songlin Yang、Bailin Wang、Yoon Kim 等。

## 原始链接
- url: https://arxiv.org/abs/2312.06635
- pdf_url: https://arxiv.org/pdf/2312.06635
- github_url: https://github.com/fla-org/flash-linear-attention

## 一手源存档（sources/）
- gla.pdf  （PDF 不入 git，走 HF bucket）
