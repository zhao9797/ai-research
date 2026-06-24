---
title: "R1-Searcher: Incentivizing the Search Capability in LLMs via Reinforcement Learning"
org: "中国人民大学高瓴人工智能学院 / DataCanvas Alaya NeW"
country: CN
date: 2025-03
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2503.05592
pdf_url: https://arxiv.org/pdf/2503.05592
github_url: https://github.com/RUCAIBox/R1-Searcher
downloaded: [r1-searcher-2503.05592.pdf]
---

## 一句话定位
纯 RL（无蒸馏、无 SFT 冷启动）激发 LLM 自主调用外部检索的能力：两阶段 outcome-based RL，是与 Search-R1 同期的"RL 训练搜索 agent"代表作。

## 摘要
R1-Searcher 提出两阶段、基于结果（outcome-based）的 RL 方法，让 LLM 在推理过程中自主调用外部检索系统获取额外知识。框架完全依赖 RL，不需要过程奖励（process reward），也不需要蒸馏或 SFT 冷启动。第一阶段用"检索奖励"先让模型学会正确发起检索（不看答案对错）；第二阶段引入"答案奖励"让模型学会有效利用检索系统正确解题。实验在 HotpotQA / 2WikiMultiHopQA / Bamboogle / Musique 四个多跳问答基准上显著超过强 RAG 基线，甚至超过闭源 GPT-4o-mini。

## 关键技术细节
- 基座：Llama-3.1-8B-Instruct 与 Qwen-2.5-7B-Base（对 base 与 instruct 均有效）。
- RL 算法：基于 Reinforce++ 改造，加入 RAG-based rollout 与"检索 mask-based 损失计算"（对检索回来的文档 token 在损失中掩码，避免对外部内容算策略梯度）。
- 两阶段奖励：Stage-1 = 检索奖励 + 格式奖励（只激励发起检索，不看答案）；Stage-2 = 引入答案奖励（F1/正确性）。
- 训练数据按难度分级（按解出所需 rollout 数：easy <10、medium 10–20、difficult >20）；Stage-1 用 HotpotQA 200 + 2Wiki 150（均 medium），Stage-2 用 HotpotQA 2561 medium + 2000 difficult、2Wiki 1087 medium + 2500 difficult。
- 交互格式：`<think>...</think>`、`<answer>...</answer>`，检索用 `<|begin_of_query|>...<|end_of_query|>`，结果回填 `<|begin_of_documents|>...<|end_of_documents|>`。
- 结果（LLM-as-Judge）：Qwen-2.5-7B-Base 相比强基线 ReARTeR（GPT-4o-mini）在 HotpotQA 最高 +48.22%、2Wiki +21.72%；在训练时未见的 Bamboogle（在线搜索）上比 32B 参数的 Search-o1 高 11.4%，验证了泛化与在线搜索能力。

## 原始链接
- url: https://arxiv.org/abs/2503.05592
- pdf_url: https://arxiv.org/pdf/2503.05592
- github_url: https://github.com/RUCAIBox/R1-Searcher

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/r1-searcher-2503.05592.pdf
