---
title: "Pathways: Asynchronous Distributed Dataflow for ML"
org: Google
country: US
date: 2022-03
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2203.12533
pdf_url: https://arxiv.org/pdf/2203.12533
downloaded: [pathways-2203.12533.pdf]
---

## 一句话定位
Google 的下一代 ML 系统运行时，用单控制器（single-controller）异步分布式 dataflow 调度数千 TPU，支撑 PaLM 等模型的稀疏/多任务/流水线编排。

## 摘要（3-6 句）
Pathways 面向新型 ML 工作负载（稀疏、多任务、跨 pod），采用 single-controller + 异步 gang-scheduling 架构，区别于传统 SPMD 多控制器。它用分片 dataflow 图与异步分发，使客户端可在不阻塞的情况下提交跨数千加速器的程序，并行执行不同子计算。论文报告在 2048 TPU 上达到与 SPMD 系统相当（约 100% 硬件利用）的性能，同时支持更灵活的并行模式。Pathways 是训练 PaLM（540B）的底层系统。

## 关键技术细节
- 架构：client → resource manager → 多个 TPU island；单控制器协调，异步派发避免 host 端串行瓶颈。
- 分片 dataflow 执行 + gang scheduling，支持 SPMD 与 MPMD/pipeline 混合。
- 通过 parallel asynchronous dispatch 隐藏跨 pod 调度延迟，2048-TPU 上接近满利用。
- 是 JAX/TF 之上的运行时，支撑 PaLM 训练（6144 TPU v4 两 pod）。

## 原始链接
- url: https://arxiv.org/abs/2203.12533
- pdf_url: https://arxiv.org/pdf/2203.12533

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/pathways-2203.12533.pdf
