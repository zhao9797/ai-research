---
title: "DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence"
org: DeepSeek-AI
country: 中国
date: 2024-06
type: arxiv
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2406.11931
pdf_url: https://arxiv.org/pdf/2406.11931
github_url: https://github.com/deepseek-ai/DeepSeek-Coder-V2
downloaded: [files/deepseek-coder-v2.pdf]
---

## 一句话定位
基于 DeepSeek-V2 继续预训练 6T token 的开源 MoE 代码模型，代码任务比肩 GPT-4-Turbo，支持语言从 86 扩到 338 种、上下文从 16K 扩到 128K。

## 摘要
DeepSeek-Coder-V2 是开源 MoE 代码语言模型，从 DeepSeek-V2 的中间 checkpoint 继续预训练额外 6T token，大幅增强代码与数学推理能力，同时保持通用与语言能力。代码专项任务上达到与 GPT-4-Turbo 可比的水平。

## 关键技术细节（带数字）
- 架构：沿用 DeepSeek-V2 MoE（MLA + DeepSeekMoE）；提供 16B（2.4B 激活）与 236B（21B 激活）两档。
- 继续预训练：在 DeepSeek-V2 中间 checkpoint 基础上 +6T tokens。
- 语料配比：60% 源代码 + 10% 数学语料 + 30% 自然语言。
- 编程语言：支持从 86 种扩展到 338 种。
- 上下文：从 16K 扩展到 128K。
- 后训练：SFT + GRPO 强化学习。
- 性能：HumanEval、MBPP+、MATH、GSM8K 等代码与数学基准上达到开源 SOTA，代码任务比肩 GPT-4-Turbo。

## 原始链接
- arXiv: https://arxiv.org/abs/2406.11931
- PDF: https://arxiv.org/pdf/2406.11931
- GitHub: https://github.com/deepseek-ai/DeepSeek-Coder-V2

## 一手源存档（sources/）
- deepseek-coder-v2.pdf  （PDF 不入 git，走 HF bucket）
