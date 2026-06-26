---
title: Rethinking Attention with Performers
org: Google / DeepMind / University of Cambridge
country: US
date: 2020-09
type: paper
categories: [架构]
url: https://arxiv.org/abs/2009.14794
pdf_url: https://arxiv.org/pdf/2009.14794
github_url: https://github.com/google-research/google-research/tree/master/performer
downloaded: [arxiv-2009.14794.pdf]
---

## 一句话定位
Performer 用 FAVOR+（基于正随机特征的核近似）把 softmax 注意力线性化，得到无偏、低方差、线性时间与空间复杂度的注意力，且无需稀疏性假设。

## 摘要（3-6 句）
Performer 提出 FAVOR+（Fast Attention Via positive Orthogonal Random features），用随机特征映射对 softmax 注意力核做无偏估计，将注意力的时间/空间复杂度从二次降到线性，且与标准 Transformer 完全兼容（可加载预训练权重微调）。与依赖稀疏/低秩先验的方法不同，Performer 不引入此类假设，提供可证明的近似误差界。在蛋白质序列建模等长序列任务上验证了准确性与可扩展性。

## 关键技术细节
- FAVOR+：用正交正随机特征（positive orthogonal random features）近似 softmax 核，保证非负、低方差、无偏估计。
- 复杂度：线性 O(n)（时间与空间），可处理远超标准注意力的序列长度。
- 兼容性：可与常规 Transformer 互换，支持加载已训练权重后微调（backward compatible）。
- 理论：给出近似的集中性（concentration）与误差界。
- 应用：长序列任务（如蛋白质序列 ProGen 类任务）验证质量与效率。

## 原始链接
- url: https://arxiv.org/abs/2009.14794
- pdf_url: https://arxiv.org/pdf/2009.14794

## 一手源存档（sources/）
- [arxiv-2009.14794.pdf](https://arxiv.org/pdf/2009.14794)  （arXiv 原文 PDF，不入 git）
