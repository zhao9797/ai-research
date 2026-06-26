---
title: "Textbooks Are All You Need II: phi-1.5 technical report"
org: Microsoft Research
country: US
date: 2023-09
type: paper
categories: [预训练数据]
url: https://arxiv.org/abs/2309.05463
pdf_url: https://arxiv.org/pdf/2309.05463
downloaded: [phi-1-5.pdf]
---

## 一句话定位
phi 路线延伸到常识推理，1.3B 的 phi-1.5 媲美 5x 大模型，且因无网络数据而毒性更低。

## 摘要
延续 TinyStories→phi-1 的合成数据路线，phi-1.5 是 1.3B 模型，聚焦自然语言常识推理，性能媲美 5x 大的模型，在小学数学、基础代码等复杂推理上超过多数非前沿 LLM。展现大模型的诸多特性（如逐步思考、初步 in-context learning），同时因几乎不用网络数据而在毒性/偏见上有所改善。开源。

## 关键技术细节
- 参数：1.3B（与 phi-1 同尺寸，但面向 NL 推理）。
- 数据：约 30B token，其中约 20B 为新合成的“教材式”常识推理数据（用 GPT-3.5 生成），无网络爬取文本。
- 涌现能力：逐步推理(step by step)、rudimentary in-context learning。
- 评测：常识/语言任务媲美 5x 大模型；GSM8K、HumanEval 上超多数非前沿模型。
- 安全：无 web 数据带来更低毒性/偏见。

## 原始链接
- url: https://arxiv.org/abs/2309.05463
- pdf_url: https://arxiv.org/pdf/2309.05463

## 一手源存档（sources/）
- phi-1-5.pdf  （PDF 不入 git，走 HF bucket）
