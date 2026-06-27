---
title: "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"
org: Google Research
country: US
date: 2023-05
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2305.13245
pdf_url: https://arxiv.org/pdf/2305.13245
downloaded: [gqa-2305.13245.pdf]
---

> 📄 主题索引条目 —— 完整六维精读见 [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](../../2023/gqa.md)。

## 一句话定位
分组查询注意力（Grouped-Query Attention），介于 MHA 与 MQA 之间，多个 query head 共享一组 KV head，在几乎不降质的前提下大幅缩小推理 KV cache。
