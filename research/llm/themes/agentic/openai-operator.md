---
title: "Introducing Operator"
org: OpenAI
country: US
date: 2025-01
type: blog
categories: [agentic训练]
url: https://openai.com/index/introducing-operator/
pdf_url:
github_url:
downloaded: [openai-introducing-operator.html]
---

## 一句话定位
OpenAI 首个面向消费者的浏览器 agent 产品：用自带浏览器替用户在网上做事(填表、下单、订位)，由 CUA 模型驱动，2025-01 以研究预览面向美国 Pro 用户发布，后并入 ChatGPT Agent 模式。

## 摘要
2025-01-23，OpenAI 发布 Operator——一个能上网替用户执行任务的 agent。它用自己的浏览器查看网页，用户可通过打字/点击/滚动与之交互。作为研究预览，从美国 Pro 用户小规模起步(operator.chatgpt.com)，计划逐步扩展到 Plus/Team/Enterprise 并集成进 ChatGPT。可让 Operator 处理重复性浏览器任务(填表、订杂货、做备忘)。驱动它的是 Computer-Using Agent(CUA) 模型——把 GPT-4o 视觉与 RL 习得的高级推理结合，与 GUI 交互；Operator 通过截图"看"浏览器、用鼠标键盘"操作"，无需自定义 API；遇错可自我纠错，卡住时把控制权交还用户。

## 关键技术细节
- 模型：CUA(GPT-4o 视觉 + 强化学习推理)。
- 形态：自带云端浏览器的 agent，通过截图感知 + 键鼠操作真实网站。
- 发布：2025-01-23 研究预览，先开放美国 ChatGPT Pro。
- 演进：2025-07-17 起 Operator 完全集成进 ChatGPT(选择 Agent 模式)，独立站点 operator.chatgpt.com 逐步下线。
- 安全：用户监督、take-over(交还控制)、敏感操作需确认等护栏。

## 原始链接
- url: https://openai.com/index/introducing-operator/

## 一手源存档（sources/）
- [openai-introducing-operator.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/agentic/openai-introducing-operator.html)
