---
title: "Building effective agents"
org: Anthropic
country: US
date: 2024-12
type: blog
categories: [架构, agentic训练]
url: https://www.anthropic.com/engineering/building-effective-agents
pdf_url:
github_url: https://github.com/anthropics/anthropic-cookbook
downloaded: [anthropic-building-effective-agents.html]
---

## 一句话定位
Anthropic 官方工程指南，定义了至今被广泛引用的"workflows vs agents"区分与一组可组合的 agentic 设计模式(提示链/路由/并行/编排-工人/评估-优化)，主张"简单可组合"胜过复杂框架。

## 摘要
2024-12-19，Anthropic 发布工程博客《Building effective agents》。基于与数十个跨行业团队构建 LLM agent 的经验，作者发现最成功的实现往往不用复杂框架或专用库，而是用简单、可组合的模式。文章给出关键架构区分：workflow(LLM 与工具按预定义代码路径编排) vs agent(LLM 动态自主决定流程与工具使用)；并建议从最简单方案做起、按需增加复杂度(很多场景只需单次 LLM 调用 + 检索 + in-context 示例)。随后系统介绍若干 agentic 构建块与工作流模式，以及构建自主 agent 的实践与防护。

## 关键技术细节
- 核心区分：Workflows(预定义代码路径编排 LLM/工具) vs Agents(LLM 动态主导流程与工具使用)，统称 agentic systems。
- 基础构建块：augmented LLM(配检索/工具/记忆的增强型 LLM)。
- 五大工作流模式：① Prompt chaining(提示链)；② Routing(路由分流)；③ Parallelization(并行：分段 sectioning / 投票 voting)；④ Orchestrator-workers(编排者-工人，主 LLM 动态拆解委派)；⑤ Evaluator-optimizer(评估者-优化者，生成-评判-改写循环)。
- 自主 agent：在循环中基于环境反馈自主使用工具、规划、纠错；强调要有 stopping condition、护栏、沙盒。
- 实践建议：保持简单、增加透明度(展示规划步骤)、精心设计 agent-computer interface(ACI，呼应 SWE-agent)。
- 附录给出客服、编码两个落地领域案例；配 cookbook 代码。

## 原始链接
- url: https://www.anthropic.com/engineering/building-effective-agents
- github_url: https://github.com/anthropics/anthropic-cookbook

## 一手源存档（sources/）
- [anthropic-building-effective-agents.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/agentic/anthropic-building-effective-agents.html)
