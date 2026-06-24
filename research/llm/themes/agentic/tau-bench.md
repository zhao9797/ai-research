---
title: "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"
org: "Sierra (Bret Taylor) / 等"
country: US
date: 2024-06
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2406.12045
pdf_url: https://arxiv.org/pdf/2406.12045
github_url: https://github.com/sierra-research/tau-bench
downloaded: [tau-bench-2406.12045.pdf]
---

## 一句话定位
首个评测"工具-agent-用户"三方交互的基准：用 LM 模拟用户与 agent 多轮对话，按数据库终态判定成败，并用 pass^k 度量可靠性，揭示 function-calling agent 的不一致性问题。

## 摘要
τ-bench 模拟"用户(由 LM 扮演)"与"被赋予领域 API 工具和策略规则的语言 agent"之间的动态对话。评测方式高效且忠实：把对话结束时的数据库状态与标注的目标状态比对来判定是否成功。论文还提出新指标 pass^k 评估 agent 在多次试验中的行为可靠性。实验显示即便是 SOTA function-calling agent(如 gpt-4o) 成功率也 <50%，且很不一致(零售域 pass^8 <25%)。结论指向需要能让 agent 行为更一致、可靠遵循规则的方法。

## 关键技术细节
- 设置：两域(零售 retail、航空 airline)，agent 配领域 API 工具 + 政策指南(policy)，与 LM 模拟用户多轮对话。
- 评测：比较对话终态数据库 vs 目标状态(执行级、可自动判定)。
- 新指标 pass^k：同一任务跑 k 次全部成功的概率，衡量可靠性/一致性(而非单次 pass@1)。
- 结果：gpt-4o 等 SOTA 单次成功率 <50%；retail 域 pass^8 <25%，说明严重不一致。
- 衍生：τ²-bench(2025) 进一步扩展用户也能操作的双控场景；被 GLM-4.5、Kimi K2 等作为核心 agentic 评测(TAU-Bench/Tau2-Bench)。

## 原始链接
- url: https://arxiv.org/abs/2406.12045
- pdf_url: https://arxiv.org/pdf/2406.12045
- github_url: https://github.com/sierra-research/tau-bench

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/tau-bench-2406.12045.pdf
