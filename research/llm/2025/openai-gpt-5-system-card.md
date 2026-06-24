---
title: OpenAI GPT-5 System Card
org: OpenAI
country: US
date: 2025-08
type: system-card
categories: [后训练, agentic训练, AI infra]
url: https://openai.com/index/gpt-5-system-card/
pdf_url: https://cdn.openai.com/gpt-5-system-card.pdf
github_url:
downloaded: [files/openai-gpt-5-system-card.pdf]
---

## 一句话定位
OpenAI 2025-08-07 发布的 GPT-5 官方 system card（60 页），GPT-5 是一个统一的"router + 推理/非推理双子模型"系统，可按需在快速回答与深度思考之间自动路由。

## 摘要
GPT-5 不是单一模型，而是一个系统：一个高效快速回答的主模型、一个面向难题的深度推理模型（GPT-5 thinking）、以及一个实时路由器（real-time router）决定调用哪条路径；并提供 gpt-5-main / gpt-5-thinking 及 mini/nano 变体。System card 重点是安全：引入"safe completions"训练范式（以输出安全为目标而非简单拒答）、欺骗/谄媚（sycophancy）缓解、Preparedness Framework 评估（Biological/Chemical 维度按 High 能力处理并启用对应防护）。不披露架构参数。

## 关键技术细节（带数字）
- 系统组成：gpt-5-main（快速）+ gpt-5-thinking（深推理）+ real-time router；含 mini/nano 小型变体与 thinking-mini。
- 训练对齐：新"safe completions"安全训练范式（最大化有用性同时约束输出安全），相较纯拒答策略。
- 安全评估：依 Preparedness Framework；在 Biological and Chemical 领域按 "High capability" 谨慎处理并部署相应缓解。
- 缓解项：减少幻觉、减少欺骗/不诚实（deception）、降低 sycophancy；含 agentic/工具使用红队。
- 文档 60 页，不含总参/层数/MoE/训练 token 等架构数字。
- 发布日期：2025-08-07。

## 原始链接
- 官方页面：https://openai.com/index/gpt-5-system-card/
- 官方 PDF：https://cdn.openai.com/gpt-5-system-card.pdf

## 本地落盘文件
- ../../../sources/llm/2025/openai-gpt-5-system-card.pdf
