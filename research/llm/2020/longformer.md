---
title: Longformer — The Long-Document Transformer
org: Allen Institute for AI (AI2)
country: US
date: 2020-04
type: paper
categories: [架构]
url: https://arxiv.org/abs/2004.05150
pdf_url: https://arxiv.org/pdf/2004.05150
github_url: https://github.com/allenai/longformer
downloaded: [arxiv-2004.05150.pdf]
---

## 一句话定位
Longformer 用线性复杂度的“滑动窗口 + 扩张窗口 + 任务相关全局注意力”处理数千 token 的长文档，是长上下文 Transformer 的代表作之一。

## 摘要（3-6 句）
Longformer 提出随序列长度线性增长的注意力机制，组合局部滑动窗口注意力、扩张（dilated）滑动窗口、以及针对任务设定的全局注意力，可直接处理上千 token 的长文档。它可作为 RoBERTa 的 drop-in 替换继续预训练。Longformer 在 text8/enwik8 字符级语言建模上达到 SOTA，并在 WikiHop、TriviaQA、HotpotQA、长文档分类等任务上超过 RoBERTa。论文还提出 Longformer-Encoder-Decoder (LED) 用于长文档生成式任务。

## 关键技术细节
- 注意力：滑动窗口（局部）+ 扩张滑动窗口（增大感受野）+ 任务相关全局注意力（如 [CLS] 或问题 token）。
- 复杂度 O(n)，支持序列长度达 4096+（远超 BERT 的 512）。
- 可作为 RoBERTa 的替换继续预训练；对长文档任务无需切块。
- 任务：enwik8/text8 字符级 LM SOTA；WikiHop、TriviaQA、HotpotQA、IMDB/Hyperpartisan 长文档分类。
- LED（Longformer-Encoder-Decoder）：用于 arXiv 长文档摘要等生成式任务。

## 原始链接
- url: https://arxiv.org/abs/2004.05150
- pdf_url: https://arxiv.org/pdf/2004.05150
- github_url: https://github.com/allenai/longformer

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2004.05150.pdf
