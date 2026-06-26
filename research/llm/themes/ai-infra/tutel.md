---
title: "Tutel: Adaptive Mixture-of-Experts at Scale"
org: Microsoft
country: US
date: 2022-06
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2206.03382
pdf_url: https://arxiv.org/pdf/2206.03382
github_url: https://github.com/microsoft/tutel
downloaded: [tutel-2206.03382.pdf]
---

## 一句话定位
为 MoE 设计的可在运行时「自适应并行/流水」的高扩展性系统：用同一套布局让所有并行/流水方式零成本切换，适配 token 路由带来的动态专家负载。

## 摘要（3-6 句）
稀疏门控 MoE 靠 token 路由把每个 token 分给合适的专家，但路由在运行时动态决定各专家工作量，而现有系统采用静态并行与静态流水，无法适应这种动态负载，导致算力浪费。Tutel（论文内系统命名 Flex）为分发 MoE 参数与输入数据设计了「同一种布局」，任何并行或流水方式都能直接复用，无数学不等价、无张量迁移开销，从而可在运行时零成本做自适应并行/流水优化。基于此再叠加多种 MoE 加速技术后，单个 MoE 层在 16 卡和 2048 卡 A100 上分别比此前 SOTA 快 4.96× 和 5.75×。在真实模型 SwinV2-MoE（基于 Swin Transformer V2）上训练/推理比 Fairseq 快最高 1.55×/2.11×，且精度优于对应 dense 模型。

## 关键技术细节
- 核心设计：为 MoE 模型参数与输入数据采用「同一种布局」（identical layout），使所有可能的并行/流水方法都能复用而无数学不等价或张量迁移开销，实现运行时零成本的自适应并行+自适应流水优化。
- 单 MoE 层加速（vs 此前 SOTA）：16 卡 A100 上 4.96×；2048 卡 A100 上 5.75×。
- 端到端真实模型 SwinV2-MoE（建在 Swin Transformer V2 上）：训练比 Fairseq 快最高 1.55×，推理快最高 2.11×；预训练与下游任务（如 COCO 目标检测）精度均优于对应 dense 模型。
- 适配动态 token 路由负载，解决静态并行/静态流水带来的计算低效。
- 开源 microsoft/tutel，被广泛用作 MoE 训练/推理后端（如对比 MegaBlocks 等系统时的 baseline）。

## 原始链接
- url: https://arxiv.org/abs/2206.03382
- pdf_url: https://arxiv.org/pdf/2206.03382
- github_url: https://github.com/microsoft/tutel

## 一手源存档（sources/）
- [tutel-2206.03382.pdf](https://arxiv.org/pdf/2206.03382)  （arXiv 原文 PDF，不入 git）
