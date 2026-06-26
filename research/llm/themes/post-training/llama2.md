---
title: "Llama 2: Open Foundation and Fine-Tuned Chat Models"
org: Meta
country: US
date: 2023-07
type: paper
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2307.09288
pdf_url: https://arxiv.org/pdf/2307.09288
downloaded: [llama2.pdf]
---

## 一句话定位
Llama 2 / Llama 2-Chat：开源代表性的完整 RLHF 后训练配方，提出"双奖励模型（有用/安全）+ 拒绝采样 + PPO"与 Ghost Attention（GAtt）多轮一致性技巧。

## 摘要（3-6 句）
Llama 2 系列含 7B/13B/70B 预训练模型与对话微调版 Llama 2-Chat。后训练采用 SFT + 迭代 RLHF：先做高质量 SFT，再训练两个独立奖励模型（helpfulness RM 与 safety RM），通过多轮迭代——先用 rejection sampling（best-of-n）收集高奖励样本微调，后期叠加 PPO——逐步对齐。论文详细公开了偏好数据规模、RM 训练、RLHF 迭代轮次（RLHF-v1…v5）、安全对齐（safety RLHF + context distillation）与多轮 Ghost Attention 技巧，是工业级开源 RLHF 的最详尽报告之一。

## 关键技术细节
- 预训练：2T tokens，上下文 4K，70B 用 GQA（grouped-query attention）。
- 偏好数据：Meta 自采约 140 万条人类成对偏好（含 helpfulness 与 safety 两类），加开源数据。
- 双 RM：分别优化 helpfulness 与 safety，避免单一 RM 的目标冲突；RM 用 margin loss（偏好程度分级）。
- RLHF 迭代：rejection sampling fine-tuning（从 N 个采样取最高 RM 分）为主，后期加 PPO；共 5 轮迭代（v1–v5）。
- 安全：safety SFT、safety RLHF、safety context distillation；红队测试。
- Ghost Attention (GAtt)：在多轮对话中合成系统指令以保持长程一致性。

## 原始链接
- url: https://arxiv.org/abs/2307.09288
- pdf_url: https://arxiv.org/pdf/2307.09288

## 一手源存档（sources/）
- llama2.pdf  （PDF 不入 git，走 HF bucket）
