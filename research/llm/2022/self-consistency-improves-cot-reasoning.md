---
title: Self-Consistency Improves Chain of Thought Reasoning in Language Models
org: Google Research (Brain)
country: US
date: 2022-03
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2203.11171
pdf_url: https://arxiv.org/pdf/2203.11171
github_url:
downloaded: [self-consistency.pdf]
---

## 一句话定位
用"采样多条推理路径 + 多数投票"替代贪心解码，大幅提升 CoT 推理准确率，是测试时计算（test-time scaling）的早期范式。

## 摘要
提出 self-consistency 解码策略替代 CoT 中的贪心解码：从语言模型采样多条不同的推理路径，然后对最终答案做多数投票（marginalize over reasoning paths）。直觉是复杂推理问题往往有多条正确路径殊途同归。该方法在一系列算术与常识推理基准上显著提升 CoT 性能。

## 关键技术细节
- 方法：对同一问题用温度采样生成多条 CoT 推理路径，取出各自最终答案，按出现频次多数投票。
- 无需额外训练、无需验证器、无需人工标注，纯解码期技巧。
- 提升幅度（配 PaLM-540B / GPT-3 等）：GSM8K +17.9%，SVAMP +11.0%，AQuA +12.2%，StrategyQA +6.4%，ARC-challenge +3.9%。
- 采样路径数越多收益越高（典型 40 条），呈现"测试时算力换准确率"的缩放。
- 是后续 reasoning model（o1/R1 思路）测试时扩展的思想源头之一。

## 原始链接
- url: https://arxiv.org/abs/2203.11171
- pdf_url: https://arxiv.org/pdf/2203.11171

## 一手源存档（sources/）
- self-consistency.pdf  （PDF 不入 git，走 HF bucket）
