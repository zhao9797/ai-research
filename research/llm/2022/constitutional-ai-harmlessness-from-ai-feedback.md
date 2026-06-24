---
title: Constitutional AI: Harmlessness from AI Feedback
org: Anthropic    country: US    date: 2022-12    type: paper
categories: [后训练]
url: https://arxiv.org/abs/2212.08073    pdf_url: https://arxiv.org/pdf/2212.08073    github_url:
downloaded: [constitutional-ai.pdf]
---

## 一句话定位
提出 Constitutional AI（CAI）与 RLAIF：仅用一份"宪法"原则、几乎不用人类有害性标注，让 AI 自我批判修订并用 AI 偏好做 RL，训练出无害但不回避的助手。

## 摘要
随着 AI 能力增强，希望用 AI 来监督其他 AI。本文实验通过自我改进训练无害助手，不使用任何标注有害输出的人类标签——唯一人类监督是一份规则/原则清单（故称 Constitutional AI）。流程含监督学习与强化学习两阶段：监督阶段从初始模型采样、生成自我批判与修订、用修订后回复微调原模型；RL 阶段从微调模型采样、用一个模型评判哪条更好、据此 AI 偏好数据训练偏好模型，再用其作奖励信号做 RL（即 RLAIF——RL from AI Feedback）。结果训练出无害但不回避的助手，会就有害请求解释反对理由而非简单拒答。

## 关键技术细节
- 两阶段：(1) SL-CAI——few-shot 让模型按宪法原则对自己的有害回复做 self-critique → revise，再在修订回复上 SFT；(2) RL-CAI（RLAIF）——用 AI 按宪法对比一对回复给偏好，训练偏好模型(PM)，再用 PM 作奖励做 PPO。
- "宪法"：约十余条自然语言原则（无害、避免歧视、不协助危险行为等），是唯一的人类监督输入。
- 与传统 RLHF 对比：harmlessness 偏好数据由 AI 生成而非人工标注，大幅降低人工成本，并提升可扩展监督。
- 结果：在 helpfulness 不降的前提下显著提升 harmlessness，且模型"非回避"——会解释拒绝理由。
- 加入 CoT 推理可进一步提升评判与无害性。
- 影响：RLAIF 成为可扩展对齐的代表方法，后续广泛影响开源对齐（如各类 AI feedback 数据）。

## 原始链接
- url: https://arxiv.org/abs/2212.08073
- pdf_url: https://arxiv.org/pdf/2212.08073

## 本地落盘文件
- ../../../sources/llm/2022/constitutional-ai.pdf
