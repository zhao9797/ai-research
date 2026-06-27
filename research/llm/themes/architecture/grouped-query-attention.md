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

> 📄 主题索引条目 —— 完整六维精读见 [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](../../2023/gqa.md)。

## 一句话定位
提出 Grouped-Query Attention (GQA)：在 MHA 与 MQA 之间取折中，把 query 头分成若干组、每组共享一份 K/V，并给出从已有 MHA 检查点低成本「uptraining」到 GQA 的方法。
