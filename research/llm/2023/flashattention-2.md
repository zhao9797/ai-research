---
title: FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
org: Stanford / Princeton
country: US
date: 2023-07
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2307.08691
pdf_url: https://arxiv.org/pdf/2307.08691
github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [flashattention-2.pdf]
---

## 一句话定位
Tri Dao 的 FlashAttention-2，重排并行与工作划分，A100 上注意力达硬件峰值 50-73%，长上下文训练基础设施。

## 摘要
注意力层是扩展到长序列的主瓶颈(随序列长度二次)。FlashAttention 用 GPU 显存层级实现线性显存+2-4x 提速且无近似，但仅达理论 FLOPs 的 25-40%。FlashAttention-2 通过更好的工作划分：(1)减少非 matmul FLOPs，(2)单头内跨 thread block 并行提高占用率，(3)block 内 warp 间分工减少 shared memory 通信，较 FA1 再 2x 提速，A100 上达理论峰值 50-73%；端到端训 GPT 风格模型达 225 TFLOPs/s/A100(72% MFU)。

## 关键技术细节
- 优化1：减少非矩阵乘 FLOPs（rescaling 重排）。
- 优化2：在序列长度维度上并行（单 attention head 也跨 thread blocks），提升 GPU 占用率。
- 优化3：warp 间重新分工，减少 shared memory 读写。
- 性能：FA2 较 FA1 约 2x；A100 上 50-73% 理论 FLOPs；端到端 225 TFLOPs/s/A100、72% MFU。
- 无近似，精确注意力；支持 MQA/GQA、因果掩码。

## 原始链接
- url: https://arxiv.org/abs/2307.08691
- pdf_url: https://arxiv.org/pdf/2307.08691
- github_url: https://github.com/Dao-AILab/flash-attention

## 本地落盘文件
- ../../../sources/llm/2023/flashattention-2.pdf
