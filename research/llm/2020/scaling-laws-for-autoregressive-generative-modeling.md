---
title: Scaling Laws for Autoregressive Generative Modeling
org: OpenAI
country: US
date: 2020-10
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2010.14701
pdf_url: https://arxiv.org/pdf/2010.14701
github_url:
downloaded: [arxiv-2010.14701.pdf]
---

## 一句话定位
把 Scaling Laws 从纯文本扩展到图像、视频、多模态（图文）、数学等多个生成域，证明幂律标度是跨模态的普适现象。

## 摘要（3-6 句）
论文（Henighan、Kaplan 等）在图像生成、视频生成、多模态图文、以及数学问题求解四类自回归生成任务上测量交叉熵损失的标度规律，发现各域损失对模型规模均呈幂律下降，并存在一个不可约损失项（数据熵）加可约幂律项的统一形式 L = L∞ + (N0/N)^α。论文还研究了最优模型规模与算力的关系，以及生成模型与下游任务（如图像分类）性能间的关系。

## 关键技术细节
- 统一形式：L(N) = L∞ + (N0/N)^αN，其中 L∞ 是数据本身的熵下界，αN 为幂律指数。
- 跨域验证：文本、图像（VQ-VAE 编码后的离散 token）、视频、多模态图文、以及数学，均符合该形式。
- 最优模型规模与算力同样呈幂律；提出“最优模型规模随算力的标度指数”。
- 信息论视角：可约损失对应模型可学习到的信息，L∞ 对应不可压缩的数据熵。
- 与下游任务关联：生成预训练损失越低，迁移到分类等任务的表现越好。

## 原始链接
- url: https://arxiv.org/abs/2010.14701
- pdf_url: https://arxiv.org/pdf/2010.14701

## 一手源存档（sources/）
- [arxiv-2010.14701.pdf](https://arxiv.org/pdf/2010.14701)  （arXiv 原文 PDF，不入 git）
