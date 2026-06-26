---
title: "OpenHands: An Open Platform for AI Software Developers as Generalist Agents"
org: OpenHands community (UIUC / CMU 等, f.k.a. OpenDevin)
country: US
date: 2024-07
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2407.16741
pdf_url: https://arxiv.org/pdf/2407.16741
github_url: https://github.com/All-Hands-AI/OpenHands
downloaded: [2407.16741.pdf]
---

## 一句话定位
OpenHands（前 OpenDevin）：开源通用软件开发 agent 平台——agent 像人类开发者一样写代码、用命令行、浏览网页，含沙箱执行与多 agent 协作。

## 摘要
软件是人类最强大的工具之一。随着 LLM 进步，能与环境交互并产生改变的 AI agent 快速发展。OpenHands 是开发强大、灵活 AI agent 的平台，agent 以类似人类开发者的方式与世界交互：写代码、操作命令行、浏览网页。论文描述该平台如何支持实现新 agent、与沙箱环境安全交互执行代码、多 agent 协调、以及纳入评测基准。基于已集成基准，对 agent 在 15 个挑战任务（含 SWE-bench、WebArena 等）上评测。以宽松 MIT 许可发布，是横跨学术与工业的社区项目（>188 贡献者、>2.1K 贡献）。

## 关键技术细节
- agent 动作空间：代码执行（IPython/Jupyter）、bash 命令、网页浏览，统一为事件流（event stream）架构。
- 沙箱：Docker 隔离的运行时（runtime），安全执行 agent 生成的代码。
- 多 agent：支持 agent 间委派与协作（delegation）。
- 评测集成：SWE-bench、WebArena、GAIA、MINT 等 15+ 基准开箱即用。
- 默认 agent：CodeActAgent（把动作统一为可执行代码）。
- 开源：MIT 许可，活跃社区。

## 原始链接
- url: https://arxiv.org/abs/2407.16741
- pdf_url: https://arxiv.org/pdf/2407.16741
- github: https://github.com/All-Hands-AI/OpenHands

## 一手源存档（sources/）
- [2407.16741.pdf](https://arxiv.org/pdf/2407.16741)  （arXiv 原文 PDF，不入 git）
