---
title: RLAIF vs. RLHF: Scaling RL from Human Feedback with AI Feedback
org: Google Research
country: US
date: 2023-09
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2309.00267
pdf_url: https://arxiv.org/pdf/2309.00267
downloaded: [rlaif-vs-rlhf.pdf]
---

## 一句话定位
Google 系统对比 RLAIF 与 RLHF，证明用现成 LLM 生成偏好可媲美人类标注，并提出 d-RLAIF。

## 摘要
RLAIF 用现成 LLM 生成偏好来训奖励模型，作为昂贵人类标注的替代。在摘要、有用对话、无害对话三任务上，RLAIF 与 RLHF 表现相当；即使 AI 标注器与策略同尺寸甚至同 checkpoint，RLAIF 也能超过 SFT 基线。还提出 direct-RLAIF(d-RLAIF)：跳过 RM 训练，RL 时直接从现成 LLM 取奖励，效果优于标准 RLAIF。

## 关键技术细节
- 对比：RLHF（人类偏好）vs RLAIF（AI 偏好）训练奖励模型。
- 任务：摘要、helpful dialogue、harmless dialogue。
- 结论1：RLAIF ≈ RLHF（人评 win-rate 接近）。
- 结论2：自我提升——AI 标注器与 policy 同规模/同 checkpoint 仍优于 SFT。
- d-RLAIF：RL 过程中直接用现成 LLM 打分作为奖励，免去 RM 训练，效果更佳。
- 算法：PPO；奖励来自 AI 标注偏好。

## 原始链接
- url: https://arxiv.org/abs/2309.00267
- pdf_url: https://arxiv.org/pdf/2309.00267

## 本地落盘文件
- ../../../sources/llm/2023/rlaif-vs-rlhf.pdf
