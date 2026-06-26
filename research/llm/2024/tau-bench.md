---
title: "tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"
org: Sierra
country: US
date: 2024-06
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2406.12045
pdf_url: https://arxiv.org/pdf/2406.12045
github_url: https://github.com/sierra-research/tau-bench
downloaded: [2406.12045.pdf]
---

## 一句话定位
τ-bench（tau-bench）：评测语言 agent 与（模拟）人类用户多轮交互、并遵守领域规则的基准，提出 pass^k 衡量可靠性，揭示即便 GPT-4o 成功率也 <50%。

## 摘要
现有基准不测试 agent 与人类用户的交互、也不测遵守领域特定规则的能力，而这两者对真实部署至关重要。τ-bench 模拟用户（由 LM 模拟）与配备领域 API 工具和策略指南的语言 agent 之间的动态对话。采用高效且忠实的评测：对话结束时比较数据库状态与标注的目标状态。还提出新指标 pass^k 评测多次试验中 agent 行为的可靠性。实验显示即便 SOTA 函数调用 agent（如 gpt-4o）成功率 <50%，且很不一致（retail 域 pass^8 <25%）。结论指出需要让 agent 更一致行动、可靠遵守规则的方法。

## 关键技术细节
- 设置：retail 与 airline 两个真实领域；agent 有领域 API 工具 + 策略文档；用户由 LM 模拟，多轮交互。
- 评测：对比对话结束时数据库状态 vs 目标状态（结果可验证）。
- pass^k 指标：同一任务跑 k 次全部成功的概率，衡量可靠性/一致性（非单次成功率）。
- 关键发现：gpt-4o 等单次成功率 <50%；retail pass^8 <25%（一致性极差）。
- 影响：成为 agentic 工具使用的标准评测（Claude 3.5 等都报告 τ-bench 分数）。

## 原始链接
- url: https://arxiv.org/abs/2406.12045
- pdf_url: https://arxiv.org/pdf/2406.12045
- github: https://github.com/sierra-research/tau-bench

## 一手源存档（sources/）
- [2406.12045.pdf](https://arxiv.org/pdf/2406.12045)  （arXiv 原文 PDF，不入 git）
