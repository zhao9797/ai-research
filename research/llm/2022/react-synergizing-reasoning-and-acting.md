---
title: ReAct: Synergizing Reasoning and Acting in Language Models
org: Princeton & Google Research    country: US    date: 2022-10    type: paper
categories: [agentic训练, 后训练]
url: https://arxiv.org/abs/2210.03629    pdf_url: https://arxiv.org/pdf/2210.03629    github_url: https://github.com/ysymyth/ReAct
downloaded: [react.pdf]
---

## 一句话定位
让 LLM 交替生成推理轨迹（reasoning）与行动（acting），可调用外部工具/环境，是现代 LLM agent 的奠基范式之一。

## 摘要
LLM 在语言理解与交互决策上表现出色，但其推理（如 CoT）与行动（如生成行动计划）此前多被分开研究。ReAct 让 LLM 以交错方式同时生成推理轨迹与任务相关行动：推理轨迹帮助模型归纳/追踪/更新行动计划并处理异常，行动让模型与外部知识库或环境交互获取信息。在多种语言与决策任务上超越 SOTA 基线，且比纯推理或纯行动方法有更好的可解释性与可信度。在 QA（HotpotQA）与事实验证（Fever）上缓解了纯 CoT 的幻觉问题。

## 关键技术细节
- 范式：交替输出 Thought（推理）→ Action（调用工具，如 search/lookup）→ Observation（环境返回），循环直到 Finish。
- 知识密集任务（HotpotQA、FEVER）：用 Wikipedia API 作为外部工具，显著减少 CoT 的幻觉与事实错误。
- 决策任务（ALFWorld、WebShop）：ReAct 在交互环境中以稀疏示例超越模仿/RL 基线（ALFWorld 成功率绝对值 +34%，WebShop +10%）。
- 纯提示（few-shot）即可，无需微调；可与 CoT-SC 结合。
- 影响：成为 LangChain/AutoGPT 等 agent 框架与"工具调用"范式的直接思想来源。

## 原始链接
- url: https://arxiv.org/abs/2210.03629
- pdf_url: https://arxiv.org/pdf/2210.03629
- github_url: https://github.com/ysymyth/ReAct

## 本地落盘文件
- ../../../sources/llm/2022/react.pdf
