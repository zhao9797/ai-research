---
title: "Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time"
org: Univ. of Washington / Google / Columbia 等
country: US
date: 2022-03
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2203.05482
pdf_url: https://arxiv.org/pdf/2203.05482
github_url: https://github.com/mlfoundations/model-soups
downloaded: [model-soups.pdf]
---

## 一句话定位
"模型汤"：对多个不同超参微调出的模型直接平均权重，免费提升精度与鲁棒性，无额外推理成本。

## 摘要
传统最大化精度的做法是训练多组超参模型、选验证集最佳者、丢弃其余。本文重审在微调大预训练模型场景下的第二步：微调模型往往落在同一低误差盆地。证明平均多个用不同超参微调的模型权重常提升精度与鲁棒性。与常规集成不同，权重平均不增加推理或显存成本——称之为"model soups"。在 CLIP、ALIGN、JFT 预训练 ViT-G 上微调时，soup 配方显著超过盆地内最佳单模型。

## 关键技术细节
- 方法：uniform soup（全部平均）/ greedy soup（按验证集贪心加入有增益的模型）。
- 关键前提：微调模型位于同一损失盆地，权重可线性插值/平均（mode connectivity）。
- 结果：greedy soup 把 ViT-G 在 ImageNet 上推到当时 SOTA（90.94%），并提升分布外鲁棒性。
- 零额外推理成本（仍是单模型），区别于输出集成。
- 影响后续 weight averaging / model merging（SWA、WiSE-FT、task arithmetic）一系列工作。

## 原始链接
- url: https://arxiv.org/abs/2203.05482
- pdf_url: https://arxiv.org/pdf/2203.05482
- github_url: https://github.com/mlfoundations/model-soups

## 一手源存档（sources/）
- model-soups.pdf  （PDF 不入 git，走 HF bucket）
