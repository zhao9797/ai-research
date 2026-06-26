---
title: "Search-o1: Agentic Search-Enhanced Large Reasoning Models"
org: "中国人民大学 / 清华大学"
country: CN
date: 2025-01
type: paper
categories: [agentic训练, 推理]
url: https://arxiv.org/abs/2501.05366
pdf_url: https://arxiv.org/pdf/2501.05366
github_url: https://github.com/sunnynexus/Search-o1
downloaded: [search-o1-2501.05366.pdf]
---

## 一句话定位
给 o1 类大推理模型（LRM）装上"按需检索 + 文档精炼"的 agentic RAG：训练无关（inference-time）框架，是后续 Search-R1/R1-Searcher 等 RL 搜索 agent 的重要前置工作与对比基线。

## 摘要
Search-o1 针对 o1 类大推理模型（LRM）在长链推理中"知识不足→频繁出现不确定词→错误传播"的问题，提出一个增强框架：把 agentic RAG 机制与 Reason-in-Documents（文档内推理/精炼）模块嵌入推理流程，使 LRM 在遇到知识缺口时动态发起检索。由于检索文档冗长、且 LRM 长文档理解能力受限，专门设计独立于主推理链的 Reason-in-Documents 模块，先基于当前查询与已有推理对文档做深度分析、提炼出精炼信息，再注入推理链以最小化噪声、保持推理连贯。在科学/数学/代码等复杂推理任务和六个开放域 QA 基准上均表现强劲。

## 关键技术细节
- 实验主干：QwQ-32B-Preview（开源 o1 类 LRM）；属训练无关（training-free）的推理时框架，非 RL 训练方法。
- 核心两组件：(1) agentic RAG——模型在推理中主动解码搜索查询、触发检索，单次推理会话内可多次迭代检索；(2) Reason-in-Documents 模块——独立于主链，先分析冗长文档再产出精炼信息回填，解决"冗余信息"与"长文档理解受限/灾难性遗忘"两大挑战。
- 动机量化：在 GPQA diamond 上统计不确定词出现频次，直推（Direct Reasoning）下"perhaps"平均每条输出出现 >30 次；Search-o1 显著降低此类不确定词频次（如 perhaps 由 30.4 降到 15.8 等）。
- 评测覆盖：五个复杂推理域 + 六个开放域 QA 基准；论文给出效率与可扩展性的定量分析。
- 在多个后续 RL 工作（R1-Searcher、DeepResearcher 等）中作为强基线被对比。

## 原始链接
- url: https://arxiv.org/abs/2501.05366
- pdf_url: https://arxiv.org/pdf/2501.05366
- github_url: https://github.com/sunnynexus/Search-o1

## 一手源存档（sources/）
- [search-o1-2501.05366.pdf](https://arxiv.org/pdf/2501.05366)  （arXiv 原文 PDF，不入 git）
