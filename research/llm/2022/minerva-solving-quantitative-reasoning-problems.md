---
title: Solving Quantitative Reasoning Problems with Language Models (Minerva)
org: Google Research
country: US
date: 2022-06
type: paper
categories: [预训练数据, 后训练]
url: https://arxiv.org/abs/2206.14858
pdf_url: https://arxiv.org/pdf/2206.14858
github_url:
downloaded: [minerva.pdf]
---

## 一句话定位
在 PaLM 基础上用大规模 LaTeX/数学网页继续预训练得到 Minerva，无需外部工具即在 STEM 定量推理上取得 SOTA。

## 摘要
SOTA 模型在需要定量推理的任务（大学级数学、科学、工程）上普遍吃力。Minerva 在通用自然语言数据上预训练后，进一步在技术内容（含 LaTeX 公式的 arXiv、网页数学）上继续训练。模型在技术基准上取得 SOTA，且不使用外部工具。在 200+ 道本科物理、生物、化学、经济等需定量推理的题目上能正确回答近 1/3。

## 关键技术细节
- 基座：PaLM（8B / 62B / 540B），在 118GB 含数学/科学内容的数据集（arXiv LaTeX + 数学网页）上继续预训练 26B–38.5B token。
- 关键：保留 LaTeX/数学符号格式（不剥离），让模型学会数学排版语义。
- 推理：CoT + few-shot + majority voting（self-consistency）。
- 结果：MATH 数据集 50.3%（540B + maj voting），MMLU-STEM、GSM8K 大幅领先；不调用计算器/Python 等外部工具。
- 证明"领域继续预训练 + 格式保真 + 多数投票"对数学推理的有效性。

## 原始链接
- url: https://arxiv.org/abs/2206.14858
- pdf_url: https://arxiv.org/pdf/2206.14858

## 本地落盘文件
- ../../../sources/llm/2022/minerva.pdf
