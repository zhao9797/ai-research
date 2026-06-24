---
title: "Apple Intelligence Foundation Language Models"
org: Apple
country: US
date: 2024-07
type: report
categories: [架构, AI infra, 后训练]
url: https://arxiv.org/abs/2407.21075
pdf_url: https://arxiv.org/pdf/2407.21075
github_url:
downloaded: [2407.21075.pdf]
---

## 一句话定位
Apple Intelligence 基础模型技术报告：一个约 3B 的端侧模型 + 一个用于 Private Cloud Compute 的服务器模型，详述架构、数据、训练、推理优化与负责任 AI。

## 摘要
本文介绍为 Apple Intelligence 功能打造的基础语言模型：一个约 30 亿参数、为端侧高效运行设计的模型（AFM-on-device），以及一个为 Private Cloud Compute 设计的大服务器模型（AFM-server）。模型旨在高效、准确、负责任地完成广泛任务。报告描述模型架构、训练数据、训练过程、推理优化、评测结果，并强调负责任 AI 原则贯穿全程。

## 关键技术细节
- AFM-on-device：约 3B 参数；为内存/延迟优化（GQA、共享 input/output embedding、low-bit palettization 量化）。
- AFM-server：大模型，跑在 Private Cloud Compute（隐私保护推理）。
- 数据：授权出版数据 + AppleBot 网页 + 代码/数学/合成；强调不使用用户私有数据。
- 训练 infra：用 AXLearn（基于 JAX）在 TPU 上训练；AFM-server 用 8192 TPUv4，AFM-on-device 用 2048 TPUv5p。
- 后训练：SFT + RLHF，提出两种新算法 iTeC（迭代教学委员会）与 MDLOO（含 leave-one-out 优势估计的 online RL）。
- 适配：用 LoRA adapter 为不同功能动态切换（端侧按任务加载 adapter）。

## 原始链接
- url: https://arxiv.org/abs/2407.21075
- pdf_url: https://arxiv.org/pdf/2407.21075

## 本地落盘文件
- ../../../sources/llm/2024/2407.21075.pdf
