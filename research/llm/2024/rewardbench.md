---
title: "RewardBench: Evaluating Reward Models for Language Modeling"
org: Allen Institute for AI (AI2)
country: US
date: 2024-03
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2403.13787
pdf_url: https://arxiv.org/pdf/2403.13787
github_url: https://github.com/allenai/reward-bench
downloaded: [2403.13787.pdf]
---

## 一句话定位
RewardBench：首个系统评测 RLHF 奖励模型的基准与排行榜，覆盖 chat/推理/安全，含可验证理由的对照集。

## 摘要
奖励模型（RM）是用 RLHF 对齐模型的核心，但对其评测研究稀少。评测 RM 有助于理解对齐所用的不透明技术与其内嵌价值观。AI2 提出 RewardBench —— 一个基准数据集与代码库。其数据是覆盖 chat、推理、安全的 prompt-chosen-rejected 三元组，用于考察 RM 在挑战性、结构化、分布外查询上的表现；并构造有微妙但可验证理由（如 bug、错误事实）的对照集。排行榜评测用不同方法训练的 RM（分类器 MLE、DPO 隐式奖励等），给出关于拒答倾向、推理局限、指令遵循缺陷的诸多发现。

## 关键技术细节
- 评测范畴：Chat、Chat-Hard、Reasoning（代码/数学）、Safety。
- 数据：prompt + chosen + rejected 三元组，部分含可验证的偏好理由。
- 支持模型类型：序列分类 RM、DPO 隐式 RM（用策略与参考模型的 log-ratio 当奖励）。
- 产出：开放排行榜 + 代码 + 数据集，成为后续 RM/对齐工作的标准评测。

## 原始链接
- url: https://arxiv.org/abs/2403.13787
- pdf_url: https://arxiv.org/pdf/2403.13787
- github: https://github.com/allenai/reward-bench

## 一手源存档（sources/）
- [2403.13787.pdf](https://arxiv.org/pdf/2403.13787)  （arXiv 原文 PDF，不入 git）
