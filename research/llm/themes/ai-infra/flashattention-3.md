---
title: "FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision"
org: Colfax / Meta / NVIDIA / Together AI / Princeton / Dao-AILab
country: US
date: 2024-07
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2407.08608
pdf_url: https://arxiv.org/pdf/2407.08608
github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [flashattention3-2407.08608.pdf]
---

## 一句话定位
针对 Hopper（H100）重写 FlashAttention，利用 warp-specialization 异步、TMA、FP8 低精度，把注意力吞吐再提升约 1.5-2×。

## 摘要（3-6 句）
FlashAttention-2 没充分利用 Hopper 的新特性。FA-3 用三类技术：通过 warp-specialization 与 block-wise 调度让 Tensor Core（WGMMA）与 TMA 异步重叠、把 softmax 与 GEMM 交错隐藏延迟、用 incoherent processing 让 FP8 注意力保持精度。在 H100 上 FP16 达 740 TFLOPs（75% 利用率，1.5-2× over FA-2），FP8 接近 1.2 PFLOPs，且 FP8 数值误差比基线低 2.6×。

## 关键技术细节
- 异步：warp-specialized producer/consumer，WGMMA + TMA 与 softmax 重叠（pingpong/intra-warpgroup pipelining）。
- 低精度：FP8 注意力 + block quantization + incoherent processing（用 Hadamard 变换）降误差，误差较基线低 2.6×。
- 性能：H100 FP16 ~740 TFLOPs（75% 峰值），FP8 接近 1.2 PFLOPs。
- 专为 Hopper SM90 设计，利用 TMA、FP8 Tensor Core。

## 原始链接
- url: https://arxiv.org/abs/2407.08608
- pdf_url: https://arxiv.org/pdf/2407.08608
- github_url: https://github.com/Dao-AILab/flash-attention

## 一手源存档（sources/）
- [flashattention3-2407.08608.pdf](https://arxiv.org/pdf/2407.08608)  （arXiv 原文 PDF，不入 git）
