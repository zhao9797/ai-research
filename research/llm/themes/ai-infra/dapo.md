---
title: "DAPO: An Open-Source LLM Reinforcement Learning System at Scale"
org: ByteDance Seed / Tsinghua University (AIR)
country: China
date: 2025-03
type: paper
categories: [后训练, AI infra, agentic训练]
url: https://arxiv.org/abs/2503.14476
pdf_url: https://arxiv.org/pdf/2503.14476
github_url: https://github.com/volcengine/verl
downloaded: [dapo-2503.14476.pdf]
---

## 一句话定位
完全开源的大规模推理 RL 系统与算法（Decoupled Clip + Dynamic Sampling Policy Optimization），用 Qwen2.5-32B base 在 AIME 2024 取得 50 分，公开训练代码（基于 verl）与数据。

## 摘要（3-6 句）
针对 o1/R1 训练细节不透明、社区难复现的问题，DAPO 提出并完全开源一套 SOTA 大规模 RL 系统：算法上给出四项关键技术，系统上基于 verl 框架。用 Qwen2.5-32B base 在 AIME 2024 达 50 分，超过 DeepSeek-R1-Zero-Qwen-32B 的 47 分且只用约一半训练步数。论文同时开源代码、精选数据集，强调可复现性，是研究推理型 RL（RLVR）的重要一手系统。

## 关键技术细节
- 算法四技巧：Clip-Higher（解耦上下裁剪上限，防熵塌缩）、Dynamic Sampling（过滤全对/全错样本提升梯度有效性）、Token-Level Policy Gradient Loss（长 CoT 友好）、Overlong Reward Shaping（长度惩罚降噪）。
- 基于 GRPO 改进，去掉 KL 项、规避长度偏置。
- 系统：基于 verl（volcengine/verl）；Qwen2.5-32B base，AIME 2024 = 50（vs R1-Zero-Qwen-32B 47），约 50% 步数。
- 完全开源代码 + 数据集，强调可复现。

## 原始链接
- url: https://arxiv.org/abs/2503.14476
- pdf_url: https://arxiv.org/pdf/2503.14476
- github_url: https://github.com/volcengine/verl

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/dapo-2503.14476.pdf
