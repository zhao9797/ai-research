---
title: Efficiently Scaling Transformer Inference
org: Google
country: US
date: 2022-11
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2211.05102
pdf_url: https://arxiv.org/pdf/2211.05102
downloaded: [efficiently-scaling-inference-2211.05102.pdf]
---

## 一句话定位
Google 系统性给出 500B+ 模型在 TPU v4 上推理的分区（partitioning）分析框架，权衡延迟与 MFU，为大模型多芯片推理选并行策略提供原则。

## 摘要（3-6 句）
论文针对超大 Transformer 推理提出一套分区策略分析：给定延迟与芯片数约束，如何在权重/激活上选 1D/2D 张量切分以最小化通信与延迟。结合 multiquery attention（缩小 KV cache）支持 32K+ 上下文，并讨论 PaLM 540B 量级的部署。在 TPU v4 上对 500B 模型实现低延迟（首 token 29ms 量级）与高 MFU（76% 量级），给出延迟优先与吞吐优先两种 partitioning 配方。

## 关键技术细节
- partitioning 分析：weight-stationary / weight-gathered 等布局，1D/2D 张量并行通信代价建模。
- 用 multiquery attention（MQA）大幅减小 KV cache，支撑长上下文（32K）解码。
- PaLM 540B 在 64 TPU v4 上：低批延迟与高 MFU（吞吐优先 76% MFU）之间的 Pareto。
- 给出生成（decode）与预填充（prefill）不同最优分区的工程结论。

## 原始链接
- url: https://arxiv.org/abs/2211.05102
- pdf_url: https://arxiv.org/pdf/2211.05102

## 一手源存档（sources/）
- [efficiently-scaling-inference-2211.05102.pdf](https://arxiv.org/pdf/2211.05102)  （arXiv 原文 PDF，不入 git）
