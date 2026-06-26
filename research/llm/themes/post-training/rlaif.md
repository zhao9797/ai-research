---
title: "RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback"
org: Google Research / DeepMind
country: US
date: 2023-09
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2309.00267
pdf_url: https://arxiv.org/pdf/2309.00267
downloaded: [rlaif.pdf]
---

## 一句话定位
系统对比 RLAIF（AI 反馈）与 RLHF（人类反馈），证明用现成 LLM 生成偏好标签可达到与人类反馈相当的对齐效果，并提出 direct-RLAIF（d-RLAIF）跳过偏好模型。

## 摘要（3-6 句）
本文在摘要、有用对话、无害对话三类任务上系统对比 RLAIF 与 RLHF：用一个现成 LLM（off-the-shelf）依据指令对成对回答打偏好标签，训练 RM 再做 RL。结果显示 RLAIF 与 RLHF 在人类评测中胜率相当（摘要、对话任务上人类对两者偏好接近 50/50），且二者都显著优于 SFT 基线。论文还提出 direct-RLAIF（d-RLAIF）：直接用 LLM 打分作为 RL 奖励，省去训练独立 RM 的步骤。这为低成本、可扩展的偏好数据生成提供了实证支持。

## 关键技术细节
- AI labeler：用大 LLM（如 PaLM 2）依据详细 prompt（含 CoT、few-shot、position-bias 缓解）对成对回答给偏好。
- 三任务：摘要、helpful dialogue、harmless dialogue。
- 结果：RLAIF vs SFT 人类偏好胜率约 71%（摘要）/63%（helpful），与 RLHF 接近；harmless 任务 RLAIF 甚至更优。
- d-RLAIF：直接把 LLM 输出的偏好/分数当奖励信号做 RL，绕过 RM 蒸馏，缓解 RM 过时与过优化。
- 关键发现：即使 AI labeler 与被训练策略同规模，RLAIF 仍有效；缓解 position bias 对标签质量重要。

## 原始链接
- url: https://arxiv.org/abs/2309.00267
- pdf_url: https://arxiv.org/pdf/2309.00267

## 一手源存档（sources/）
- rlaif.pdf  （PDF 不入 git，走 HF bucket）
