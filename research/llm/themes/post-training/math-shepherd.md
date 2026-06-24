---
title: Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations
org: Peking University / DeepSeek-AI
country: China
date: 2023-12
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2312.08935
pdf_url: https://arxiv.org/pdf/2312.08935
downloaded: [math-shepherd.pdf]
---

## 一句话定位
Math-Shepherd：用蒙特卡洛 rollout 自动给推理步骤打"过程标签"，无需人工标注即可训练过程奖励模型 PRM，并用其做 verification + step-by-step PPO 强化。

## 摘要（3-6 句）
为避免 PRM800K 那样昂贵的人工步骤标注，Math-Shepherd 用自动化方式构造过程监督信号：对推理的每一步，用完成器（completer）从该步出发做多次蒙特卡洛采样，以"能否最终得到正确答案"的频率作为该步的软质量标签，从而自动生成过程奖励数据训练 PRM。该 PRM 既可用于 best-of-n 验证重排，也可作为逐步奖励直接做 step-by-step PPO。在 GSM8K/MATH 上，自动过程监督达到甚至超过人工标注 PRM 的效果，且可扩展。

## 关键技术细节
- 自动过程标注：对解的第 i 步，固定前缀后用 completer 采样 N 条续解，正确率作为该步质量分（hard estimation 取是否存在正确续解，soft estimation 取正确比例）。
- PRM 训练：用上述自动标签训练步骤级奖励模型，无需人工。
- 两种用法：(1) verifier——对候选解 best-of-n 重排；(2) reinforcement——把 PRM 步骤分作为奖励做 PPO（step-level reward）。
- 结果：在 Mistral-7B / DeepSeek 等上，PPO + Math-Shepherd PRM 在 GSM8K、MATH 上显著提升，逼近/超过人工 PRM。
- 意义：让过程奖励"可规模化、零人工"，是 reasoning RL（含 GRPO 路线）的重要支撑。

## 原始链接
- url: https://arxiv.org/abs/2312.08935
- pdf_url: https://arxiv.org/pdf/2312.08935

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/math-shepherd.pdf
