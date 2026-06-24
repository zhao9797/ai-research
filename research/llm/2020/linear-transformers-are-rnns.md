---
title: Transformers are RNNs — Fast Autoregressive Transformers with Linear Attention
org: Idiap Research Institute / EPFL
country: EU
date: 2020-06
type: paper
categories: [架构]
url: https://arxiv.org/abs/2006.16236
pdf_url: https://arxiv.org/pdf/2006.16236
github_url: https://github.com/idiap/fast-transformers
downloaded: [arxiv-2006.16236.pdf]
---

## 一句话定位
用核特征映射把 softmax 注意力线性化，复杂度降到 O(N)，并揭示带因果掩码的线性注意力 Transformer 在推理时等价于 RNN，可常数内存自回归生成、推理快达数千倍。

## 摘要（3-6 句）
论文将注意力表述为核函数内积，用特征映射（如 elu+1）替代 softmax，使自注意力复杂度从 O(N²) 降到 O(N)（N 为序列长度）。对于自回归（因果掩码）情形，线性注意力可写成循环形式，使 Transformer 等价于一个具有线性注意力的 RNN，从而在自回归推理时只需常数内存与时间。实验显示在很长序列上推理速度提升可达数千倍，质量与标准 Transformer 相当。

## 关键技术细节
- 线性注意力：attention(Q,K,V) 用特征映射 φ(·)（论文用 φ(x)=elu(x)+1）改写为 (φ(Q)(φ(K)ᵀV)) / (φ(Q) Σφ(K))，复杂度 O(N)。
- 因果版可递推：维护一个累积的 KV 状态矩阵与归一化项，逐步更新，等价于 RNN。
- 自回归生成：常数内存、线性时间，对长序列推理快达约 4000 倍（论文报告）。
- 任务：图像自回归生成（MNIST/CIFAR）、自动语音识别等长序列任务验证。

## 原始链接
- url: https://arxiv.org/abs/2006.16236
- pdf_url: https://arxiv.org/pdf/2006.16236
- github_url: https://github.com/idiap/fast-transformers

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2006.16236.pdf
