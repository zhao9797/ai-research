---
title: Direct Preference Optimization: Your Language Model is Secretly a Reward Model
org: Stanford University
country: US
date: 2023-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2305.18290
pdf_url: https://arxiv.org/pdf/2305.18290
downloaded: [dpo.pdf]
---

## 一句话定位
斯坦福提出 DPO，把 RLHF 简化为一个分类损失，无需训练奖励模型/采样，成为 2023 后训练范式转折点。

## 摘要
DPO 给出 RLHF 中奖励模型的新参数化，使最优策略可闭式求出，从而用一个简单分类损失即可解 RLHF 问题，无需在微调中从 LM 采样、无需大量调参。DPO 稳定、高效、轻量，控制情感生成上超 PPO-RLHF，在摘要与单轮对话上匹配或超过，且实现/训练大幅简化。

## 关键技术细节
- 核心洞见：语言模型本身隐式就是奖励模型；reward 与 policy 之间存在闭式映射。
- 损失：直接在偏好对(chosen, rejected)上用 logistic/分类损失，目标是提高 chosen 相对 rejected 的对数似然比，受参考模型 KL 约束（隐含在 β 系数）。
- 不需要：独立 reward model、RL 采样、PPO、value function。
- 超参：仅 β（KL 强度）；训练稳定。
- 实验：IMDb 情感控制超 PPO；TL;DR 摘要、Anthropic-HH 单轮对话匹配/超过 RLHF。
- 影响：催生 Zephyr、Tulu-DPO 等大量后训练工作。

## 原始链接
- url: https://arxiv.org/abs/2305.18290
- pdf_url: https://arxiv.org/pdf/2305.18290

## 本地落盘文件
- ../../../sources/llm/2023/dpo.pdf
