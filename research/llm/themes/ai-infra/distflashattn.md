---
title: "DISTFLASHATTN: Distributed Memory-efficient Attention for Long-context LLMs Training"
org: UC Berkeley / UCSD / CMU / MBZUAI
country: US
date: 2023-10
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2310.03294
pdf_url: https://arxiv.org/pdf/2310.03294
downloaded: [distflashattn-2310.03294.pdf]
---

## 一句话定位
把 FlashAttention 分布式化的长上下文训练注意力，用 token 级负载均衡 + KV 通信重叠 + 重计算感知 checkpoint，相对 Ring Attention/DeepSpeed-Ulysses 进一步提速。

## 摘要（3-6 句）
FlashAttention 把单卡注意力峰值显存从平方降到线性，但长上下文需跨卡。DISTFLASHATTN 提出三项技术：token-level workload balancing（解决因果掩码导致的各 rank 负载不均）、overlapping KV communication（通信与计算重叠）、rematerialization-aware gradient checkpointing（重计算感知的 checkpoint，减少重算开销）。在 Llama-7B 及变体上支持 32K–512K 序列，相对 Ring Self-Attention 提速 4.45–5.64×，相对 Megatron-LM+FlashAttention 提速 1.24–2.01×，并优于 Ring Attention 与 DeepSpeed-Ulysses。

## 关键技术细节
- token-level workload balancing：针对因果 attention 三角形负载不均做跨 rank 均衡。
- overlapping KV communication：把 KV 跨卡传输与本地 attention 计算重叠。
- rematerialization-aware gradient checkpointing：避免重复重计算注意力。
- 结果：32K–512K 序列；vs Ring Self-Attention 4.45–5.64×、vs Megatron+FA 1.24–2.01×、vs Ring Attention 1.67×、vs Ulysses 1.26–1.88×。

## 原始链接
- url: https://arxiv.org/abs/2310.03294
- pdf_url: https://arxiv.org/pdf/2310.03294

## 一手源存档（sources/）
- [distflashattn-2310.03294.pdf](https://arxiv.org/pdf/2310.03294)  （arXiv 原文 PDF，不入 git）
