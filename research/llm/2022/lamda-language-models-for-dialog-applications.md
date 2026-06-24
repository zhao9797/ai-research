---
title: LaMDA: Language Models for Dialog Applications
org: Google Research    country: US    date: 2022-01    type: paper
categories: [预训练数据, 后训练]
url: https://arxiv.org/abs/2201.08239    pdf_url: https://arxiv.org/pdf/2201.08239    github_url:
downloaded: [lamda.pdf]
---

## 一句话定位
谷歌专为对话设计的 137B 模型族，靠微调 + 调用外部工具提升安全性与事实接地（factual grounding）。

## 摘要
LaMDA 是面向对话应用的 Transformer 神经语言模型族，最大 137B 参数，在 1.56T 词的公开对话数据与网页文本上预训练。模型缩放本身能提升质量，但在安全与事实接地上提升有限。论文展示用标注数据微调、并让模型查询外部知识源，可在这两大挑战上显著改进。安全方面用基于一组人类价值观的指标量化，并用 LaMDA 分类器过滤候选回复；事实接地方面让模型调用外部检索系统。

## 关键技术细节
- 规模：2B / 8B / 137B；decoder-only Transformer，预训练 1.56T 词（公开对话 + 网页）。
- 安全微调：定义一组人类价值（避免有害建议、不公平偏见等），用众包标注训练安全分类器过滤输出。
- 事实接地（groundedness）：微调使模型学会调用外部信息检索系统（toolset：检索、计算器、翻译），把回答建立在可核查来源上——agentic 工具调用早期范式。
- 三类指标：quality（合理性/具体性/趣味性 SSI）、safety、groundedness。
- 微调用相对少量标注数据即显著提升 safety/groundedness，超过单纯缩放。
- 是谷歌对话 AI（后 Bard）的技术底座之一。

## 原始链接
- url: https://arxiv.org/abs/2201.08239
- pdf_url: https://arxiv.org/pdf/2201.08239

## 本地落盘文件
- ../../../sources/llm/2022/lamda.pdf
