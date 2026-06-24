---
title: Let's Verify Step by Step
org: OpenAI
country: US
date: 2023-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2305.20050
pdf_url: https://arxiv.org/pdf/2305.20050
github_url: https://github.com/openai/prm800k
downloaded: [lets-verify-step-by-step.pdf]
---

## 一句话定位
OpenAI 证明过程监督(PRM)显著优于结果监督，并开源 PRM800K，奠定 process reward / o1 推理基础。

## 摘要
训可靠模型可用 outcome supervision(对最终结果反馈)或 process supervision(对每个中间推理步反馈)。本文系统比较二者，发现在高难度 MATH 数据集上 process supervision 显著优于 outcome supervision：过程监督模型解决 MATH 代表子集 78% 的题。还表明 active learning 大幅提升过程监督效率。开源 PRM800K——训练最佳奖励模型用的 80 万步级人类反馈标签全量数据集。

## 关键技术细节
- 对比：Outcome RM(ORM，仅最终对错) vs Process RM(PRM，逐步打分)。
- 数据 PRM800K：约 80 万条步级人工标注(对 GPT-4 生成的推理步逐步标 正确/错误/中性)。
- 验证方式：用 RM 给候选解打分做 best-of-N 重排序。
- 结果：PRM 在 MATH 子集达 78%（best-of-1860），显著超 ORM 与多数投票。
- active learning：提升过程监督数据效率。
- 影响：process reward 思想直接通向 OpenAI o1 的推理范式。

## 原始链接
- url: https://arxiv.org/abs/2305.20050
- pdf_url: https://arxiv.org/pdf/2305.20050
- github_url: https://github.com/openai/prm800k

## 本地落盘文件
- ../../../sources/llm/2023/lets-verify-step-by-step.pdf
