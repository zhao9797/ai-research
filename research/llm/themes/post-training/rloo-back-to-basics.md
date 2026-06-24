---
title: "Back to Basics: Revisiting REINFORCE Style Optimization for Learning from Human Feedback in LLMs (RLOO)"
org: Cohere / Cohere For AI
country: EU
date: 2024-02
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2402.14740
pdf_url: https://arxiv.org/pdf/2402.14740
downloaded: [rloo-back-to-basics.pdf]
---

## 一句话定位
RLOO（REINFORCE Leave-One-Out）：论证在 LLM RLHF 中 PPO 的诸多复杂组件（critic、clipping、GAE）多余，回归更简单的 REINFORCE + leave-one-out 基线即可更优、更省内存。

## 摘要（3-6 句）
作者指出 PPO 是为高方差、部分可观测、需多步信用分配的 RL 场景设计的，而 LLM RLHF 实为单步（整段生成给一个奖励）、初始化良好的低方差设定，PPO 的 critic/裁剪等组件并非必要。提出 RLOO：对每个 prompt 采样 k 个回答，用其余 k−1 个样本的平均奖励作为 leave-one-out 基线来估计优势，做 REINFORCE 更新。RLOO 比 PPO 更简单、显存更省、对噪声/KL 更鲁棒，且在多项 RLHF 任务上效果更好。这是"是否需要 PPO 全套"讨论中的关键工作，也是 GRPO 等无 critic 方法的近亲。

## 关键技术细节
- 设定洞察：RLHF 是单动作（full-completion）bandit 式问题，奖励仅在序列末端，PPO 的多步信用分配冗余。
- RLOO 基线：对 k 个采样，第 i 个样本的基线 = 其余 (k−1) 个奖励的均值，无偏、无需 critic 网络。
- 更省内存：去掉价值网络，显著降低 RLHF 显存与实现复杂度。
- 鲁棒：对 KL 惩罚系数与奖励噪声比 PPO 更稳定。
- 结果：在 TL;DR、HH 等任务上胜过 PPO、RAFT、vanilla REINFORCE、DPO 等。

## 原始链接
- url: https://arxiv.org/abs/2402.14740
- pdf_url: https://arxiv.org/pdf/2402.14740

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/rloo-back-to-basics.pdf
