---
title: "FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision"
org: Colfax Research / Meta / NVIDIA / Georgia Tech / Princeton / Together AI
country: US
date: 2024-07
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2407.08608
pdf_url: https://arxiv.org/pdf/2407.08608
github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [flashattention3.pdf]
---

## 一句话定位
FlashAttention-3 针对 Hopper (H100) 重写注意力 kernel，用异步 Tensor Core/TMA、warp 专门化和 FP8 块量化，把 H100 利用率从 35% 提到 ~75%。

## 摘要（3-6 句）
注意力是 LLM 和长上下文应用的瓶颈。FlashAttention 通过减少显存读写加速，但 FlashAttention-2 在 H100 上仅 35% 利用率，未用上新硬件能力。FlashAttention-3 用三项技术在 Hopper GPU 上提速：(1) 利用 Tensor Core 与 TMA 的异步性，用 warp 专门化重叠计算与数据搬运；(2) 交错 block-wise matmul 与 softmax；(3) block quantization 与 incoherent processing 以利用 FP8 低精度。结果在 FP16 上达约 1.5-2× FA-2 速度、H100 上约 75% 利用率（740 TFLOPs/s），FP8 接近 1.2 PFLOPs/s，且数值误差比基线 FP8 注意力更低。

## 关键技术细节
- warp-specialization + 异步：用 H100 的异步 WGMMA Tensor Core 与 TMA，生产者/消费者 warp 重叠 GEMM 与 softmax。
- ping-pong scheduling：交错不同 warpgroup 的 matmul 与 softmax，隐藏 softmax 的非矩阵乘开销。
- FP8 支持：block quantization + incoherent processing（用随机正交变换降量化误差），FP8 精度优于 baseline。
- 性能：FP16 约 740 TFLOPs/s（~75% H100 利用率），FP8 近 1.2 PFLOPs/s；比 FA-2 快约 1.5-2×。
- 作者含 Tri Dao；面向 Hopper 架构。

## 原始链接
- url: https://arxiv.org/abs/2407.08608
- pdf_url: https://arxiv.org/pdf/2407.08608
- github_url: https://github.com/Dao-AILab/flash-attention

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/flashattention3.pdf
