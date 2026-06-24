---
title: "AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning"
org: Ant Group / Tsinghua University (IIIS)
country: China
date: 2025-05
type: paper
categories: [后训练, AI infra, agentic训练]
url: https://arxiv.org/abs/2505.24298
pdf_url: https://arxiv.org/pdf/2505.24298
github_url: https://github.com/inclusionAI/AReaL
downloaded: [areal-2505.24298.pdf]
---

## 一句话定位
全异步 RL 训练系统，把生成（rollout）与训练完全解耦，rollout worker 持续产数据、training worker 一攒够 batch 就更新，靠 staleness 控制 + staleness-enhanced PPO 保稳，大幅提升 GPU 利用。

## 摘要（3-6 句）
现有大规模 RL 系统多为同步：每个 batch 的 rollout 由同一（最新）模型生成，但必须等最长输出完成才更新，GPU 严重空转。AReaL（Ant Reinforcement learning）让 rollout worker 不间断生成、training worker 随时用攒满的数据更新模型，完全解耦二者。为稳住训练，它平衡 rollout/training 负载以控制数据 staleness，并用 staleness-enhanced PPO 变体。配合系统级优化，GPU 利用与端到端训练速度显著高于同步系统。

## 关键技术细节
- 全异步架构：rollout 与 training 解耦，rollout 持续生成、training 异步更新，消除「等最长序列」空转。
- 稳定性：interruptible rollout、数据 staleness 控制、staleness-enhanced PPO（对陈旧数据加权/裁剪）。
- 系统优化：高利用率调度，相对同步 RL 端到端大幅提速（论文报告数倍训练加速）。
- 面向 reasoning（数学/代码）大规模 RL；开源 AReaL（含 AReaL-lite）。

## 原始链接
- url: https://arxiv.org/abs/2505.24298
- pdf_url: https://arxiv.org/pdf/2505.24298
- github_url: https://github.com/inclusionAI/AReaL

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/areal-2505.24298.pdf
