---
title: "Yuan 2.0-M32: Mixture of Experts with Attention Router"
org: 浪潮信息 (IEIT Systems)
country: 中国
date: 2024-05
type: arxiv
categories: [架构, AI infra]
url: https://arxiv.org/abs/2405.17976
pdf_url: https://arxiv.org/pdf/2405.17976
github_url: https://github.com/IEIT-Yuan/Yuan2.0-M32
downloaded: [files/yuan2-m32.pdf]
---

## 一句话定位
浪潮"源 2.0-M32" MoE，提出 Attention Router（注意力路由器）替代经典路由，32 专家激活 2 个，仅 3.7B 激活参数。

## 摘要
Yuan 2.0-M32 基础架构类似 Yuan-2.0 2B，采用 32 专家、激活 2 个的 MoE。提出新的 Attention Router 路由网络——考虑专家间相关性来更高效地选专家，相比经典路由提升精度。从头训练 2000B token，训练算力仅为同参数规模稠密模型的 9.25%。仅 3.7B 激活参数即在代码、数学与多领域展现有竞争力的能力。

## 关键技术细节（带数字）
- MoE：40B 总参，32 专家激活 2 个，3.7B 激活参数。
- 路由：Attention Router（注意力路由器，建模专家间相关性，优于经典 router）。
- 训练数据：2000B tokens 从头训练。
- 算力：仅为同参数规模稠密模型的 9.25%。
- 性能：在 MATH/GSM8K/HumanEval/ARC 等基准上以 3.7B 激活达到有竞争力水平。

## 原始链接
- arXiv: https://arxiv.org/abs/2405.17976
- PDF: https://arxiv.org/pdf/2405.17976
- GitHub: https://github.com/IEIT-Yuan/Yuan2.0-M32

## 一手源存档（sources/）
- yuan2-m32.pdf  （PDF 不入 git，走 HF bucket）
