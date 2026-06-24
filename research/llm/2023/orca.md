---
title: "Orca: Progressive Learning from Complex Explanation Traces of GPT-4"
org: Microsoft Research
country: US
date: 2023-06
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2306.02707
pdf_url: https://arxiv.org/pdf/2306.02707
downloaded: [orca.pdf]
---

## 一句话定位
微软用 GPT-4 的“解释轨迹”教 13B 小模型学推理过程而非模仿风格，开创 explanation tuning。

## 摘要
Orca 是 13B 模型，学习模仿大模型(LFM)的推理过程而非仅风格。它从 GPT-4 的解释轨迹、逐步思维过程、复杂指令中学习，并用 ChatGPT 做教学助理。在 BBH、AGIEval 等复杂零样本推理上超 Vicuna-13B 100%+/42%，在 BBH 上与 ChatGPT 持平。

## 关键技术细节
- 参数：13B（基于 LLaMA）。
- 核心方法 Explanation Tuning：不只学最终答案，而是学 GPT-4 的 system message 引导的“逐步解释轨迹”。
- 渐进学习：先用 ChatGPT(GPT-3.5) 海量数据热身，再用 GPT-4 数据进阶（teacher assistant 机制）。
- 数据规模：约 5M ChatGPT + 1M GPT-4 解释样本，judicious sampling 选取。
- 评测：BBH 超 Vicuna-13B 113%、AGIEval 超 42%；BBH 与 ChatGPT 持平；SAT/LSAT/GRE/GMAT 零样本接近 ChatGPT。
- 论点：从逐步解释学习是提升小模型能力的有效方向。

## 原始链接
- url: https://arxiv.org/abs/2306.02707
- pdf_url: https://arxiv.org/pdf/2306.02707

## 本地落盘文件
- ../../../sources/llm/2023/orca.pdf
