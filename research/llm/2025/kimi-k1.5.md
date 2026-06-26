---
title: "Kimi k1.5: Scaling Reinforcement Learning with LLMs"
org: 月之暗面 Moonshot AI
country: China
date: 2025-01
type: paper
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2501.12599
pdf_url: https://arxiv.org/pdf/2501.12599
github_url: https://github.com/MoonshotAI/Kimi-k1.5
downloaded: [kimi-k1.5.pdf]
---

## 一句话定位
月之暗面首个用 RL 训练的多模态推理模型，靠 long-context scaling + 简洁 RL 框架（不用 MCTS/value function/PRM）达到 o1 级别，并提出 long2short 把长 CoT 能力压到短 CoT。发布 2025-01-22。

## 摘要
Kimi k1.5 报告了用 RL 训练多模态 LLM 的实践：RL 训练技巧、多模态数据配方、infra 优化。关键在 long context scaling 与改进的策略优化方法，建立了一个简洁有效的 RL 框架，不依赖 MCTS、value function、process reward model 等复杂技术。系统在多 benchmark/模态上达 SOTA：AIME 77.5、MATH500 96.2、Codeforces 94 百分位、MathVista 74.9，匹敌 OpenAI o1。提出 long2short 方法用长 CoT 改进短 CoT 模型，短 CoT 也达 SOTA（AIME 60.8、MATH500 94.6、LiveCodeBench 47.3），大幅超过 GPT-4o / Claude 3.5 Sonnet。

## 关键技术细节
- RL 框架：简洁有效，不用 MCTS / value function / process reward model；用 online policy mirror descent 变体做策略优化。
- Long context scaling：把 RL 上下文扩到 128K，部分回放（partial rollouts）提升训练效率，是性能提升关键。
- 多模态：文本 + 视觉联合 RL 训练；公布多模态数据配方。
- long2short：用长 CoT 模型（model merging / DPO / shortest-rejection sampling）改进短 CoT 模型，控制 token 预算。
- 成绩：AIME 77.5、MATH500 96.2、Codeforces 94th、MathVista 74.9（long-CoT，匹敌 o1）。
- Infra：大规模 RL 训练系统优化（含 code sandbox、混合部署）。

## 原始链接
- url: https://arxiv.org/abs/2501.12599
- pdf_url: https://arxiv.org/pdf/2501.12599
- github_url: https://github.com/MoonshotAI/Kimi-k1.5

## 一手源存档（sources/）
- kimi-k1.5.pdf  （PDF 不入 git，走 HF bucket）
