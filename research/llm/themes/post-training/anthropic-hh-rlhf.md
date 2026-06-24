---
title: Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback (HH-RLHF)
org: Anthropic
country: US
date: 2022-04
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2204.05862
pdf_url: https://arxiv.org/pdf/2204.05862
github_url: https://github.com/anthropics/hh-rlhf
downloaded: [anthropic-hh-rlhf.pdf]
---

## 一句话定位
Anthropic 的 RLHF 系统性研究与 HH（helpful & harmless）偏好数据集发布，确立"有用-无害"双目标对齐范式，并提出 online iterated RLHF。

## 摘要（3-6 句）
本文用偏好建模 + RLHF 训练既有用又无害的对话助手，并研究其规模化规律。作者发现 RLHF 在大多数 NLP 评测上几乎无"对齐税"，甚至提升；helpfulness 与 harmlessness 之间存在张力但可共同优化。提出 online iterated RLHF：定期用最新策略重新收集偏好数据、重训 RM，持续迭代提升。公开了大规模 HH 人类偏好数据集（helpfulness 与 harmlessness 两类成对比较），成为社区最常用的 RLHF 训练/评测资源之一。

## 关键技术细节
- 模型规模：从 13M 到 52B 的一系列模型，研究 RM 与 RLHF 的 scaling。
- 数据：HH-RLHF 数据集，含 helpfulness（约 11.8 万对）与 harmlessness/red-team（约 4.2 万对）人类成对偏好，开源于 GitHub。
- 流程：偏好模型预训练 (PMP) → 在 HH 数据上训 RM → PPO RLHF；reward 含 KL 惩罚。
- 发现 RM 的对数损失与模型规模/数据量近似幂律；RLHF 性能随 RM 质量提升。
- online iterated RLHF：用部署中的策略采样新对比数据，循环更新 RM 与策略，是后来"on-policy 偏好数据"思路的早期实践。
- robustness 分析：RM 在分布外样本上的可靠性、校准等。

## 原始链接
- url: https://arxiv.org/abs/2204.05862
- pdf_url: https://arxiv.org/pdf/2204.05862
- github_url: https://github.com/anthropics/hh-rlhf

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/anthropic-hh-rlhf.pdf
