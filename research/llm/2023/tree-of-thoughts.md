---
title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
org: Princeton / Google DeepMind
country: US
date: 2023-05
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2305.10601
pdf_url: https://arxiv.org/pdf/2305.10601
github_url: https://github.com/princeton-nlp/tree-of-thought-llm
downloaded: [tree-of-thoughts.pdf]
---

## 一句话定位
ToT 把 CoT 推广为可搜索/回溯的思维树，GPT-4 在 Game of 24 从 4% 提到 74%，推理时搜索范式。

## 摘要
LLM 推理仍局限于 token 级、从左到右的决策，难做需探索/前瞻/初始决策关键的任务。提出 Tree of Thoughts(ToT) 推理框架，推广 Chain of Thought，允许在“思维(thoughts，连贯文本单元)”上探索——作为解题的中间步。ToT 让 LM 通过考虑多条推理路径、自评选择来做深思决策，并可前瞻或回溯做全局选择。在三项需非平凡规划/搜索的新任务上显著提升：Game of 24 中 GPT-4 用 CoT 仅解 4%，ToT 达 74%。

## 关键技术细节
- 框架：thought decomposition → thought generator(采样/提议候选 thought) → state evaluator(LLM 自评 value/vote) → 搜索算法(BFS/DFS) 含回溯。
- 与 CoT 区别：CoT 是单条链；ToT 是可分支、可剪枝、可回溯的树搜索。
- 任务：Game of 24、Creative Writing、Mini Crosswords。
- 结果：Game of 24 GPT-4 CoT 4% → ToT 74%。
- 意义：推理时计算(test-time search)的代表，启发后续 reasoning/search 工作。

## 原始链接
- url: https://arxiv.org/abs/2305.10601
- pdf_url: https://arxiv.org/pdf/2305.10601
- github_url: https://github.com/princeton-nlp/tree-of-thought-llm

## 一手源存档（sources/）
- tree-of-thoughts.pdf  （PDF 不入 git，走 HF bucket）
