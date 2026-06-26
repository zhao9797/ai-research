---
title: "AgentBench: Evaluating LLMs as Agents"
org: "清华大学 / 智谱 AI / 俄亥俄州立 / UC Berkeley (THUDM)"
country: China
date: 2023-08
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2308.03688
pdf_url: https://arxiv.org/pdf/2308.03688
github_url: https://github.com/THUDM/AgentBench
downloaded: [agentbench-2308.03688.pdf]
---

## 一句话定位
首个系统性、多环境的 LLM-as-agent 综合评测基准：横跨 8 个交互环境，揭示顶尖闭源模型与开源模型在 agent 能力上的巨大差距。

## 摘要
AgentBench 是评估 LLM 作为 agent 的多维度基准，含 8 个不同的交互环境，覆盖操作系统、数据库、知识图谱、卡牌对战、家庭(具身)、网购、网页浏览等任务，评估 LLM 在多轮开放式生成场景中的推理与决策能力。作者测试 25+ 个商用与开源 LLM，发现顶尖商用模型(如 GPT-4)在复杂环境中表现尚可，但与开源 LLM 之间存在显著差距；并分析失败原因(长程推理、指令遵循、格式遵循等)。AgentBench 配套提供了用于评测/训练的环境与工具链。

## 关键技术细节
- 8 个交互环境：Operating System、Database、Knowledge Graph、Digital Card Game、Lateral Thinking Puzzles、House-Holding(ALFWorld 类)、Web Shopping(WebShop)、Web Browsing(Mind2Web 类)。
- 评测 25+ 模型：含 GPT-4、GPT-3.5、Claude、以及大量开源 LLM。
- 关键发现：GPT-4 显著领先；开源模型 agent 能力弱，主因长程一致性、遵循指令/动作格式、利用环境反馈能力不足。
- 与 AgentTuning/AgentInstruct 是同一团队(THUDM/智谱)的配套工作：AgentBench 评测、AgentInstruct 训练。

## 原始链接
- url: https://arxiv.org/abs/2308.03688
- pdf_url: https://arxiv.org/pdf/2308.03688
- github_url: https://github.com/THUDM/AgentBench

## 一手源存档（sources/）
- [agentbench-2308.03688.pdf](https://arxiv.org/pdf/2308.03688)  （arXiv 原文 PDF，不入 git）
