---
title: "FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision"
org: Colfax / Together AI / Meta / NVIDIA / Princeton (Tri Dao 等)
country: US
date: 2024-07
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2407.08608
pdf_url: https://arxiv.org/pdf/2407.08608
github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [2407.08608.pdf]
---

## 一句话定位
FlashAttention-3：针对 Hopper(H100) 重写注意力内核，利用异步 Tensor Core/TMA 与 FP8，FP16 达 75% 利用率、FP8 接近 1.2 PFLOPs/s。

## 摘要
注意力是 Transformer 与长上下文应用的瓶颈。FlashAttention 通过最小化显存读写加速注意力，但尚未利用新硬件能力——FlashAttention-2 在 H100 上仅 35% 利用率。本文用三项技术加速 Hopper 上的注意力：(1) 用 warp-specialization 重叠整体计算与数据搬运（利用 Tensor Core 与 TMA 的异步性）；(2) 交错 block-wise matmul 与 softmax；(3) block 量化 + incoherent processing 以利用 FP8 低精度硬件支持。FlashAttention-3 在 H100 上比 FA2 快 1.5-2.0×，FP16 达 740 TFLOPs/s（75% 利用率），FP8 接近 1.2 PFLOPs/s，且 FP8 数值误差比基线 FP8 注意力低 2.6×。

## 关键技术细节
- 目标硬件：NVIDIA Hopper（H100），利用 WGMMA 异步 Tensor Core 与 TMA。
- 技术1：warp-specialization 生产者/消费者，重叠 GEMM 与数据搬运。
- 技术2：ping-pong 调度，交错 matmul 与 softmax（隐藏 softmax 的非 matmul 开销）。
- 技术3：FP8 block 量化 + incoherent processing（用 Hadamard 变换降低量化误差）。
- 结果：vs FA2 提速 1.5-2.0×；FP16 740 TFLOPs/s（75% 利用率）；FP8 ≈1.2 PFLOPs/s；FP8 误差较基线低 2.6×。

## 原始链接
- url: https://arxiv.org/abs/2407.08608
- pdf_url: https://arxiv.org/pdf/2407.08608
- github: https://github.com/Dao-AILab/flash-attention

## 一手源存档（sources/）
- [2407.08608.pdf](https://arxiv.org/pdf/2407.08608)  （arXiv 原文 PDF，不入 git）
