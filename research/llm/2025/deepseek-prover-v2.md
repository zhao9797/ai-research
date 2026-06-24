---
title: DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition
org: DeepSeek
country: China
date: 2025-04
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2504.21801
pdf_url: https://arxiv.org/pdf/2504.21801
github_url: https://github.com/deepseek-ai/DeepSeek-Prover-V2
downloaded: [deepseek-prover-v2.pdf]
---

## 一句话定位
面向 Lean 4 形式化定理证明的 671B 模型，用 DeepSeek-V3 做子目标分解递归证明 + RL，MiniF2F-test 达 88.9%。

## 摘要
DeepSeek-Prover-V2 通过递归定理证明 pipeline 收集冷启动数据：先用 DeepSeek-V3 把复杂问题分解为子目标，已解子目标的证明合成为 CoT，结合 V3 的逐步推理，构造 RL 冷启动，把非形式化与形式化数学推理统一到一个模型。DeepSeek-Prover-V2-671B 在 MiniF2F-test 达 88.9% pass ratio，PutnamBench 658 题解出 49 题。

## 关键技术细节
- 任务：Lean 4 形式化定理证明（neural theorem proving）。
- 数据合成：DeepSeek-V3 递归子目标分解 → 已证子目标合成 CoT → RL 冷启动。
- 训练：cold-start SFT + 强化学习（subgoal decomposition reward）。
- 规模：DeepSeek-Prover-V2-671B（基于 V3 架构）+ 7B 版本。
- 成绩：MiniF2F-test 88.9%；PutnamBench 49/658。
- 统一：informal + formal 数学推理融合于单一模型。

## 原始链接
- url: https://arxiv.org/abs/2504.21801
- pdf_url: https://arxiv.org/pdf/2504.21801
- github_url: https://github.com/deepseek-ai/DeepSeek-Prover-V2

## 本地落盘文件
- ../../../sources/llm/2025/deepseek-prover-v2.pdf
