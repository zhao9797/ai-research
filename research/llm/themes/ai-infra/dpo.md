---
title: Direct Preference Optimization: Your Language Model is Secretly a Reward Model
org: Stanford
country: US
date: 2023-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2305.18290
pdf_url: https://arxiv.org/pdf/2305.18290
downloaded: [dpo-2305.18290.pdf]
---

## 一句话定位
把 RLHF 的「训奖励模型 + PPO」两阶段简化为单一分类损失，直接在偏好对上优化策略，无需采样/奖励模型，是 RLHF 之外最主流的对齐方法。

## 摘要（3-6 句）
DPO 证明 RLHF 的最优策略与奖励模型存在闭式映射，从而把约束奖励最大化问题重参数化为对策略的简单二分类（log-sigmoid）损失，直接用偏好数据训练，无需显式奖励模型、无需 RL 采样/调参。它稳定、轻量、计算省，在情感控制、摘要、单轮对话上匹配或超过 PPO-RLHF。DPO 引发了一大类「直接偏好优化」变体（IPO、KTO、ORPO、SimPO 等），是后训练对齐的事实标准之一。

## 关键技术细节
- 重参数化：r(x,y) = β·log(π_θ(y|x)/π_ref(y|x)) + const，代入 Bradley-Terry 偏好得到分类损失。
- 训练：仅需偏好对 (chosen, rejected) + 参考模型 π_ref；无奖励模型、无 on-policy 采样。
- 稳定且省算力，匹配/超过 PPO-RLHF；催生 IPO/KTO/ORPO/SimPO 等变体。
- β 控制与参考策略的偏离强度。

## 原始链接
- url: https://arxiv.org/abs/2305.18290
- pdf_url: https://arxiv.org/pdf/2305.18290

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/dpo-2305.18290.pdf
