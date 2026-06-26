---
title: "Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning"
org: "UIUC / 马萨诸塞大学 Amherst / Google 等"
country: US
date: 2025-03
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2503.09516
pdf_url: https://arxiv.org/pdf/2503.09516
github_url: https://github.com/PeterGriffinJin/Search-R1
downloaded: [search-r1-2503.09516.pdf]
---

## 一句话定位
把 R1 式 RL 推到"边推理边搜索"：用结果奖励 + 检索 token 掩码稳定训练，让 LLM 在推理链中自主发起多轮搜索查询，是 2025 "agentic RL + 工具"浪潮的代表作之一。

## 摘要
Search-R1 把推理框架的强化学习扩展到搜索引擎使用：LLM 在逐步推理中自主生成(可多个)搜索查询并实时检索。它用多轮搜索交互优化 LLM 推理轨迹，采用"检索 token 掩码(retrieved token masking)"实现稳定的 RL 训练，并用简单的基于结果(outcome-based)的奖励函数。在七个问答数据集上，相比各种 RAG 基线(相同设置)，Search-R1 使 Qwen2.5-7B 提升 41%、Qwen2.5-3B 提升 20%。论文还给出 RL 优化方法、LLM 选择、回复长度动态的经验洞见。

## 关键技术细节
- 基座：Qwen2.5-3B / 7B(base 与 instruct)。
- RL 算法：支持 PPO 与 GRPO；奖励为简单的 outcome-based(答案是否正确)。
- 关键技巧 retrieved token masking：对检索回来的文档 token 在损失中做掩码，避免对外部内容计算策略梯度，稳定训练。
- 交互格式：推理链中以 <search>query</search> 触发检索，<information>...</information> 回填结果，多轮交错。
- 结果：7 个 QA 数据集上较 RAG 基线 +41%(7B) / +20%(3B)；分析了 response length 动态(随训练增长)等。
- 与同期 R1-Searcher、ReSearch、DeepResearcher 等同属"RL 训练搜索 agent"方向。

## 原始链接
- url: https://arxiv.org/abs/2503.09516
- pdf_url: https://arxiv.org/pdf/2503.09516
- github_url: https://github.com/PeterGriffinJin/Search-R1

## 一手源存档（sources/）
- [search-r1-2503.09516.pdf](https://arxiv.org/pdf/2503.09516)  （arXiv 原文 PDF，不入 git）
