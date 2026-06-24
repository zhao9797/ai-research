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
提出 Grouped-Query Attention (GQA)：在 MHA 与 MQA 之间取折中，把 query 头分成若干组、每组共享一份 K/V，并给出从已有 MHA 检查点低成本「uptraining」到 GQA 的方法。

## 摘要（3-6 句）
MQA 虽能加速解码但常导致质量下降和训练不稳。GQA 把 H 个 query 头分成 G 组（1<G<H），每组共享一份 K/V 头，介于 MHA（G=H）与 MQA（G=1）之间。论文还提出用约 5% 的原预训练计算量把已有的 MHA 模型「uptrain」成 MQA/GQA。实验表明 GQA 在接近 MQA 的推理速度下达到接近 MHA 的质量。GQA 已成为 LLaMA-2/3、Mistral 等主流模型的默认注意力。

## 关键技术细节
- 结构：G 个 KV 组，G 介于 1（MQA）和 H（MHA）之间；KV cache ∝ G/H。
- Uptraining：把 MHA 的多头 K/V 投影按组做 mean-pooling 得到初始 GQA 权重，再用约 5% 原预训练算力继续训练恢复质量。
- 收益：相比 MHA 大幅降低 KV cache 与解码内存带宽，质量损失远小于 MQA。
- 已被 LLaMA-2 70B、LLaMA-3、Mistral、Qwen 等广泛采用，是当前 dense 模型的事实标准注意力。

## 原始链接
- url: https://arxiv.org/abs/2305.13245
- pdf_url: https://arxiv.org/pdf/2305.13245

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/gqa.pdf
