---
title: "Big Bird: Transformers for Longer Sequences"
org: Google Research
country: US
date: 2020-07
type: paper
categories: [架构]
url: https://arxiv.org/abs/2007.14062
pdf_url: https://arxiv.org/pdf/2007.14062
github_url: https://github.com/google-research/bigbird
downloaded: [bigbird.pdf]
---

## 一句话定位
BigBird 提出「全局 + 局部窗口 + 随机」三类稀疏注意力的组合，把复杂度降到线性，并证明它是图灵完备的、能逼近完整注意力。

## 摘要（3-6 句）
BigBird 用一种广义稀疏注意力近似完整注意力：每个 token 关注少量全局 token、局部邻居窗口、以及若干随机 token。论文从理论上证明这种稀疏模式保留了完整 Transformer 的表达力（图灵完备、可逼近任意序列函数）。线性复杂度让它能处理比 BERT 长 8 倍的序列。在长文档 QA、摘要、以及基因组学等任务上取得 SOTA。

## 关键技术细节
- 三种注意力组合：global tokens（少量全局可见）+ window attention（局部）+ random attention（随机 r 个 token）。
- 理论：证明该稀疏注意力图灵完备，且是 sparse universal approximator。
- 复杂度从 O(n²) 降到 O(n)，可处理约 4096+ token（约 BERT 的 8 倍长度）。
- 应用扩展到长文档 NLP 与基因组序列（DNA）建模。

## 原始链接
- url: https://arxiv.org/abs/2007.14062
- pdf_url: https://arxiv.org/pdf/2007.14062
- github_url: https://github.com/google-research/bigbird

## 一手源存档（sources/）
- bigbird.pdf  （PDF 不入 git，走 HF bucket）
