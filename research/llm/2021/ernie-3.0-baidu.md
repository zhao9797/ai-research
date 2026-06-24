---
title: "ERNIE 3.0: Large-scale Knowledge Enhanced Pre-training for Language Understanding and Generation"
org: 百度 (Baidu)
country: China
date: 2021-07
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2107.02137
pdf_url: https://arxiv.org/pdf/2107.02137
github_url: https://github.com/PaddlePaddle/ERNIE
downloaded: [arxiv-2107.02137.pdf]
---

## 一句话定位
百度 ERNIE 3.0：10B 参数的知识增强统一预训练框架，融合自回归 + 自编码网络，并引入大规模知识图谱，可同时服务理解与生成任务。

## 摘要（3-6 句）
ERNIE 3.0 提出统一的知识增强大规模预训练框架，融合自回归（生成）与自编码（理解）网络，使同一模型既能做 NLU 又能做 NLG，并支持 zero-shot/few-shot/fine-tune。模型在 4TB 语料（纯文本 + 大规模知识图谱）上训练 100 亿参数。结果在 54 个中文 NLP 任务上超过 SOTA。区别于纯文本训练的大模型，ERNIE 3.0 显式注入语言学知识与世界知识。

## 关键技术细节
- 参数：10B（100 亿）。
- 架构：Continual Multi-Paradigm Unified Pre-training；共享底层 + 任务特定上层（understanding network 自编码 + generation network 自回归）。
- 数据：4TB 语料 = 纯文本 + 大规模知识图谱（knowledge graph）注入。
- 知识增强：universal knowledge-text prediction 等任务把三元组与文本联合建模。
- 结果：54 个中文 NLP 任务 SOTA。
- 平台：PaddlePaddle（飞桨），代码在 PaddlePaddle/ERNIE。
- 同年 12 月升级为 ERNIE 3.0 Titan（260B，见单独条目）。

## 原始链接
- url: https://arxiv.org/abs/2107.02137
- pdf_url: https://arxiv.org/pdf/2107.02137
- github_url: https://github.com/PaddlePaddle/ERNIE

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2107.02137.pdf
