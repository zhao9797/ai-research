---
title: Self-Rewarding Language Models
org: Meta (FAIR) / NYU
country: US
date: 2024-01
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2401.10020
pdf_url: https://arxiv.org/pdf/2401.10020
downloaded: [self-rewarding-language-models.pdf]
---

## 一句话定位
Self-Rewarding LM：让同一个模型既当策略又当裁判（LLM-as-a-Judge），自己给自己生成的回答打分造偏好对，再做迭代 DPO，突破"奖励模型固定"的瓶颈。

## 摘要（3-6 句）
传统 RLHF 的奖励模型在训练后固定，能力受限于人类标注。Self-Rewarding LM 让模型用 LLM-as-a-Judge 能力（按一套加性评分准则给 0–5 分）评判自己采样的多个回答，选出最高/最低分构成偏好对，做 DPO 迭代（Iterative DPO，M1→M2→M3）。随着迭代，模型不仅指令遵循能力提升，其自我评判（奖励）能力也同步提升，形成正反馈。从 Llama-2-70B 起经 3 轮自奖励迭代，在 AlpacaEval 2.0 上超过 Claude 2、Gemini Pro、GPT-4 0613 等。

## 关键技术细节
- 单模型双角色：instruction-following（生成）+ LLM-as-a-Judge（按 5 点加性 rubric 打分）。
- 种子数据：IFT（指令微调）+ EFT（评估微调，教模型按 rubric 打分）。
- 迭代：M_t 采样 N 个回答 → 自评打分 → 取最高/最低构 (chosen, rejected) → DPO 得 M_{t+1}。
- 关键发现：迭代中"自我奖励"质量随之提升，不像固定 RM 会瓶颈化。
- 结果：Llama-2-70B 经 3 轮，AlpacaEval 2.0 LC 胜率超过多款前沿模型。

## 原始链接
- url: https://arxiv.org/abs/2401.10020
- pdf_url: https://arxiv.org/pdf/2401.10020

## 一手源存档（sources/）
- self-rewarding-language-models.pdf  （PDF 不入 git，走 HF bucket）
