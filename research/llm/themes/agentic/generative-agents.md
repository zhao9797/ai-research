---
title: "Generative Agents: Interactive Simulacra of Human Behavior"
org: "Stanford University / Google Research / Google DeepMind"
country: US
date: 2023-04
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2304.03442
pdf_url: https://arxiv.org/pdf/2304.03442
github_url: https://github.com/joonspk-research/generative_agents
downloaded: [generative-agents-2304.03442.pdf]
---

## 一句话定位
用 LLM 构建可信的人类行为模拟体：记忆流 + 反思 + 规划三件套，让 25 个 agent 在沙盒小镇里自主生活、形成关系、协调群体活动（如自发组织情人节派对）。

## 摘要
Generative Agents 是可模拟可信人类行为的计算性 agent：它们起床、做饭、上班、形成观点、注意彼此、发起对话、回忆并反思过往以规划未来。论文提出一种 agent 架构，扩展 LLM 以自然语言存储 agent 的完整经验记录(记忆流, memory stream)，随时间把记忆合成为更高层反思(reflection)，并动态检索记忆来规划行为(planning)。在受《模拟人生》启发的沙盒环境中部署 25 个 agent，观察到个体与涌现的社会行为：仅由一个用户设定"想办情人节派对"的意图，agent 们便在两天内自主传播邀请、结识新朋友、相约赴会、协调时间到场。

## 关键技术细节
- 基座：ChatGPT/GPT-3.5（论文时期）。
- 核心架构三模块：
  - 记忆流(Memory Stream)：以自然语言记录完整经验，按"近因(recency)+重要性(importance)+相关性(relevance)"检索。
  - 反思(Reflection)：周期性把底层观察合成为更抽象的高层推断。
  - 规划(Planning)：把高层意图自上而下分解为日程与具体动作，并随交互动态修订。
- 评测：用"可信度(believability)"消融实验，证明记忆/反思/规划三者缺一不可，均显著贡献行为可信度；agent 行为优于人类众包基线。
- 涌现社会行为：信息扩散、关系记忆、群体协调（情人节派对案例）。

## 原始链接
- url: https://arxiv.org/abs/2304.03442
- pdf_url: https://arxiv.org/pdf/2304.03442
- github_url: https://github.com/joonspk-research/generative_agents

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/generative-agents-2304.03442.pdf
