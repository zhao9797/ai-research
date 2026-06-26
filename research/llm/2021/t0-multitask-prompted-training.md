---
title: "Multitask Prompted Training Enables Zero-Shot Task Generalization (T0)"
org: Hugging Face / BigScience
country: US
date: 2021-10
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2110.08207
pdf_url: https://arxiv.org/pdf/2110.08207
github_url: https://github.com/bigscience-workshop/t-zero
downloaded: [arxiv-2110.08207.pdf]
---

## 一句话定位
BigScience/Hugging Face 的 T0：用大量人工编写的提示模板（prompt）对 encoder-decoder 模型做多任务提示微调，以更小的模型超过 GPT-3 的 zero-shot，与 FLAN 并列为指令微调萌芽。

## 摘要（3-6 句）
T0 通过"多任务提示训练"（multitask prompted training）实现强 zero-shot 任务泛化：把大量监督数据集映射为多种自然语言提示（prompted form），在显式多任务混合上训练。结果模型在多个 held-out 任务上 zero-shot 超过规模大很多的 GPT-3。论文由 BigScience 协作完成，作者来自 Hugging Face、Brown、Snorkel AI 等。配套发布 PromptSource 提示模板库。

## 关键技术细节
- 基座：T5（LM-adapted T5，11B 为 T0++ 等变体）encoder-decoder 架构。
- 训练方式：把监督数据集用多个人工撰写的提示模板（prompts）改写成统一的文本到文本格式，做显式多任务训练。
- 评估：在训练时未见的任务类型上 zero-shot，超过 GPT-3（参数量小一个量级以上）。
- 配套资源：PromptSource（提示模板众包库）。
- 与 FLAN 的差异：T0 用 encoder-decoder、显式多任务混合 + 人写提示；FLAN 用 decoder-only 137B + 指令模板。
- 发表于 ICLR 2022。

## 原始链接
- url: https://arxiv.org/abs/2110.08207
- pdf_url: https://arxiv.org/pdf/2110.08207
- github_url: https://github.com/bigscience-workshop/t-zero

## 一手源存档（sources/）
- [arxiv-2110.08207.pdf](https://arxiv.org/pdf/2110.08207)  （arXiv 原文 PDF，不入 git）
