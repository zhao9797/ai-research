---
title: "HybridFlow: A Flexible and Efficient RLHF Framework (verl)"
org: ByteDance / Hong Kong University
country: China
date: 2024-09
type: paper
categories: [后训练, AI infra, agentic训练]
url: https://arxiv.org/abs/2409.19256
pdf_url: https://arxiv.org/pdf/2409.19256
github_url: https://github.com/volcengine/verl
downloaded: [hybridflow-verl-2409.19256.pdf, verl-readme.md]
---

## 一句话定位
字节提出的 RLHF 框架（开源为 verl），用 single-controller + multi-controller 混合范式表达复杂 RLHF dataflow，兼顾灵活性与效率，是当前大规模 RL post-training 最主流的框架之一。

## 摘要（3-6 句）
RLHF 可建模为 dataflow（节点是 NN 计算、边是数据依赖），但每个节点是分布式 LLM 训练/生成、每条边是多对多多播。纯 single-controller 控制开销大，纯 multi-controller 又不灵活。HybridFlow 把二者混合：上层用 single-controller 描述 RL 算法 dataflow，下层用 multi-controller 做高效分布式计算，并用一套分层 API 解耦计算与数据依赖、用 3D-HybridEngine 在训练/生成间高效 resharding。相比 SOTA 系统吞吐提升 1.5-20×。开源为 verl，被 DAPO、众多推理模型 RL 训练采用。

## 关键技术细节
- hybrid 范式：single-controller（算法编排）+ multi-controller（分布式执行）；分层 API 封装 compute/data 依赖。
- 3D-HybridEngine：actor 在训练（3D 并行）与生成（vLLM）之间零冗余/低开销 resharding，消除显存峰值与重分布开销。
- 自动 device mapping + 灵活模型放置；支持 PPO、GRPO、DAPO、RLVR 等。
- 吞吐：相比已有 RLHF 系统 1.5×–20×；支撑 DAPO（Qwen2.5-32B，AIME 50 分）。

## 原始链接
- url: https://arxiv.org/abs/2409.19256
- pdf_url: https://arxiv.org/pdf/2409.19256
- github_url: https://github.com/volcengine/verl

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/hybridflow-verl-2409.19256.pdf
- ../../../../sources/llm/themes/ai-infra/verl-readme.md
