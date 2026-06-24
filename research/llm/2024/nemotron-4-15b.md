---
title: "Nemotron-4 15B Technical Report"
org: NVIDIA
country: US
date: 2024-02
type: report
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2402.16819
pdf_url: https://arxiv.org/pdf/2402.16819
github_url:
downloaded: [2402.16819.pdf]
---

## 一句话定位
NVIDIA Nemotron-4 15B：15B 多语言模型，训练 8T token，主打超同级的多语言能力。

## 摘要
Nemotron-4 15B 为 15B 参数多语言大模型，训练于 8T 文本 token。在英语、多语言、编码任务上表现强劲：在 7 个下游评测领域中的 4 个超过所有同规模开放模型，其余领域与领先模型竞争。其多语言能力为同级最佳，甚至超过 4 倍大及专门为多语言设计的模型。

## 关键技术细节
- 规模：15B 参数，decoder-only Transformer。
- 训练 token：8T（英文 + 多语言 53 种 + 43 种编程语言）。
- 架构：RoPE、squared ReLU 激活、无 bias、GQA；tokenizer SentencePiece 256K 词表。
- 算力：384 台 DGX H100（3072 H100 GPU），TP+DP，BF16。
- 多语言：同级最佳，超 4× 大模型。

## 原始链接
- url: https://arxiv.org/abs/2402.16819
- pdf_url: https://arxiv.org/pdf/2402.16819

## 本地落盘文件
- ../../../sources/llm/2024/2402.16819.pdf
