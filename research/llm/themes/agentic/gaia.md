---
title: "GAIA: a benchmark for General AI Assistants"
org: "Meta AI (FAIR) / HuggingFace / AutoGPT"
country: US
date: 2023-11
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2311.12983
pdf_url: https://arxiv.org/pdf/2311.12983
github_url: https://huggingface.co/gaia-benchmark
downloaded: [gaia-2311.12983.pdf]
---

## 一句话定位
通用 AI 助手的标尺：提出对人简单、对 AI 极难的真实问题(需推理+多模态+网页浏览+工具使用)，人类 92% 而装插件 GPT-4 仅 15%，成为 deep research / 通用 agent 的核心评测。

## 摘要
GAIA 是面向通用 AI 助手的基准，若被攻克将是 AI 研究里程碑。它提出真实世界问题，需要一组基础能力：推理、多模态处理、网页浏览、以及总体工具使用熟练度。GAIA 的问题对人类概念上简单、对最先进 AI 却很难：人类回答正确率 92%，而装了插件的 GPT-4 仅 15%。这一显著差距与"LLM 在法律/化学等专业任务上超越人类"的趋势形成对比。GAIA 的理念与"追求对人类越来越难的任务"潮流相反——它认为通用 AI 的到来应体现在对人简单的稳健性任务上。共 466 个问题，分三个难度级别。

## 关键技术细节
- 任务：466 道真实问题，分 3 个难度等级；需多步推理、网页浏览、读文件/表格/图像、调用工具综合作答。
- 评测：答案唯一、可自动比对(quasi-exact match)，避免主观评分。
- 基线：人类 92% vs GPT-4+plugins 15%。
- 影响：成为 agentic 信息检索/deep research 的标准基准——WebDancer、WebSailor、OpenAI/Google deep research 等均以 GAIA 为核心指标。
- 出自 Meta FAIR(Yann LeCun 等署名)、HuggingFace、AutoGPT 合作。

## 原始链接
- url: https://arxiv.org/abs/2311.12983
- pdf_url: https://arxiv.org/pdf/2311.12983
- github_url: https://huggingface.co/gaia-benchmark

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/gaia-2311.12983.pdf
