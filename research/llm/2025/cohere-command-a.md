---
title: Command A - An Enterprise-Ready Large Language Model
org: Cohere
country: Canada
date: 2025-03
type: technical-report
categories: [架构, 后训练, AI infra, agentic训练]
url: https://arxiv.org/abs/2504.00698
pdf_url: https://cohere.com/research/papers/command-a-technical-report.pdf
github_url:
downloaded: [files/command-a.pdf]
---

## 一句话定位
Cohere 的 Command A 技术报告：111B 参数、面向企业 RAG/工具使用/agentic 的多语言模型，采用 sliding-window+full attention 3:1 的混合架构与去中心化训练（self-refinement + model merging）。

## 摘要
Command A 是面向真实企业用例的 111B 模型，支持 23 种商业语言，新型 hybrid 架构兼顾效率与顶级性能，具备 best-in-class RAG（grounding + tool use）以自动化复杂业务流程。训练采用去中心化方法（self-refinement 算法 + model merging）。报告还给出与之架构/能力相似的 Command R7B，两者权重均供研究使用。Command A 单/多卡可达 156 tokens/s（1.75x GPT-4o）。

## 关键技术细节（带数字）
- 参数：111B（Command A）；并发布 Command R7B（7B，相似架构/能力）。
- 架构：interleaved sliding window attention 与 full attention 按 3:1 交错；sliding window 层用 RoPE；GQA 提升吞吐；上下文 256k tokens。
- 超参：µP / µTransfer 在小模型上调参后迁移。
- 训练基础设施：NVIDIA H100 集群 + 内部 JAX/GSPMD 分布式框架；DP + 序列并行（sequence parallelism）+ FSDP；利用 Hopper FP8 tensor cores。
- 训练方法：去中心化（decentralised）训练 + self-refinement 算法 + model merging（把多个专家模型合并出最终家族）。
- 能力：23 种语言；best-in-class RAG（grounding + tool use）、agentic 业务流程自动化。
- 吞吐：最高 156 tokens/s（约 1.75x GPT-4o）。
- 发布：2025-03（模型发布）；arXiv:2504.00698。

## 原始链接
- arXiv：https://arxiv.org/abs/2504.00698
- 官方 PDF：https://cohere.com/research/papers/command-a-technical-report.pdf

## 一手源存档（sources/）
- command-a.pdf  （PDF 不入 git，走 HF bucket）
