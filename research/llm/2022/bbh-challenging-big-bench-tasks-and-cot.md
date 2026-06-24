---
title: Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them (BBH)
org: Google Research / Stanford    country: US    date: 2022-10    type: paper
categories: [预训练数据, 后训练]
url: https://arxiv.org/abs/2210.09261    pdf_url: https://arxiv.org/pdf/2210.09261    github_url: https://github.com/suzgunmirac/BIG-Bench-Hard
downloaded: [bbh.pdf]
---

## 一句话定位
从 BIG-bench 中筛出 23 个模型尚未超过人类的"硬"任务（BBH），并证明 CoT 提示能让 PaLM 在其中多数任务上反超人类。

## 摘要
BIG-bench 是聚焦超出当前模型能力任务的评测套件。模型已取得不错进展，最佳模型在 65% 的 BIG-bench 任务上以 few-shot 超过人类平均评分。但模型在哪些任务上仍不及人类、这些任务是否真的不可解？本文聚焦 23 个有挑战的 BIG-bench 任务（称 BIG-Bench Hard, BBH）——即此前 LLM 评测未超过人类平均评分的任务。发现对 BBH 应用 CoT 提示能让 PaLM 在 23 个中的 10 个超过人类平均。

## 关键技术细节
- BBH：从 BIG-bench 精选 23 个"硬"任务（此前 LLM 未超人类平均）。
- 关键结果：标准 few-shot 下模型大多不及人类；加入 CoT 提示后，PaLM 在 10/23、Codex(code-davinci-002) 在 17/23 任务上超过人类平均。
- 说明很多"超人类难度"任务的瓶颈是提示方式（缺少分步推理）而非模型能力本身。
- BBH 成为后续 reasoning 评测（含 Flan/指令微调）的标准子集。

## 原始链接
- url: https://arxiv.org/abs/2210.09261
- pdf_url: https://arxiv.org/pdf/2210.09261
- github_url: https://github.com/suzgunmirac/BIG-Bench-Hard

## 本地落盘文件
- ../../../sources/llm/2022/bbh.pdf
