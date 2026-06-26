---
title: Reformer — The Efficient Transformer
org: Google Research / UC Berkeley
country: US
date: 2020-01
type: paper
categories: [架构]
url: https://arxiv.org/abs/2001.04451
pdf_url: https://arxiv.org/pdf/2001.04451
github_url: https://github.com/google/trax/tree/master/trax/models/reformer
downloaded: [arxiv-2001.04451.pdf]
---

## 一句话定位
Reformer 用局部敏感哈希（LSH）注意力把复杂度从 O(L²) 降到 O(L log L)，并用可逆残差层省去激活缓存，使单卡也能训练超长序列（最长可达 100 万 token）。

## 摘要（3-6 句）
Reformer 提出两项关键技术：用局部敏感哈希（LSH）近似注意力，使复杂度从序列长度的二次降为 O(L log L)；以及可逆残差层（reversible layers），训练时无需为反向传播存储每层激活，仅存一份。两者结合使 Reformer 在内存与速度上远优于标准 Transformer，可在单加速器处理长达 64K 甚至更长的序列，同时保持与标准 Transformer 相当的精度。

## 关键技术细节
- LSH Attention：用局部敏感哈希把相似的 query/key 分到同桶，只在桶内计算注意力，复杂度 O(L log L)。
- 可逆残差层（RevNet 式）：每层激活可由输出反推，反向传播无需存中间激活，显存与层数解耦。
- 分块前馈：FFN 分块计算进一步省显存。
- 可处理序列长度达 64K（论文实验），理论可到约 100 万 token。
- 在 enwik8、imagenet-64 生成等长序列任务上与标准 Transformer 精度相当但显存/速度大幅占优。

## 原始链接
- url: https://arxiv.org/abs/2001.04451
- pdf_url: https://arxiv.org/pdf/2001.04451

## 一手源存档（sources/）
- [arxiv-2001.04451.pdf](https://arxiv.org/pdf/2001.04451)  （arXiv 原文 PDF，不入 git）
