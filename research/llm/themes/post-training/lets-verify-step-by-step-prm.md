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
downloaded: [lets-verify-step-by-step-prm.pdf]
---

## 一句话定位
过程监督（Process Reward Model, PRM）奠基论文：逐步骤监督的验证器优于只看最终答案的结果监督（ORM），并发布 PRM800K 步骤级标注数据。

## 摘要（3-6 句）
作者对比过程监督（对推理每一步给反馈）与结果监督（只对最终答案对错给反馈）在数学推理上的效果，发现训练一个 PRM（过程奖励模型）来逐步判别推理步骤正确性，再用 PRM 对大量候选解做 best-of-n 重排，显著优于结果奖励模型 ORM。在 MATH 测试集上，PRM 在 1860 个测试问题上把 best-of-N 求解率提升到 78.2%。论文发布了 PRM800K——80 万条人类步骤级标注，是过程奖励研究的核心公开数据集。该工作奠定了 reasoning RL 中"过程奖励 / 步骤级验证"的方向。

## 关键技术细节
- 基座：在 GPT-4 系列基础上微调验证器；生成器采样大量候选解。
- PRM vs ORM：PRM 对每个推理步骤输出"正确/错误/中性"概率，解级分数取各步乘积或最小值；ORM 只对整解打分。
- 数据：PRM800K，约 80 万条人工步骤级标注（覆盖 MATH 训练问题的多采样解）。
- 结果：MATH 上 PRM best-of-1860 达 78.2%，显著高于 ORM 与多数投票；PRM 还更利于主动学习（选最易出错样本标注）。
- 影响：是 Math-Shepherd、Qwen PRM、o1 等过程奖励/推理 RL 路线的直接源头。

## 原始链接
- url: https://arxiv.org/abs/2305.20050
- pdf_url: https://arxiv.org/pdf/2305.20050
- github_url: https://github.com/openai/prm800k

## 一手源存档（sources/）
- lets-verify-step-by-step-prm.pdf  （PDF 不入 git，走 HF bucket）
