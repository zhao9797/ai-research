---
title: Recipes for building an open-domain chatbot (BlenderBot)
org: Meta / Facebook AI Research (FAIR)
country: US
date: 2020-04
type: paper
categories: [后训练, 预训练数据, 架构]
url: https://arxiv.org/abs/2004.13637
pdf_url: https://arxiv.org/pdf/2004.13637
github_url: https://github.com/facebookresearch/ParlAI
downloaded: [arxiv-2004.13637.pdf]
---

## 一句话定位
FAIR 的 BlenderBot：用最高 94 亿参数的对话模型 + 在众包对话数据上微调以融合“个性、知识、共情”技能，并强调解码策略对对话质量的关键作用，是开放域对话大模型的代表作（同期对标 Google Meena）。

## 摘要（3-6 句）
论文给出构建开放域聊天机器人的“配方”：大规模预训练 + 在精心设计的对话技能数据集上微调 + 合适的生成解码策略。模型在 Reddit 大规模对话上预训练，再在 Blended Skill Talk（融合个性 PersonaChat、知识 Wizard of Wikipedia、共情 Empathetic Dialogues）上微调。人类评测中 BlenderBot 在吸引力与人性化上显著优于 Meena。论文同时分析了重复、知识幻觉等失败模式。

## 关键技术细节
- 模型规模：90M / 2.7B / 9.4B 参数；架构含标准 Transformer 生成模型、retrieve-and-refine、以及检索式模型三类。
- 预训练数据：约 15 亿条 Reddit 评论对话（pushshift.io）。
- 微调数据：Blended Skill Talk（BST），融合 PersonaChat（个性）、Wizard of Wikipedia（知识）、Empathetic Dialogues（共情）。
- 解码：强调 beam search 长度约束 + 子序列屏蔽来避免过短/重复回复，对最终质量影响巨大。
- 评测：ACUTE-Eval 人类对比，2.7B/9.4B 模型在 engagingness 与 humanness 上胜过 Meena。
- 已知失败：知识幻觉、矛盾、重复、深度记忆缺失。

## 原始链接
- url: https://arxiv.org/abs/2004.13637
- pdf_url: https://arxiv.org/pdf/2004.13637
- github_url: https://github.com/facebookresearch/ParlAI

## 一手源存档（sources/）
- [arxiv-2004.13637.pdf](https://arxiv.org/pdf/2004.13637)  （arXiv 原文 PDF，不入 git）
