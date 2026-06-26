---
title: Learning to summarize from human feedback
org: OpenAI
country: US
date: 2020-09
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2009.01325
pdf_url: https://arxiv.org/pdf/2009.01325
github_url: https://github.com/openai/summarize-from-feedback
downloaded: [learning-to-summarize-from-human-feedback.pdf]
---

## 一句话定位
RLHF 在生成式摘要上的奠基性论文：用人类偏好训练奖励模型，再用 PPO 优化策略，证明 RLHF 摘要质量超过监督微调与人类参考摘要。

## 摘要（3-6 句）
作者收集大规模高质量的人类对摘要的成对偏好数据，训练一个奖励模型（RM）来预测人类更偏好的摘要，然后用强化学习（PPO）优化语言模型策略以最大化该奖励。在 Reddit TL;DR 数据集上，1.3B 与 6.7B 模型经 RLHF 训练后，其摘要被人类偏好程度显著超过 10× 规模的监督模型，甚至超过数据集中的人类参考摘要。模型还能零样本迁移到 CNN/DailyMail 新闻摘要。该工作确立了"偏好数据→奖励模型→PPO"这一现代 RLHF 的标准三段式范式。

## 关键技术细节
- 基座模型：GPT-3 风格 transformer，规模 1.3B 与 6.7B。
- 流程三段式：(1) 监督微调 SFT；(2) 用人类成对偏好训练奖励模型 RM，损失为成对 logistic（Bradley-Terry）；(3) PPO 强化学习，reward = RM 分数 − β·KL(π‖π_SFT)，KL 惩罚防止过度偏离 SFT 策略。
- 数据：约 6.4 万条人类成对偏好（TL;DR），强调标注质量与标注者校准。
- RM 与策略均从 SFT 初始化；奖励建模发现"奖励模型越大、偏好数据越多，性能越好"。
- 揭示了 reward hacking / over-optimization 现象的早期证据：过度优化 RM 会使真实质量下降（KL 与质量的权衡曲线）。

## 原始链接
- url: https://arxiv.org/abs/2009.01325
- pdf_url: https://arxiv.org/pdf/2009.01325
- github_url: https://github.com/openai/summarize-from-feedback

## 一手源存档（sources/）
- learning-to-summarize-from-human-feedback.pdf  （PDF 不入 git，走 HF bucket）
