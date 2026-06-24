---
title: LIMA: Less Is More for Alignment
org: Meta AI
country: US
date: 2023-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2305.11206
pdf_url: https://arxiv.org/pdf/2305.11206
downloaded: [lima.pdf]
---

## 一句话定位
Meta 的 LIMA：仅 1000 条精选样本 SFT(无 RLHF)即媲美 GPT-4，提出“表层对齐假说”。

## 摘要
LLM 分两阶段训练：(1)无监督预训练学通用表示；(2)大规模指令微调+RL 对齐到任务与偏好。LIMA 衡量二阶段相对重要性：在 65B LLaMa 上仅用 1000 条精选 prompt-response 做标准监督微调，不用任何 RL 或人类偏好建模。LIMA 表现极强，仅从少量样本就学会特定回复格式，并很好泛化到未见任务。受控人评中，LIMA 回复在 43% 情况下与 GPT-4 相当或更优(vs Bard 58%、vs DaVinci003 65%)。表明几乎所有知识在预训练习得，仅需少量指令数据即可对齐。

## 关键技术细节
- 数据：仅 1000 条人工精选的高质量 prompt-response(来自 StackExchange/wikiHow/Reddit + 自写)。
- 方法：标准 SFT，无 RLHF、无偏好建模。
- 底座：LLaMA 65B。
- 表层对齐假说(Superficial Alignment Hypothesis)：知识/能力来自预训练，对齐只是学习交互风格/格式。
- 评测：vs GPT-4 43% 持平或更优；vs Bard 58%；vs DaVinci003 65%。
- 启示：数据质量 >> 数量；少量高质 SFT 即可对齐。

## 原始链接
- url: https://arxiv.org/abs/2305.11206
- pdf_url: https://arxiv.org/pdf/2305.11206

## 本地落盘文件
- ../../../sources/llm/2023/lima.pdf
