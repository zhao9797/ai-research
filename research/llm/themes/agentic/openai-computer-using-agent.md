---
title: "Computer-Using Agent (CUA)"
org: OpenAI
country: US
date: 2025-01
type: blog
categories: [后训练, agentic训练]
url: https://openai.com/index/computer-using-agent/
pdf_url:
github_url:
downloaded: [openai-computer-using-agent.html]
---

## 一句话定位
OpenAI 官方介绍驱动 Operator 的 CUA 模型：把 GPT-4o 的视觉与强化学习习得的推理结合，像人一样看 GUI、用键鼠操作，无需 OS/网页专用 API，在 OSWorld/WebArena/WebVoyager 刷新 SOTA。

## 摘要
2025-01-23，OpenAI 介绍 Computer-Using Agent(CUA)——驱动 Operator 研究预览的模型。CUA 通过强化学习把 GPT-4o 的视觉能力与高级推理结合，经训练后能像人一样与 GUI(屏幕上的按钮、菜单、文本框)交互，从而无需 OS/网页专用 API 即可灵活执行数字任务。CUA 建立在多年多模态理解与推理研究之上，能把任务拆为多步计划并在遇到挑战时自适应自我纠错。虽仍处早期且有局限，但创造了新的 SOTA：OSWorld(全计算机使用任务) 38.1%、WebArena 58.1%、WebVoyager(网页任务) 87%。

## 关键技术细节
- 基座/方法：GPT-4o 视觉 + 强化学习习得的推理；端到端感知-推理-行动循环(感知截图→链式推理→执行键鼠动作)。
- 通用操作空间：仅凭截图 + 键鼠，无需为每个 OS/网站定制 API。
- 自我纠错：遇阻可基于推理重试/调整；卡住时把控制权交还用户。
- 基准(博客口径)：OSWorld 38.1%、WebArena 58.1%、WebVoyager 87%。
- 产品化：驱动 Operator(2025-01 研究预览，US Pro 起)；后并入 ChatGPT 的 Agent 模式。

## 原始链接
- url: https://openai.com/index/computer-using-agent/

## 一手源存档（sources/）
- [openai-computer-using-agent.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/agentic/openai-computer-using-agent.html)
