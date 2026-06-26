---
title: "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning"
org: Princeton / Stanford / Dao-AILab
country: US
date: 2023-07
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2307.08691
pdf_url: https://arxiv.org/pdf/2307.08691
github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [flashattention2-2307.08691.pdf]
---

## 一句话定位
FlashAttention 的工程重写，优化 GPU 工作划分与减少非矩阵乘法运算，达到约 2× 速度、接近 GEMM 的硬件利用率。

## 摘要（3-6 句）
FlashAttention-1 的 GPU 利用率仍只有理论峰值的 25-40%，原因是 non-matmul FLOP 多、warp 间分工不佳。FlashAttention-2 减少非矩阵乘运算、把序列维并行（更好占满 SM）、优化 warp 间共享内存通信。结果比 FA-1 快约 2×，在 A100 上达到 50-73% 的理论峰值 FLOPs（接近优化 GEMM 的 80-90%）。端到端 GPT 训练达 225 TFLOPs/A100（72% MFU）。

## 关键技术细节
- 减少 non-matmul FLOP（rescaling 移到循环外）；在 forward 沿序列维并行、在 backward 优化划分。
- warp 划分优化：避免共享内存往返，提升 occupancy。
- 性能：A100 上 50-73% 峰值 FLOPs，约 2× over FA-1；GPT 训练 225 TFLOPs/GPU。
- 支持 head dim 到 256、MQA/GQA。

## 原始链接
- url: https://arxiv.org/abs/2307.08691
- pdf_url: https://arxiv.org/pdf/2307.08691
- github_url: https://github.com/Dao-AILab/flash-attention

## 一手源存档（sources/）
- [flashattention2-2307.08691.pdf](https://arxiv.org/pdf/2307.08691)  （arXiv 原文 PDF，不入 git）
