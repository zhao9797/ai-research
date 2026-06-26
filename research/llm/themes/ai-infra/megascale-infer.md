---
title: "MegaScale-Infer: Serving Mixture-of-Experts at Scale with Disaggregated Expert Parallelism"
org: ByteDance / Peking University
country: China
date: 2025-04
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2504.02263
pdf_url: https://arxiv.org/pdf/2504.02263
downloaded: [megascale-infer-2504.02263.pdf]
---

## 一句话定位
字节面向大规模 MoE 推理的系统，把每层的 attention 与 FFN（专家）模块解耦独立部署，用 ping-pong 流水线隐藏通信，提升 MoE serving 的 GPU 利用与性价比。

## 摘要（3-6 句）
MoE 稀疏激活使 FFN 在推理时从计算密集变为访存密集，GPU 利用率低、成本高。MegaScale-Infer 在每层内把 attention 与 FFN 模块分离（disaggregated），各自独立扩展、用各自最优并行策略、异构部署。为充分利用分离 + 稀疏，提出 ping-pong pipeline parallelism：把请求 batch 切成 micro-batch 在 attention 与 FFN 间往返流转以隐藏通信。配合高性能 M2N 通信库，大幅降低每 token 成本并提高吞吐。

## 关键技术细节
- attention/FFN 模块解耦：分别独立扩展、独立并行策略（attention 用 TP/DP，FFN 用 expert parallelism）、异构 GPU 部署。
- ping-pong pipeline parallelism：micro-batch 在两类模块间往返，隐藏 all-to-all/通信开销，提升利用率。
- 定制 M2N（many-to-many）高性能通信库降低 token dispatch 开销。
- 目标：大规模 MoE serving 的 cost-per-token 下降与吞吐提升（对 DeepSeek-V3 量级 MoE）。

## 原始链接
- url: https://arxiv.org/abs/2504.02263
- pdf_url: https://arxiv.org/pdf/2504.02263

## 一手源存档（sources/）
- [megascale-infer-2504.02263.pdf](https://arxiv.org/pdf/2504.02263)  （arXiv 原文 PDF，不入 git）
