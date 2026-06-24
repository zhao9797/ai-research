---
title: "OpenHands: An Open Platform for AI Software Developers as Generalist Agents"
org: "All Hands AI / UIUC / CMU / 等(原 OpenDevin 社区)"
country: US
date: 2024-07
type: paper
categories: [架构, AI infra, agentic训练]
url: https://arxiv.org/abs/2407.16741
pdf_url: https://arxiv.org/pdf/2407.16741
github_url: https://github.com/All-Hands-AI/OpenHands
downloaded: [openhands-2407.16741.pdf]
---

## 一句话定位
开源通用软件开发 agent 平台(原 OpenDevin)：提供代码执行沙盒、浏览器、命令行等动作空间与多 agent 协作框架，是社区最广泛使用的 coding/computer-use agent 基础设施。

## 摘要
OpenHands(原名 OpenDevin) 是一个用于开发能像人类开发者一样行动的通用 AI agent 的开放平台：编写代码、使用命令行、浏览网页。平台提供一套机制实现 agent 与环境交互——agent 通过统一动作空间(执行任意代码、跑 shell 命令、浏览网页)与一个安全的沙盒环境交互；并支持 agent 间协调、可扩展的评测框架(集成 SWE-bench、WebArena 等 15+ 基准、近 2000 个任务)。论文给出社区贡献的多种 agent 实现与评测结果，是开源 agent 生态的核心基础设施。

## 关键技术细节
- 动作空间：可执行代码(Python，受 CodeAct 启发)、bash 命令、浏览器操作，统一抽象；配 Docker 安全沙盒(runtime)。
- 架构：事件流(event stream) 架构记录 agent 的动作与观察；agent hub 支持插拔多种 agent；支持多 agent 委派/协作(delegation)。
- 评测集成：内置 15+ 基准、近 2000 测试任务，含 SWE-bench、WebArena、GAIA、HumanEvalFix、MINT 等。
- 开源社区：原 OpenDevin，160+ 贡献者；是 SWE-bench 榜单上众多开源方案的载体。
- 定位：既是 agent 框架，也是 agent 评测/训练的基础设施(infra)。

## 原始链接
- url: https://arxiv.org/abs/2407.16741
- pdf_url: https://arxiv.org/pdf/2407.16741
- github_url: https://github.com/All-Hands-AI/OpenHands

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/openhands-2407.16741.pdf
