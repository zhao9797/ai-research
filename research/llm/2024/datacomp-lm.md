---
title: "DataComp-LM: In search of the next generation of training sets for language models"
org: DataComp / University of Washington / Apple / TRI / AI2 等
country: US
date: 2024-06
type: paper
categories: [预训练数据]
url: https://arxiv.org/abs/2406.11794
pdf_url: https://arxiv.org/pdf/2406.11794
github_url: https://github.com/mlfoundations/dclm
downloaded: [2406.11794.pdf]
---

## 一句话定位
DCLM：一个可控数据集实验的标准化测试平台（240T token 语料 + 统一训练配方 + 53 项评测），证明基于模型的过滤是构建高质量训练集的关键。

## 摘要
DataComp for Language Models（DCLM）是用于受控数据集实验、以改进语言模型为目标的测试平台。提供从 Common Crawl 抽取的 240T token 标准化语料、基于 OpenLM 框架的有效预训练配方、以及 53 项下游评测套件。参赛者可在 412M–7B 参数规模上试验去重、过滤、数据混合等策略。作为基线，作者做了大量实验，发现基于模型的过滤是组装高质量训练集的关键。所得 DCLM-Baseline 数据集能让一个 7B 模型用 2.6T token 训到 MMLU 5-shot 64%；相比此前开放数据 SOTA（MAP-Neo）提升 6.6 个百分点且少 40% 算力，并以 6.6× 更少算力达到与 Llama 3 8B 相当的水平。

## 关键技术细节
- 语料：DCLM-Pool，240T token（来自 Common Crawl，是当时最大公开语料）。
- 关键发现：fastText 等基于模型的质量分类器过滤 >> 启发式过滤。
- DCLM-Baseline：7B 模型用 2.6T token → MMLU 64%；与 Mistral-7B-v0.3、Llama 3 8B（MMLU 63%/66%）相当，但算力少 6.6×。
- 规模档：412M、1B、3B、7B；统一 OpenLM 训练框架 + 53 项评测。
- 全开放：语料、过滤模型、训练/评测代码。

## 原始链接
- url: https://arxiv.org/abs/2406.11794
- pdf_url: https://arxiv.org/pdf/2406.11794
- github: https://github.com/mlfoundations/dclm

## 一手源存档（sources/）
- [2406.11794.pdf](https://arxiv.org/pdf/2406.11794)  （arXiv 原文 PDF，不入 git）
