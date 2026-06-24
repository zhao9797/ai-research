---
title: "Finetuned Language Models Are Zero-Shot Learners (FLAN)"
org: Google Research
country: US
date: 2021-09
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2109.01652
pdf_url: https://arxiv.org/pdf/2109.01652
github_url: https://github.com/google-research/FLAN
downloaded: [arxiv-2109.01652.pdf]
---

## 一句话定位
Google 的 FLAN：提出"指令微调"（instruction tuning），在 60+ 个用自然语言指令模板改写的 NLP 数据集上微调 137B 模型，显著提升未见任务的 zero-shot 能力——指令微调范式的开山之作。

## 摘要（3-6 句）
FLAN 提出 instruction tuning：在一组以自然语言指令描述的数据集上微调语言模型，可大幅提升其在未见任务类型上的 zero-shot 表现。作者取一个 137B 预训练模型，在 60+ 个用指令模板改写的 NLP 数据集上微调，得到 FLAN。FLAN 在 25 个评测数据集中的 20 个上超过 175B GPT-3 的 zero-shot，在 ANLI/RTE/BoolQ/ARC/OpenbookQA/StoryCloze 上甚至大幅超过 few-shot GPT-3。消融显示微调数据集数量、模型规模、自然语言指令三者是成功关键。

## 关键技术细节
- 基座：137B 参数预训练语言模型（LaMDA-PT 系）。
- 指令微调：60+ 个 NLP 数据集，按任务簇组织，用自然语言指令模板（templates）口语化改写。
- 评估：在未见任务类型（held-out task clusters）上 zero-shot；20/25 数据集超过 GPT-3 zero-shot。
- 关键消融：①微调任务数量越多越好；②模型规模需足够大（小模型上指令微调反而有害）；③自然语言指令本身不可或缺。
- 是 instruction tuning（指令微调萌芽）的代表性工作，与 T0 并列。
- 发表于 ICLR 2022。

## 原始链接
- url: https://arxiv.org/abs/2109.01652
- pdf_url: https://arxiv.org/pdf/2109.01652
- github_url: https://github.com/google-research/FLAN

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2109.01652.pdf
