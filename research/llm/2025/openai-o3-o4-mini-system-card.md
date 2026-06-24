---
title: OpenAI o3 and o4-mini System Card
org: OpenAI
country: US
date: 2025-04
type: system-card
categories: [后训练, agentic训练, AI infra]
url: https://openai.com/index/o3-o4-mini-system-card/
pdf_url: https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf
github_url:
downloaded: [files/openai-o3-o4-mini-system-card.pdf]
---

## 一句话定位
OpenAI 2025-04-16 发布的 o 系列推理模型 o3 与 o4-mini 的官方 system card，首次让推理模型在思维链中"agentically"调用 ChatGPT 全部工具（浏览、Python、图像分析与生成、文件检索、记忆）。

## 摘要
o3 是 OpenAI 当时最强的推理模型，o4-mini 为小而快、高性价比的推理模型。两者均经大规模 RL 训练，在数学/编码/科学上达到 SOTA，并能在推理过程中自主组合调用工具。System card 重点是安全评估（Preparedness Framework）：生物化学、网络安全、AI 自我改进三类前沿风险均评为未达 "High"。文档不披露参数等架构细节，但披露了能力/安全/对抗测试方法与红队结果。

## 关键技术细节（带数字）
- 训练范式：大规模强化学习（RL）训练推理；o 系列"think for longer before responding"。
- agentic 工具：模型可在单条思维链中组合调用 web browsing、Python、图像/文件分析、图像生成、canvas、自动化、文件检索、记忆。
- 安全框架：依据 Preparedness Framework 评估，o3/o4-mini 在 Biological/Chemical、Cybersecurity、AI Self-improvement 三类追踪风险均未达 High 阈值。
- 评估：disallowed content、jailbreak（StrongReject 等）、hallucination（PersonQA/SimpleQA）、bias、instruction hierarchy、agentic 红队等。
- 文档不含总参/层数/MoE 等架构参数（OpenAI 闭源策略）。

## 原始链接
- 官方页面：https://openai.com/index/o3-o4-mini-system-card/
- 官方 PDF：https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf
- 发布博客：https://openai.com/index/introducing-o3-and-o4-mini/

## 本地落盘文件
- ../../../sources/llm/2025/openai-o3-o4-mini-system-card.pdf
