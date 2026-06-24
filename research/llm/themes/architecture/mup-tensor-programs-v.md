---
title: "Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer (muP / muTransfer)"
org: Microsoft / OpenAI
country: US
date: 2022-03
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2203.03466
pdf_url: https://arxiv.org/pdf/2203.03466
github_url: https://github.com/microsoft/mup
downloaded: [mup.pdf]
---

## 一句话定位
提出 Maximal Update Parametrization (muP) 与 muTransfer：在小模型上调好超参，零样本迁移到大模型，免去对大模型直接调参。

## 摘要（3-6 句）
大模型超参调优极贵。论文证明在 Maximal Update Parametrization (muP) 下，许多最优超参（学习率、初始化等）随模型宽度变化保持稳定。由此提出 muTransfer：用 muP 参数化目标大模型，在小代理模型上间接调超参，再零样本迁移到全尺寸模型，无需直接调大模型。作者在 Transformer 与 ResNet 上验证：例如从 13M 参数模型迁移预训练超参，结果超过已发表的 BERT-large（350M）数字；并把方法用到 GPT-3 规模。

## 关键技术细节
- muP：按宽度对初始化方差、学习率、注意力缩放等做特定缩放，使训练动力学随宽度保持「最大特征更新」不变。
- muTransfer：proxy 小模型调超参 → 零样本迁移到 target 大模型（width transfer，亦可一定程度 depth transfer）。
- 验证：13M→BERT-large 超参迁移超过原始 BERT-large；GPT-3 6.7B 用迁移超参超过原版。
- 大幅降低大模型超参搜索成本（小模型上搜索 + 一次大模型训练）。
- 作者：Greg Yang、Edward J. Hu 等（Microsoft + OpenAI）。

## 原始链接
- url: https://arxiv.org/abs/2203.03466
- pdf_url: https://arxiv.org/pdf/2203.03466
- github_url: https://github.com/microsoft/mup

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/mup.pdf
