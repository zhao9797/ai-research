---
title: "Kimi k1.5: Scaling Reinforcement Learning with LLMs"
org: "Moonshot AI (月之暗面 / Kimi Team)"
country: China
date: 2025-01
type: report
categories: [后训练, AI infra, agentic训练]
url: https://arxiv.org/abs/2501.12599
pdf_url: https://arxiv.org/pdf/2501.12599
github_url: https://github.com/MoonshotAI/Kimi-k1.5
downloaded: [kimi-k1.5-2501.12599.pdf]
---

## 一句话定位
月之暗面用"长上下文 + 简化策略优化"做大规模 RL 的多模态推理模型，不用 MCTS/价值函数/过程奖励即对标 o1，并提出 long2short 把长思考能力压回短模型——是把 RL 当作新 scaling 轴的代表报告。

## 摘要
预训练的 next-token prediction 受限于可用数据量；扩展 RL 打开了 AI 持续提升的新维度——LLM 可通过"带奖励的探索"扩充训练数据。Kimi k1.5 是用 RL 训练的最新多模态 LLM，报告其 RL 训练技术、多模态数据配方与基础设施优化。长上下文扩展(long context scaling) 与改进的策略优化方法是关键，建立了一个简洁有效的 RL 框架，不依赖 MCTS、价值函数、过程奖励模型等复杂技术。系统在多基准多模态上达 SOTA：AIME 77.5、MATH500 96.2、Codeforces 94 百分位、MathVista 74.9，与 OpenAI o1 相当。还提出 long2short 方法——用长 CoT 技术改进短 CoT 模型，得到 SOTA 短 CoT 结果(AIME 60.8、MATH500 94.6、LiveCodeBench 47.3)，大幅超过 GPT-4o、Claude Sonnet 3.5(最高 +550%)。

## 关键技术细节
- 训练范式：大规模 RL；刻意"做减法"——不用 MCTS、不用单独价值函数、不用过程奖励模型(PRM)，靠长上下文 + 改进的策略优化(在线镜像下降式更新、长度惩罚等)。
- 长上下文 RL：把上下文/思考长度扩到很长(128k 级)，让模型用更长思考探索，是性能关键。
- 多模态：文本 + 视觉联合 RL；数据配方覆盖多模态推理。
- long2short：把长 CoT 模型的能力蒸馏/合并回短 CoT 模型，提升短输出下的推理。
- 结果：long-CoT 对标 o1(AIME 77.5/MATH500 96.2/Codeforces 94th/MathVista 74.9)；short-CoT SOTA(AIME 60.8 等)。
- infra：报告了 RL 训练的基础设施优化(partial rollout、长序列训练等)。

## 原始链接
- url: https://arxiv.org/abs/2501.12599
- pdf_url: https://arxiv.org/pdf/2501.12599
- github_url: https://github.com/MoonshotAI/Kimi-k1.5

## 一手源存档（sources/）
- [kimi-k1.5-2501.12599.pdf](https://arxiv.org/pdf/2501.12599)  （arXiv 原文 PDF，不入 git）
