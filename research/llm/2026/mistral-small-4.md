---
title: "Mistral Small 4（统一 Instruct + Reasoning + Devstral，MoE 119B/6.5B）"
org: Mistral AI
country: EU (France)
date: 2026-03
type: model-card
categories: [架构, 后训练, agentic训练]
url: https://huggingface.co/mistralai/Mistral-Small-4-119B-2603
downloaded: [mistral-small-4-readme.md, mistral-small-4-config.json]
---

## 一句话定位
Mistral Small 4 —— 把 **Instruct + Reasoning（原 Magistral）+ Devstral** 三个家族统一进单一混合模型，可在「即时回复」与「推理」模式间切换（2026-03 发布，初版调研窗口前漏收，增量补录）。

## 摘要
统一模型：同一权重既是通用指令模型也是推理模型，并含代码（Devstral）能力。多模态输入（图文进、文字出），原生 function calling + JSON 输出，best-in-class agentic 能力；reasoning effort 每请求可调（none/high）。相比 Mistral Small 3：延迟优化下端到端完成时间 **−40%**，吞吐优化下 **3× RPS**。Apache-2.0。

## 关键技术细节
- **架构（config.json，model_type=mistral4）**：**MoE 128 路由专家 + 1 共享，每 token 选 4**；**119B 总参 / 6.5B 激活**；hidden 4096；**36 层**；32 注意力头 / 32 KV（MHA），qk_head_dim 128（nope 64 + rope 64）；moe_intermediate 2048；上下文 **256K**；rope_theta 1e4（+ 扩展）。
- **模式**：instant ↔ reasoning 切换；reasoning_effort none/high。
- **能力**：multimodal 输入、function calling、JSON、agentic。
- 许可 Apache-2.0。

## 原始链接
- url: https://huggingface.co/mistralai/Mistral-Small-4-119B-2603

## 本地落盘文件
- ../../../sources/llm/2026/mistral-small-4-readme.md
- ../../../sources/llm/2026/mistral-small-4-config.json
