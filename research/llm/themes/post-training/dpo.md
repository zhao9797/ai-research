---
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model (DPO)"
org: Stanford
country: US
date: 2023-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2305.18290
pdf_url: https://arxiv.org/pdf/2305.18290
downloaded: [dpo.pdf]
---

## 一句话定位
DPO：把 RLHF 的"RM + PPO"两阶段重参数化为单一分类损失，直接用偏好对优化策略，无需显式奖励模型与在线 RL，是后 RLHF 时代最具影响力的偏好优化方法。

## 摘要（3-6 句）
DPO 利用 RLHF 目标（KL 约束下最大化奖励）的闭式最优解，把奖励隐式表达为策略对参考策略的对数比，从而将 Bradley-Terry 偏好似然改写成只依赖策略的简单二分类损失。这样无需训练独立奖励模型、无需采样与 PPO，即可用 (prompt, chosen, rejected) 偏好对直接微调。DPO 训练稳定、计算轻量，效果在情感、摘要、对话等任务上匹配或超过基于 PPO 的 RLHF。它开启了"离线偏好优化"大家族（IPO/KTO/ORPO/SimPO 等）。

## 关键技术细节
- 损失：L = −E[log σ(β·(logπ_θ(y_w|x)/π_ref(y_w|x) − logπ_θ(y_l|x)/π_ref(y_l|x)))]，β 控制偏离参考策略的强度。
- 隐式奖励：r(x,y) = β·log(π_θ(y|x)/π_ref(y|x)) + βZ(x)，即"语言模型本身就是奖励模型"。
- 无需：显式 RM、在线采样、PPO/critic；用静态偏好数据离线训练。
- 参考策略 π_ref 通常取 SFT 模型；β 典型 0.1~0.5。
- 局限（后续工作指出）：易过拟合偏好、可能降低被拒答案概率同时也压低被选答案概率（likelihood displacement），催生 IPO/KTO/SimPO 等改进。

## 原始链接
- url: https://arxiv.org/abs/2305.18290
- pdf_url: https://arxiv.org/pdf/2305.18290

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/dpo.pdf
