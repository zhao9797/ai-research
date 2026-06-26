---
title: "GPT-NeoX-20B: An Open-Source Autoregressive Language Model"
org: EleutherAI
country: US
date: 2022-04
type: paper
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2204.06745
pdf_url: https://arxiv.org/pdf/2204.06745
github_url: https://github.com/EleutherAI/gpt-neox
downloaded: [gpt-neox-20b.pdf]
---

## 一句话定位
EleutherAI 开源的 200 亿参数自回归模型，当时权重公开的最大稠密自回归模型，在 the Pile 上训练，是开源 LLM 浪潮的重要一环。

## 摘要
GPT-NeoX-20B 是 200 亿参数的自回归语言模型，权重以宽松许可证向公众免费开放。它是发表时已知最大的、权重公开的稠密自回归模型。论文描述其架构与训练，并在语言理解、数学、知识类任务上评测。发现 GPT-NeoX-20B 是特别强的 few-shot 推理者，从 zero-shot 到 five-shot 的性能增益远超同规模 GPT-3 与 FairSeq 模型。训练与评测代码、权重全部开源。

## 关键技术细节
- 架构：decoder-only Transformer，20B 参数，44 层，隐藏维度 6144，64 注意力头。
- 改进：旋转位置编码（RoPE，仅应用于部分维度）、并行 Attention+FFN 计算、与 GPT-3 不同的初始化与超参。
- 训练数据：the Pile（EleutherAI 自建 825GB 多样化英文语料），约 472B token。
- tokenizer：基于 the Pile 重新训练的 BPE，50257→50432 词表，对空白/代码更友好。
- Infra：12 台 8×A100-40GB 节点（96 块 A100），Megatron + DeepSpeed，张量并行 + 流水并行。
- 开放：完整训练代码库 gpt-neox、权重、超参全公开。

## 原始链接
- url: https://arxiv.org/abs/2204.06745
- pdf_url: https://arxiv.org/pdf/2204.06745
- github_url: https://github.com/EleutherAI/gpt-neox

## 一手源存档（sources/）
- gpt-neox-20b.pdf  （PDF 不入 git，走 HF bucket）
