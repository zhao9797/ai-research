---
title: GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints
org: Google Research
country: US
date: 2023-05
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2305.13245
pdf_url: https://arxiv.org/pdf/2305.13245
downloaded: [gqa-2305.13245.pdf]
---

## 一句话定位
分组查询注意力（Grouped-Query Attention），介于 MHA 与 MQA 之间，多个 query head 共享一组 KV head，在几乎不降质的前提下大幅缩小推理 KV cache。

## 摘要（3-6 句）
Multi-Query Attention（MQA）让所有 head 共享单一 KV，推理快但掉点且训练不稳。GQA 把 query head 分成 G 组、每组共享一份 KV，是 MHA（G=heads）与 MQA（G=1）的插值。论文给出从已有 MHA checkpoint 通过 uptraining（额外少量训练）转换到 GQA 的方法。GQA 以接近 MHA 的质量取得接近 MQA 的推理速度，被 Llama 2/3、Mistral 等广泛采用。

## 关键技术细节
- KV head 数从 H（MHA）减到 G（1<G<H），KV cache 与解码带宽随之下降。
- uptraining：用原 checkpoint 平均池化 KV 投影后再用 ~5% 预训练算力微调。
- 质量-速度折中：质量接近 MHA，速度接近 MQA；成为现代 LLM（Llama2-70B 起）标配。

## 原始链接
- url: https://arxiv.org/abs/2305.13245
- pdf_url: https://arxiv.org/pdf/2305.13245

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/gqa-2305.13245.pdf
