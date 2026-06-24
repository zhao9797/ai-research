---
title: "UltraFeedback: Boosting Language Models with Scaled AI Feedback"
org: Tsinghua / OpenBMB
country: China
date: 2023-10
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2310.01377
pdf_url: https://arxiv.org/pdf/2310.01377
github_url: https://github.com/OpenBMB/UltraFeedback
downloaded: [ultrafeedback.pdf]
---

## 一句话定位
UltraFeedback：大规模、细粒度 GPT-4 AI 反馈偏好数据集，成为社区 DPO/RM 训练（Zephyr、Tulu 等）的事实标准数据源。

## 摘要（3-6 句）
UltraFeedback 收集约 6.4 万条指令、用多个不同模型生成约 25.6 万条回答，并用 GPT-4 从 instruction-following、truthfulness、honesty、helpfulness 四个维度给出细粒度评分与文字评语，构成高质量 AI 偏好数据集。基于它训练的奖励模型 UltraRM 与对话模型 UltraLM 在多项基准上领先。该数据集是 Zephyr-DPO、Tulu 2/3、Notus 等众多开源对齐模型的核心偏好数据来源，极大降低了高质量偏好数据的获取门槛。

## 关键技术细节
- 规模：约 6.4 万指令（聚合多个指令集），每条采样 4 个不同模型的回答，合计约 25.6 万 (instruction, completion) 与对应评分。
- 评分：GPT-4 四维度打分（instruction following / truthfulness / honesty / helpfulness）+ 总体评分 + 文字 critique，可转成成对偏好。
- 多样性：刻意用不同能力/家族模型（含较弱模型）生成回答，扩大偏好对比信号。
- 衍生：UltraRM（奖励模型）、UltraLM（SFT/对齐模型）；被 HuggingFace H4 用于 Zephyr 的 DPO。
- 影响：使"GPT-4 as judge 批量造偏好数据 → DPO"成为开源对齐主流配方。

## 原始链接
- url: https://arxiv.org/abs/2310.01377
- pdf_url: https://arxiv.org/pdf/2310.01377
- github_url: https://github.com/OpenBMB/UltraFeedback

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/ultrafeedback.pdf
