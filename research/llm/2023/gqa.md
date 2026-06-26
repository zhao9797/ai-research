---
title: "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"
org: Google Research
country: US
date: 2023-05
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2305.13245
pdf_url: https://arxiv.org/pdf/2305.13245
downloaded: [gqa.pdf]
---

## 一句话定位
Google 提出 Grouped-Query Attention，介于 MHA 与 MQA 之间，被 Llama2/Mistral 等广泛采用的标配。

## 摘要
MQA 仅用单个 KV 头大幅加速解码但损质量，且不愿为加速单独训模型。本文(1)提出用原预训练 5% 算力把已有多头检查点 uptrain 成 MQA 模型；(2)提出 GQA——MQA 的推广，用中间数量(>1 且 < 查询头数)的 KV 头。uptrained GQA 质量接近 MHA、速度接近 MQA。

## 关键技术细节
- GQA：把 query heads 分成 G 组，每组共享一对 KV 头；G=1 退化为 MQA，G=heads 即 MHA。
- Uptraining：用约 5% 原预训练算力把 MHA checkpoint 转为 GQA/MQA（mean-pool KV 头后继续训）。
- 收益：解码大幅加速、KV cache 显存大降，质量损失极小。
- 影响：Llama 2(34B/70B)、Mistral、Gemini 等成为标配；长上下文推理关键。

## 原始链接
- url: https://arxiv.org/abs/2305.13245
- pdf_url: https://arxiv.org/pdf/2305.13245

## 一手源存档（sources/）
- gqa.pdf  （PDF 不入 git，走 HF bucket）
