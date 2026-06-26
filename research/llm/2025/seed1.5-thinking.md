---
title: "Seed1.5-Thinking: Advancing Superb Reasoning Models with Reinforcement Learning"
org: 字节跳动 Seed (ByteDance Seed)
country: China
date: 2025-04
type: paper
categories: [后训练, AI infra, agentic训练]
url: https://arxiv.org/abs/2504.13914
pdf_url: https://arxiv.org/pdf/2504.13914
github_url:
downloaded: [seed1.5-thinking.pdf]
---

## 一句话定位
字节 Seed 的 RL 推理模型，200B 总参 / 20B 激活的小型 MoE，AIME 2024 86.7、Codeforces 55.0、GPQA 77.3，非推理任务胜率超 DeepSeek-R1 8%。发布 2025-04-10（即豆包/Seed 系列推理模型）。

## 摘要
Seed1.5-Thinking 在响应前先思考，在广泛 benchmark 上提升表现：AIME 2024 86.7、Codeforces 55.0、GPQA 77.3，STEM 与编程推理能力突出。该方法在多领域泛化良好，非推理任务上胜率超 DeepSeek R1 达 8%。相较其他 SOTA 推理模型，Seed1.5-Thinking 是相对小型的 MoE：20B 激活、200B 总参。报告详述 RL 训练方法、数据与 infra。

## 关键技术细节
- 架构：MoE，200B 总参 / 20B 激活（相对同类更小）。
- RL：大规模强化学习（可验证任务 reward + reward model）；详述数据配方与 RL infra。
- 数据：覆盖 STEM、编程及通用领域，强调泛化。
- 成绩：AIME 2024 86.7、Codeforces 55.0、GPQA 77.3；非推理任务胜率超 DeepSeek-R1 8%。
- 机构：字节跳动 Seed 团队（豆包底层推理模型）。

## 原始链接
- url: https://arxiv.org/abs/2504.13914
- pdf_url: https://arxiv.org/pdf/2504.13914

## 一手源存档（sources/）
- seed1.5-thinking.pdf  （PDF 不入 git，走 HF bucket）
