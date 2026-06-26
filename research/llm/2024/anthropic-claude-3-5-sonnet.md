---
title: Introducing Claude 3.5 Sonnet
org: Anthropic
country: US
date: 2024-06
type: blog
categories: [架构, 后训练, agentic训练]
url: https://www.anthropic.com/news/claude-3-5-sonnet
pdf_url:
github_url:
downloaded: [anthropic-claude-3-5-sonnet.md]
---

## 一句话定位
Claude 3.5 Sonnet 首发博客：以 Claude 3 Sonnet 的速度和成本超越 Claude 3 Opus，并引入 Artifacts 交互，agentic 编码能力大幅领先。

## 摘要
2024-06-21 发布。Claude 3.5 Sonnet 在 GPQA（研究生推理）、MMLU（本科知识）、HumanEval（编码）等树立新基准，超越竞品与自家 Claude 3 Opus，却保持中端 Sonnet 的速度与成本（$3/M 输入、$15/M 输出，200K 上下文），运行速度是 Opus 的 2 倍。在内部 agentic 编码评测中解决 64% 问题（Opus 仅 38%）。同时是 Anthropic 最强视觉模型，并在 Claude.ai 推出 Artifacts 功能。

## 关键技术细节
- 定价/上下文：$3/M 输入、$15/M 输出；200K 上下文；速度为 Opus 的 2×。
- 编码（agentic）：内部 agentic coding eval 解决 64%（Opus 38%）——给定自然语言描述，自主修 bug/加功能并执行代码。
- 视觉：超越 Opus 的视觉基准，擅长图表解读、不完美图像文字转录。
- 可用性：Claude.ai/iOS 免费提供，API、Amazon Bedrock、Google Vertex AI 均可用。
- 产品：引入 Artifacts（代码/文档/设计在侧栏实时渲染与迭代）。

## 原始链接
- url: https://www.anthropic.com/news/claude-3-5-sonnet
- 3.5 addendum model card: https://www-cdn.anthropic.com/fed9cc193a14b84131812372d8d5857f8f304c52/Model_Card_Claude_3_Addendum.pdf

## 一手源存档（sources/）
- [anthropic-claude-3-5-sonnet.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/anthropic-claude-3-5-sonnet.md)
