---
title: OpenAI o1 System Card
org: OpenAI
country: US
date: 2024-12
type: model-card
categories: [后训练, agentic训练]
url: https://openai.com/index/openai-o1-system-card/
pdf_url: https://arxiv.org/pdf/2412.16720
github_url:
downloaded: [openai-o1-system-card.md, 2412.16720.pdf]
---

## 一句话定位
o1 / o1-mini 正式版的系统卡（同时挂 arXiv 2412.16720），披露安全评测、红队、Preparedness Framework 评级，并提出"deliberative alignment"（让模型在 CoT 中显式推理安全策略）。

## 摘要
o1 系列用大规模强化学习训练，用 CoT 进行推理。文中指出这些推理能力为提升安全与鲁棒性提供新途径：模型能在响应潜在不安全 prompt 时，于上下文中对安全策略进行推理（deliberative alignment），在抗越狱、拒绝违法建议、避免刻板印象等基准上达到 SOTA。报告涵盖 o1 与 o1-mini 的安全评测、外部红队、以及 Preparedness Framework（CBRN/网络/说服/模型自主）风险评级。

## 关键技术细节
- 对齐新方法：deliberative alignment —— 模型在思维链中显式引用并推理 OpenAI 的安全策略文本，再作答。
- 安全收益：在 jailbreak（如 StrongREJECT）、生成违法建议、刻板印象等安全基准上较 GPT-4o 显著提升。
- Preparedness Framework 评级：报告对 CBRN、网络安全、说服、模型自主等类别给出风险等级（多数为 Low/Medium）。
- 包含外部红队（含 Apollo Research 对欺骗/scheming 行为的测试）结果。
- arXiv 版本作者署名 "OpenAI"（265 位贡献者条目）。

## 原始链接
- url: https://openai.com/index/openai-o1-system-card/
- pdf_url: https://arxiv.org/pdf/2412.16720
- arXiv abs: https://arxiv.org/abs/2412.16720

## 一手源存档（sources/）
- [openai-o1-system-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/openai-o1-system-card.md)
- [2412.16720.pdf](https://arxiv.org/pdf/2412.16720)  （arXiv 原文 PDF，不入 git）
