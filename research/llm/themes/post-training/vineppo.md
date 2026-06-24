---
title: "VinePPO: Unlocking RL Potential For LLM Reasoning Through Refined Credit Assignment"
org: Mila / McGill / ServiceNow
country: other
date: 2024-10
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2410.01679
pdf_url: https://arxiv.org/pdf/2410.01679
github_url: https://github.com/McGill-NLP/VinePPO
downloaded: [vineppo.pdf]
---

## 一句话定位
VinePPO：用蒙特卡洛 rollout 估计每一步的真实价值（细粒度信用分配），替代 PPO 中不准的价值网络，在数学推理上更准更省。

## 摘要（3-6 句）
论文指出 PPO 在 LLM 推理中的价值网络（critic）信用分配很差，难以区分一条长推理中哪些 token 真正重要。VinePPO 借鉴经典 vine 采样思想：在推理的中间状态从当前策略做多次蒙特卡洛 rollout，用其平均回报作为该状态的无偏价值估计，从而获得更准的优势/信用分配，完全不需要训练价值网络。在 MATH、GSM8K 上，VinePPO 用更少梯度步与更少 wall-clock 时间超过标准 PPO，并优于 RestEM、DPO 等基线。

## 关键技术细节
- 信用分配诊断：标准 PPO 的 value network 在推理任务上估计很差，导致优势噪声大。
- VinePPO 估值：对中间步状态从当前策略采样 K 条续解，回报均值即蒙特卡洛价值（无偏，无需 critic）。
- 资源权衡：用额外采样换掉价值网络训练；总体更少梯度步即收敛，wall-clock 更短、显存更省。
- 结果：MATH/GSM8K 上超过 PPO（更高准确率 + 更快收敛），且优于 RestEM、DPO 等。
- 意义：强调"准确的信用分配"是推理 RL 的关键，呼应 GRPO/RLOO 去 critic 的潮流。

## 原始链接
- url: https://arxiv.org/abs/2410.01679
- pdf_url: https://arxiv.org/pdf/2410.01679
- github_url: https://github.com/McGill-NLP/VinePPO

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/vineppo.pdf
