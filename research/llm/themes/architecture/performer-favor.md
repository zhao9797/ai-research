---
title: "Rethinking Attention with Performers (FAVOR+)"
org: Google / University of Cambridge / DeepMind / Alan Turing Institute
country: US/EU
date: 2020-09
type: paper
categories: [架构]
url: https://arxiv.org/abs/2009.14794
pdf_url: https://arxiv.org/pdf/2009.14794
github_url: https://github.com/google-research/google-research/tree/master/performer
downloaded: [performer.pdf]
---

## 一句话定位
Performer 用 FAVOR+（正交随机特征）无偏近似 softmax 注意力核，把注意力降到线性时间/空间复杂度，不依赖稀疏或低秩假设。

## 摘要（3-6 句）
Performer 是能以可证明精度近似完整 softmax 注意力的 Transformer，但只用线性（而非二次）的时间与空间，且不依赖稀疏性或低秩等先验。核心是 FAVOR+（Fast Attention Via positive Orthogonal Random features）：用正定的正交随机特征把 softmax kernel 写成两个特征映射的内积，从而把 QK^T 的二次结合律重排为线性。该近似无偏、方差可控。Performer 在长序列任务上与标准 Transformer 精度相当，内存与速度大幅改善，也适用于不可用 softmax 近似的核方法。

## 关键技术细节
- FAVOR+：用 positive orthogonal random features φ(·) 近似 exp(q·k)，使 softmax(QK^T)V ≈ φ(Q)(φ(K)^T V)，复杂度 O(L·d²) 线性于序列长 L。
- 无偏估计且方差低（正交特征 + 正值特征避免不稳定）。
- 不假设稀疏/低秩，可作 drug-in 替换标准注意力；可处理 backward-compatible 加载预训练 Transformer。
- 在 Long Range Arena、蛋白质序列建模等长序列任务上验证。
- 是早期 kernel-based 线性注意力的代表作。

## 原始链接
- url: https://arxiv.org/abs/2009.14794
- pdf_url: https://arxiv.org/pdf/2009.14794
- github_url: https://github.com/google-research/google-research/tree/master/performer

## 一手源存档（sources/）
- performer.pdf  （PDF 不入 git，走 HF bucket）
