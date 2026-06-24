---
title: "Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks"
org: "Microsoft Research (AutoGen team)"
country: US
date: 2024-11
type: paper
categories: [架构, agentic训练]
url: https://arxiv.org/abs/2411.04468
pdf_url: https://arxiv.org/pdf/2411.04468
github_url: https://github.com/microsoft/autogen
downloaded: [magentic-one-2411.04468.pdf]
---

## 一句话定位
微软的开源通用多 agent 系统：以 Orchestrator 主控 agent 做规划/进度跟踪/失败重规划，调度浏览器、文件、编码等专才 agent，在 GAIA/WebArena/AssistantBench 上达竞争力表现。

## 摘要
现代 AI agent 有望增强生产力，但要实现愿景，agent 须能有效规划、执行多步推理与动作、响应新观察、从错误中恢复，从而完成各类复杂任务。Magentic-One 是一个高性能开源 agentic 系统。它采用多 agent 架构：一个主控 agent(Orchestrator) 负责规划、跟踪进度、并在出错时重新规划以恢复；执行过程中 Orchestrator 指挥其他专才 agent(操作网页浏览器、导航文件、写/运行代码等)按需完成子任务。Magentic-One 在 GAIA、AssistantBench、WebArena 等多个具有挑战性的 agentic 基准上取得有竞争力的统计表现，无需针对任务做修改。

## 关键技术细节
- 架构：Orchestrator(主控/规划/重规划) + 专才 agent(WebSurfer 浏览器、FileSurfer 文件、Coder 写代码、ComputerTerminal 执行)。
- 双循环：外层 task ledger(任务事实/计划) + 内层 progress ledger(进度跟踪)，出错时回到外层重规划。
- 模块化、模型无关：底层 LLM 可替换(默认 GPT-4o 等)。
- 评测：GAIA、AssistantBench、WebArena 上有竞争力。
- 基于微软 AutoGen 框架开源；是多 agent 编排范式的代表。

## 原始链接
- url: https://arxiv.org/abs/2411.04468
- pdf_url: https://arxiv.org/pdf/2411.04468
- github_url: https://github.com/microsoft/autogen

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/magentic-one-2411.04468.pdf
