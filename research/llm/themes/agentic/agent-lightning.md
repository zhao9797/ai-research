---
title: "Agent Lightning: Train ANY AI Agents with Reinforcement Learning"
org: "Microsoft Research"
country: US
date: 2025-08
type: paper
categories: [AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2508.03680
pdf_url: https://arxiv.org/pdf/2508.03680
github_url: https://github.com/microsoft/agent-lightning
downloaded: [agent-lightning-2508.03680.pdf]
---

## 一句话定位
微软的 agent RL 训练基础设施：把"agent 执行"与"RL 训练"完全解耦，几乎零改代码即可对 LangChain/OpenAI Agents SDK/AutoGen/自研 agent 做强化学习，用分层 RL 算法 LightningRL 做信用分配。

## 摘要
Agent Lightning 是一个灵活可扩展的框架，能用强化学习训练任意 AI agent。不同于把 RL 训练与 agent 紧耦合、或依赖序列拼接+掩码的现有方法，Agent Lightning 实现 agent 执行与训练的完全解耦，可几乎零改代码地接入用各种方式开发的现有 agent(LangChain、OpenAI Agents SDK、AutoGen、从零构建等)。通过把 agent 执行建模为马尔可夫决策过程(MDP)，定义统一数据接口，并提出分层 RL 算法 LightningRL，含信用分配(credit assignment)模块，把任意 agent 产生的轨迹分解为可训练的转移(transition)，从而让 RL 能处理复杂交互逻辑(多 agent 场景、动态工作流)。系统上提出"训练-agent 解耦(Training-Agent Disaggregation)"架构，把 agent 可观测性框架引入 agent 运行时，提供标准化的 agent 微调接口。在 text-to-SQL、RAG、数学工具使用任务上展现稳定持续提升。

## 关键技术细节
- 设计目标：对"任意框架开发的 agent"做 RL，几乎零代码改动。
- 抽象：把 agent 执行建模为 MDP，定义统一数据接口；LLM 调用=可训练 transition。
- 算法 LightningRL：分层强化学习 + 信用分配(把整条轨迹/多次 LLM 调用拆成可训练样本)，支持多 agent、动态工作流。
- 系统架构：Training-Agent Disaggregation——训练侧与 agent 执行侧分离，借 agent 可观测性(tracing)采集轨迹。
- 验证任务：text-to-SQL、RAG、数学工具使用，均稳定提升。
- 出自 Microsoft Research，是 2025 "agent RL infra"方向的代表(与 verl/ROLL/AReaL 等并列)。

## 原始链接
- url: https://arxiv.org/abs/2508.03680
- pdf_url: https://arxiv.org/pdf/2508.03680
- github_url: https://github.com/microsoft/agent-lightning

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/agent-lightning-2508.03680.pdf
