---
title: Generative Agents: Interactive Simulacra of Human Behavior
org: Stanford / Google
country: US
date: 2023-04
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2304.03442
pdf_url: https://arxiv.org/pdf/2304.03442
downloaded: [generative-agents.pdf]
---

## 一句话定位
斯坦福“AI 小镇”：25 个生成式 agent 用记忆-反思-规划架构涌现可信社会行为，agent 记忆系统经典。

## 摘要
生成式 agent 是模拟可信人类行为的软件 agent：会起床、做早餐、上班，形成观点、相互注意、发起对话、回忆并反思过去以规划次日。架构扩展 LLM：用自然语言存储 agent 完整经历记忆流，随时间综合为更高层反思，并动态检索以规划行为。在 The Sims 式沙盒中放入 25 个 agent，用户可用自然语言交互。涌现可信个体与群体行为（如从“一个 agent 想办情人节派对”自发传播邀请、结识、约会、按时到场）。消融证明 observation/planning/reflection 各组件对可信度都关键。

## 关键技术细节
- 记忆流(Memory Stream)：自然语言记录全部经历，带 recency/importance/relevance 三因子检索打分。
- 反思(Reflection)：周期性把底层观察综合为高层抽象结论，存回记忆。
- 规划(Planning)：自顶向下生成日程并随事件递归细化/重规划。
- 底座：ChatGPT/GPT-3.5。
- 评测：25 agent 沙盒涌现社会行为；消融 observation/planning/reflection 均显著降低可信度。
- 影响：奠定 LLM agent 长期记忆架构范式。

## 原始链接
- url: https://arxiv.org/abs/2304.03442
- pdf_url: https://arxiv.org/pdf/2304.03442

## 本地落盘文件
- ../../../sources/llm/2023/generative-agents.pdf
