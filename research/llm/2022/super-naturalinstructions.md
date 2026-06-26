---
title: "Super-NaturalInstructions: Generalization via Declarative Instructions on 1600+ NLP Tasks"
org: AllenAI / Univ. Washington 等 (Tk-Instruct)
country: US
date: 2022-04
type: paper
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2204.07705
pdf_url: https://arxiv.org/pdf/2204.07705
github_url: https://github.com/allenai/natural-instructions
downloaded: [super-naturalinstructions.pdf]
---

## 一句话定位
1616 个带专家指令的 NLP 任务大基准，用于严格评测指令泛化；并训练出 Tk-Instruct，小模型靠指令泛化超越大模型。

## 摘要
NLP 模型在给定任务指令时对未见任务的泛化能力如何？为回答这一问题，构建 Super-NaturalInstructions：1,616 个多样 NLP 任务及其专家撰写指令的基准，覆盖 76 种任务类型（分类、抽取、填充、序列标注、改写、文本生成等）。这一大规模任务集合支持在指令下严格评测跨任务泛化（在子集上训练、在剩余未见任务上评测）。基于此训练 Tk-Instruct（在 in-context 指令——任务定义或 k-shot 示例——下运行），实验显示 Tk-Instruct 超越现有指令微调模型。

## 关键技术细节
- 基准：1,616 个任务，76 种任务类型，55 种语言；每任务含专家写的"task definition" + 正负示例。
- Tk-Instruct：基于 T5（11B）等，在任务子集上指令微调。
- 关键结果：Tk-Instruct（11B）在未见任务上超过 InstructGPT（175B）约 9+ 点（基于 ROUGE-L），证明指令多样性比纯规模更利于泛化。
- 提供丰富的指令格式消融（仅 definition / +正例 / +负例 / +解释）。
- 是 FLAN/T0 之外另一主流指令微调数据源，推动开源指令微调生态。

## 原始链接
- url: https://arxiv.org/abs/2204.07705
- pdf_url: https://arxiv.org/pdf/2204.07705
- github_url: https://github.com/allenai/natural-instructions

## 一手源存档（sources/）
- super-naturalinstructions.pdf  （PDF 不入 git，走 HF bucket）
