---
title: Ring Attention with Blockwise Transformers for Near-Infinite Context
org: UC Berkeley
country: US
date: 2023-10
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2310.01889
pdf_url: https://arxiv.org/pdf/2310.01889
downloaded: [ring-attention-2310.01889.pdf]
---

## 一句话定位
把长序列沿设备成环切分，每张卡持有一段 KV 并以环形通信传递块，使上下文长度随设备数线性扩展、几乎无显存上限。

## 摘要（3-6 句）
Ring Attention 将输入序列分块分布到多设备，计算 blockwise attention/FFN 时把 KV block 在设备环上轮转传递，并将该通信与计算重叠。由此单设备只需存一个块的激活，整体可支持的上下文随设备数线性增长，且不引入近似。论文展示可训练比之前长数倍（设备数倍）的上下文，达到“near-infinite context”。它与 blockwise parallel transformer 配合，是序列/上下文并行（CP）的代表方法。

## 关键技术细节
- 序列分块 + 环形 KV 传递（每步把本地 KV 发给下一 rank），通信与 blockwise 计算重叠以零额外开销。
- 显存：单卡仅存 1/N 序列的激活，最大上下文 ∝ 设备数。
- 精确注意力（exact），与 FlashAttention 思想兼容（blockwise online softmax）。
- 是 context parallelism（CP）在 Megatron/torchtitan 等系统中的算法基础。

## 原始链接
- url: https://arxiv.org/abs/2310.01889
- pdf_url: https://arxiv.org/pdf/2310.01889

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/ring-attention-2310.01889.pdf
