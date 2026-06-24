---
title: Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback
org: Anthropic    country: US    date: 2022-04    type: paper
categories: [后训练]
url: https://arxiv.org/abs/2204.05862    pdf_url: https://arxiv.org/pdf/2204.05862    github_url: https://github.com/anthropics/hh-rlhf
downloaded: [anthropic-hh-rlhf.pdf]
---

## 一句话定位
Anthropic 的 HH-RLHF 奠基论文：用偏好建模 + RLHF 训练"有用且无害"助手，提出在线迭代训练与 reward–√KL 线性关系。

## 摘要
应用偏好建模与 RLHF 微调语言模型，使其成为有用（helpful）且无害（harmless）的助手。发现这种对齐训练几乎在所有 NLP 评测上都提升性能，且与专门技能训练（如 Python 编码、摘要）完全兼容。探索"在线迭代"训练模式：偏好模型与 RL 策略每周用新人类反馈更新。研究 RLHF 鲁棒性，发现 RL 奖励与策略相对初始化的 KL 散度平方根呈大致线性关系。还做了校准、竞争目标、OOD 检测等分析，并与人类写手对比。

## 关键技术细节
- 数据：公开 HH-RLHF 偏好数据集（helpfulness + harmlessness 两类人类比较数据，数十万对）。
- 流程：预训练 LM → 偏好模型预训练（PMP）→ 偏好模型微调 → RLHF（PPO）。
- 关键发现：reward 与 sqrt(D_KL(policy‖init)) 近似线性，可用于预测/控制对齐强度。
- "alignment bonus"：对齐训练在多数 NLP 基准上不仅无税、反而提升（与 InstructGPT 的"对齐税"观察对照）。
- 在线迭代：每周收集新人类反馈、滚动更新 PM 与策略。
- 模型规模覆盖到 52B；助手既有用又无害，且与编码/摘要等技能兼容。

## 原始链接
- url: https://arxiv.org/abs/2204.05862
- pdf_url: https://arxiv.org/pdf/2204.05862
- github_url: https://github.com/anthropics/hh-rlhf

## 本地落盘文件
- ../../../sources/llm/2022/anthropic-hh-rlhf.pdf
