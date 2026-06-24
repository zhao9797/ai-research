---
title: Big Bird — Transformers for Longer Sequences
org: Google Research
country: US
date: 2020-07
type: paper
categories: [架构]
url: https://arxiv.org/abs/2007.14062
pdf_url: https://arxiv.org/pdf/2007.14062
github_url: https://github.com/google-research/bigbird
downloaded: [arxiv-2007.14062.pdf]
---

## 一句话定位
BigBird 用“随机 + 局部窗口 + 全局”的稀疏注意力把 Transformer 的复杂度从序列长度的二次降为线性，把可处理上下文长度提升到 8 倍（如 4096），并在理论上证明其图灵完备与序列函数逼近能力。

## 摘要（3-6 句）
BigBird 提出一种稀疏注意力机制，由三部分组成：随机注意力、滑动窗口（局部）注意力、以及若干全局 token，使注意力复杂度从 O(n²) 降为 O(n)。论文证明该稀疏注意力是序列函数的通用逼近器且图灵完备，理论上保留了完整注意力的表达力。实践上 BigBird 在相同硬件上把可处理序列长度提升约 8 倍，在长文档分类、问答、摘要以及基因组学等任务上取得 SOTA。

## 关键技术细节
- 稀疏注意力三组件：global tokens（关注全部并被全部关注）+ window attention（局部滑窗）+ random attention（随机连接）。
- 复杂度：O(n)（线性），相比标准 O(n²)；同等内存下序列长度提升约 8 倍（如 512 → 4096）。
- 理论结果：证明该稀疏注意力为序列到序列函数的通用逼近器，且图灵完备。
- 任务：长文档 QA（HotpotQA、TriviaQA、Natural Questions、WikiHop）、长文档摘要（arXiv、PubMed、BigPatent）、基因组学（启动子预测、染色质特征）SOTA。
- 与 Longformer 同期、思路相近（局部 + 全局），BigBird 额外引入随机注意力并给出理论分析。

## 原始链接
- url: https://arxiv.org/abs/2007.14062
- pdf_url: https://arxiv.org/pdf/2007.14062
- github_url: https://github.com/google-research/bigbird

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2007.14062.pdf
