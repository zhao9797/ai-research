---
title: Aligning language models to follow instructions (InstructGPT 官方博客)
org: OpenAI
country: US
date: 2022-01
type: blog
categories: [后训练]
url: https://openai.com/index/instruction-following/
pdf_url:
github_url: https://github.com/openai/following-instructions-human-feedback
downloaded: [openai-instructgpt-blog.html]
---

## 一句话定位
2022-01-27 OpenAI 官方博客介绍 InstructGPT：用 RLHF 让 GPT-3 更好遵循指令、更真实更少毒性，并宣布其成为 API 默认模型。

## 摘要
OpenAI 训练的 InstructGPT 比 GPT-3 更善于遵循用户意图，同时更真实、毒性更低。这些模型用 OpenAI 一年多前研究的 RLHF 技术训练。博客宣布 InstructGPT 模型已在 API 上以默认语言模型形式提供。1.3B 的 InstructGPT 输出在人类评测中优于 175B 的 GPT-3。

## 关键技术细节
- 发布日期：2022 年 1 月 27 日；同步上线 API 默认模型（text-davinci-001/-002 系列）。
- 方法：RLHF 三步——SFT（标注者示范）→ 奖励模型（标注者排序）→ PPO 强化学习微调。
- 关键结果：1.3B InstructGPT 人类偏好胜过 175B GPT-3；真实性提升、毒性下降；对未见指令有泛化。
- 局限：仍会产生幻觉、对错误前提可能配合、对指令措辞敏感；对齐到标注者/研究者偏好而非全体用户。
- 配套：论文 arXiv 2203.02155 + model card（GitHub following-instructions-human-feedback）。
- 意义：把 RLHF 对齐从研究推向产品 API，是 ChatGPT 的直接前置发布。

## 原始链接
- url: https://openai.com/index/instruction-following/
- github_url: https://github.com/openai/following-instructions-human-feedback

## 一手源存档（sources/）
- [openai-instructgpt-blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2022/openai-instructgpt-blog.html)
