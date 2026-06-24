---
title: Training language models to follow instructions with human feedback (InstructGPT)
org: OpenAI
country: US
date: 2022-03
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2203.02155
pdf_url: https://arxiv.org/pdf/2203.02155
github_url: https://github.com/openai/following-instructions-human-feedback
downloaded: [instructgpt.pdf]
---

## 一句话定位
RLHF 三阶段范式（SFT → 奖励模型 → PPO）的奠基论文：1.3B 的 InstructGPT 输出比 175B GPT-3 更受人类青睐，直接催生 ChatGPT。

## 摘要
单纯把模型做大并不能让其更好地遵循用户意图（可能产生不真实、有毒、无用的输出）。本文用人类反馈微调对齐语言模型：先用标注者撰写的 + API 提交的 prompt 收集示范数据做监督微调（SFT），再收集对模型输出的排序数据训练奖励模型，最后用 RLHF（PPO）进一步微调。所得模型称为 InstructGPT。人类评测中，1.3B InstructGPT 的输出优于 175B GPT-3（参数少 100 倍）。InstructGPT 在真实性上提升、毒性下降，公共 NLP 数据集性能回退极小。

## 关键技术细节
- 三阶段 RLHF：(1) SFT——约 13k 条标注者示范 prompt；(2) 奖励模型（RM）——约 33k 条排序比较数据，6B RM；(3) RL——PPO，约 31k prompt 上优化。
- 模型规模：1.3B / 6B / 175B 三档，均基于 GPT-3。
- 算法：PPO（近端策略优化），加入对原始 SFT 模型的 KL 惩罚项防止 reward hacking；并提出 PPO-ptx（混入预训练梯度）减少公共 NLP 任务回退（"对齐税"）。
- 关键结果：1.3B InstructGPT 人类偏好胜过 175B GPT-3；真实性（TruthfulQA）提升约 2 倍；毒性（RealToxicityPrompts）下降约 25%。
- 标注团队约 40 人，强调标注者一致性与 held-out labeler 泛化。
- 影响：定义"指令遵循 + RLHF 对齐"的工业标准管线，是 ChatGPT 的直接前身。

## 原始链接
- url: https://arxiv.org/abs/2203.02155
- pdf_url: https://arxiv.org/pdf/2203.02155
- github_url: https://github.com/openai/following-instructions-human-feedback

## 本地落盘文件
- ../../../sources/llm/2022/instructgpt.pdf
