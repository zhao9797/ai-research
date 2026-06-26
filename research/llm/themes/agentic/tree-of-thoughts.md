---
title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
org: "Princeton University / Google DeepMind"
country: US
date: 2023-05
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2305.10601
pdf_url: https://arxiv.org/pdf/2305.10601
github_url: https://github.com/princeton-nlp/tree-of-thought-llm
downloaded: [tree-of-thoughts-2305.10601.pdf]
---

## 一句话定位
把 CoT 从一条线推广为一棵树：LLM 生成多个中间"思考"分支并用自我评估 + 搜索(BFS/DFS)做有目的的探索与回溯，是 agent 规划/搜索的代表性 inference-time 方法。

## 摘要
Tree of Thoughts(ToT) 将语言模型推理建模为在"思考树"上的搜索：每个节点是一段连贯的中间思考(thought)，模型可生成多个候选思考、对其做自我评估(value/vote)，并用经典搜索算法(广度/深度优先)进行前瞻与回溯。相比一次性 chain-of-thought，ToT 允许探索不同推理路径、评估各选项并在必要时回退。在需要规划/搜索的任务上提升巨大：24 点游戏(Game of 24)中 GPT-4 用 CoT 仅 4% 成功，ToT 达 74%。

## 关键技术细节
- 四个可设计组件：① 思考分解(把问题拆成思考步)；② 思考生成器(采样或提议多个候选)；③ 状态评估器(LM 自评每个思考的前景，value 或多数投票 vote)；④ 搜索算法(BFS/DFS + 剪枝)。
- 基座：GPT-4。
- 结果：Game of 24 成功率 CoT 4% → ToT 74%；创意写作、5x5 填字游戏等也显著优于 CoT/CoT-SC。
- 定位：纯 inference-time 的"深思熟虑"框架，不需训练，把搜索/规划显式引入 LLM 解题。

## 原始链接
- url: https://arxiv.org/abs/2305.10601
- pdf_url: https://arxiv.org/pdf/2305.10601
- github_url: https://github.com/princeton-nlp/tree-of-thought-llm

## 一手源存档（sources/）
- [tree-of-thoughts-2305.10601.pdf](https://arxiv.org/pdf/2305.10601)  （arXiv 原文 PDF，不入 git）
