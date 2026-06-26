---
title: Textbooks Are All You Need (phi-1)
org: Microsoft Research
country: US
date: 2023-06
type: paper
categories: [预训练数据, 后训练]
url: https://arxiv.org/abs/2306.11644
pdf_url: https://arxiv.org/pdf/2306.11644
downloaded: [textbooks-are-all-you-need-phi-1.pdf]
---

## 一句话定位
微软提出“教材级高质量数据”路线，1.3B 的 phi-1 在代码上逼近 SOTA，开启数据质量>规模的小模型流派。

## 摘要
phi-1 是 1.3B 参数的代码 LLM，远小于竞品：用精选“教材质量”网络数据(6B token)+GPT-3.5 合成教材与习题(1B token)，在 8 张 A100 上训 4 天。尽管极小，HumanEval pass@1 达 50.6%、MBPP 55.5%。微调前后及 350M 的 phi-1-small 均显示惊人涌现能力。

## 关键技术细节
- 参数：phi-1 1.3B；phi-1-small 350M（HumanEval 仍达 45%）。
- 数据（核心创新）：约 7B token = 6B 经分类器筛选的教材质量网络代码 + 1B GPT-3.5 合成 Python 教材与习题。
- 微调数据：约 180M token 的合成代码练习(CodeExercises)。
- infra：8×A100，4 天（pretrain）。
- 评测：HumanEval 50.6%、MBPP 55.5%（远超同尺寸/更大模型）。
- 论点：数据质量可大幅降低算力与参数需求。

## 原始链接
- url: https://arxiv.org/abs/2306.11644
- pdf_url: https://arxiv.org/pdf/2306.11644

## 一手源存档（sources/）
- textbooks-are-all-you-need-phi-1.pdf  （PDF 不入 git，走 HF bucket）
