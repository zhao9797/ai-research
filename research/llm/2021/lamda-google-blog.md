---
title: "LaMDA: our breakthrough conversation technology"
org: Google
country: US
date: 2021-05
type: blog
categories: [架构, 后训练]
url: https://blog.google/technology/ai/lamda/
pdf_url:
github_url:
downloaded: [google-lamda-blog.html]
---

## 一句话定位
Google I/O 2021（2021-05-18）官方公布 LaMDA：专为开放域对话训练的 Transformer 语言模型，强调对话的"合理性（sensibleness）与具体性（specificity）"，是 Google 对话式大模型与后续 Bard 的起点。

## 摘要（3-6 句）
2021 年 5 月 18 日 Google 在官方博客（The Keyword）公布 LaMDA（Language Model for Dialogue Applications），一种专门为对话训练的语言模型。LaMDA 基于 Transformer 架构（与 BERT、GPT-3 同源），但专门在对话数据上训练，能就开放话题进行自由流畅、合乎情境的多轮对话。Google 强调其在"合理性与具体性"上的进步，并将持续研究其安全性与事实性（factual grounding）。

## 关键技术细节
- 架构：Transformer-based，专为 dialogue 训练（区别于通用 LM）。
- 设计目标：开放域多轮对话；衡量指标含 sensibleness（合理）与 specificity（具体）。
- 训练数据：以对话语料为主，使对话更自然、上下文连贯。
- 强调安全（safety）与事实性（factual grounding）是后续重点研究方向。
- 官方公告，非第三方；LaMDA 完整技术论文 2022 年发布（arXiv:2201.08239），本条为 2021 年首发公告。

## 原始链接
- url: https://blog.google/technology/ai/lamda/

## 一手源存档（sources/）
- [google-lamda-blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2021/google-lamda-blog.html)
