---
title: "AgentBench: Evaluating LLMs as Agents"
org: 清华大学 / 智谱AI（Tsinghua / Zhipu，与 Ohio State、UC Berkeley 合作）
country: China
date: 2023-08
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2308.03688
pdf_url: https://arxiv.org/pdf/2308.03688
github_url: https://github.com/THUDM/AgentBench
downloaded: [agentbench.pdf]
---

## 一句话定位
清华/智谱 AgentBench：首个系统评测"LLM 作为 agent"的多环境基准（8 个环境、29 个模型），为 AgentTuning 等中国 agentic 训练工作提供评测底座（GLM 团队主导）。

## 摘要（3-6 句）
AgentBench 是一个多维基准，由 8 个不同交互环境组成，用于量化评估 LLM 作为 agent 的推理与决策能力。对 29 个 API 与开源 LLM 的大规模测试显示：顶级商用 LLM（如 GPT-4）在复杂环境中具备强 agent 能力，而开源模型与其差距显著。论文揭示了模型在长期推理、决策与指令遵循上的不足，并发布统一评测工具包（HTTP 协议接入任意 LLM）。

## 关键技术细节
- 8 个交互环境：操作系统（OS）、数据库（DB，SQL）、知识图谱、数字卡牌游戏、横向思维谜题、家务（ALFWorld）、网购（WebShop）、网页浏览（Mind2Web）。
- 评测规模：29 个 API/开源 LLM（含 GPT-4、GLM 系等）。
- 评测范式：以 Chain-of-Thought (CoT) 提示为主，code-grounded / game-grounded / web-grounded 三类场景。
- 失败原因分类：Context Limit Exceeded、Invalid Format、Invalid Action、Task Limit Exceeded、Complete 等，定位长期推理/决策/指令遵循短板。
- 工具：统一评测工具包，HTTP 协议接入任意模型。
- 关系：与同组 AgentTuning（2310.12823）配套——AgentBench 提供 held-in/held-out 任务，AgentInstruct 训练数据多取自其中环境。

## 原始链接
- url: https://arxiv.org/abs/2308.03688
- pdf_url: https://arxiv.org/pdf/2308.03688
- github_url: https://github.com/THUDM/AgentBench

## 本地落盘文件
- ../../../sources/llm/2023/agentbench.pdf
