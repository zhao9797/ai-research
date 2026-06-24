---
title: "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
org: Microsoft Research
country: US
date: 2023-08
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2308.08155
pdf_url: https://arxiv.org/pdf/2308.08155
github_url: https://github.com/microsoft/autogen
downloaded: [autogen.pdf]
---

## 一句话定位
微软开源多智能体对话框架 AutoGen，可定制/可对话 agent + 人/工具混合，主流 multi-agent 框架。

## 摘要
AutoGen 是开源框架，让开发者用可相互对话的多个 agent 构建 LLM 应用完成任务。agent 可定制、可对话，可在 LLM/人类输入/工具的多种组合模式下运行；开发者可灵活定义 agent 交互行为，用自然语言或代码编排对话模式。作为通用框架支持各种复杂度与 LLM 能力的应用。实证覆盖数学、编码、QA、运筹、在线决策、娱乐等领域。

## 关键技术细节
- 核心抽象：ConversableAgent——可配置 LLM、human-in-the-loop、code executor 与工具。
- 内置：AssistantAgent、UserProxyAgent(可执行代码)；支持 group chat、hierarchical chat、joint chat 等会话拓扑。
- 编排：会话模式可用自然语言或 Python 代码定义。
- 代码执行：UserProxyAgent 自动执行 LLM 生成代码并把报错反馈回去迭代。
- 应用：数学求解、运筹、代码生成、网页决策等多 demo。
- 影响：成为最主流的开源 multi-agent 框架之一。

## 原始链接
- url: https://arxiv.org/abs/2308.08155
- pdf_url: https://arxiv.org/pdf/2308.08155
- github_url: https://github.com/microsoft/autogen

## 本地落盘文件
- ../../../sources/llm/2023/autogen.pdf
