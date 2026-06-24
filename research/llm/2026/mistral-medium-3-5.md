---
title: Remote agents in Vibe. Powered by Mistral Medium 3.5.
org: Mistral AI
country: EU
date: 2026-05
type: blog
categories: [架构, 后训练, agentic训练]
url: https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/
pdf_url:
github_url:
downloaded: [mistral-medium-3-5.html]
---

## 一句话定位
Mistral AI 2026-05-22 发布的旗舰"合并模型"Mistral Medium 3.5——128B 稠密模型、256k 上下文、每请求可配置推理强度，作为 Vibe / Le Chat 的默认模型支撑长周期 agentic 编程与办公任务。

## 摘要
Mistral Medium 3.5 是 Mistral 首个"合并模型"（merged model），把指令遵循、推理与编程能力融入单一权重集。它是 128B 稠密（dense，非 MoE）模型，256k 上下文窗口，开放权重（modified MIT license），真实场景表现强、最少 4 张 GPU 即可自托管。推理强度（reasoning effort）现可按请求配置，同一模型既能快速对话又能跑复杂 agentic 流程。视觉编码器从零训练以处理可变图像尺寸与宽高比。配套发布的 Le Chat "Work mode" 与 Vibe 远程 agent 基于该模型并行调用工具直到完成多步任务。

## 关键技术细节
- 发布：2026-05-22（public preview）。EU（法国）厂商。
- 架构：128B 稠密（dense，非 MoE）模型；首个把 instruction-following + reasoning + coding 合并进单一权重的"merged model"。
- 上下文：256k token 上下文窗口。
- 许可：开放权重，modified MIT license。
- 部署：最少 4 张 GPU 可自托管；定位真实世界性能/尺寸折中。
- 推理：reasoning effort 按请求可配置（per-request）——同模型可做快速直答或长链 agentic。
- 多模态：视觉编码器从零训练（from scratch），处理可变图像尺寸/宽高比。
- 基准：SWE-Bench Verified 77.6%（领先 Devstral 2 与 Qwen3.5 397B A17B）；τ³-Telecom 91.4（agentic）。
- 产品集成：Mistral Vibe 远程 agent、Le Chat Work mode（多步研究/分析/跨工具操作，工具并行调用）。

## 原始链接
- url: https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/

## 本地落盘文件
- ../../../sources/llm/2026/mistral-medium-3-5.html
