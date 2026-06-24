---
title: "Self-Rewarding Language Models"
org: Meta (FAIR) / NYU
country: US
date: 2024-01
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2401.10020
pdf_url: https://arxiv.org/pdf/2401.10020
github_url:
downloaded: [2401.10020.pdf]
---

## 一句话定位
Self-Rewarding：让模型自己用 LLM-as-a-Judge 给自己生成奖励，通过迭代 DPO 同时提升指令遵循与"打分"能力，突破固定奖励模型的人类上限。

## 摘要
作者主张要训练超人 agent，未来模型需要超人反馈作为训练信号。当前常从人类偏好训练奖励模型，但这会被人类水平瓶颈限制，且冻结的独立奖励模型不能在 LLM 训练中持续改进。本文研究 Self-Rewarding 语言模型：模型自身通过 LLM-as-a-Judge 提示为自己提供奖励。在迭代 DPO 训练中，不仅指令遵循能力提升，给自己打高质量奖励的能力也提升。对 Llama 2 70B 做三轮该方法微调，所得模型在 AlpacaEval 2.0 排行榜上超过 Claude 2、Gemini Pro、GPT-4 0613 等许多系统。这为模型在两个维度上持续自我改进打开了大门。

## 关键技术细节
- 自奖励：同一模型既生成回复，又用 LLM-as-a-Judge prompt 对回复打分（加性 5 分制）。
- 迭代 DPO：用自评构造偏好对 → DPO 训练 → 用新模型再生成与自评 → 循环（M1→M2→M3）。
- 关键现象：随迭代，judge 质量与生成质量同步提升。
- 结果：Llama 2 70B 三轮后 AlpacaEval 2.0 胜率超 Claude 2 / Gemini Pro / GPT-4 0613。

## 原始链接
- url: https://arxiv.org/abs/2401.10020
- pdf_url: https://arxiv.org/pdf/2401.10020

## 本地落盘文件
- ../../../sources/llm/2024/2401.10020.pdf
