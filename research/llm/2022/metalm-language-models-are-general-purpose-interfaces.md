---
title: Language Models are General-Purpose Interfaces (MetaLM)
org: Microsoft Research    country: US    date: 2022-06    type: paper
categories: [架构]
url: https://arxiv.org/abs/2206.06336    pdf_url: https://arxiv.org/pdf/2206.06336    github_url: https://github.com/microsoft/unilm
downloaded: [metalm.pdf]
---

## 一句话定位
微软 MetaLM：用语言模型作为各种基础模型的"通用接口/任务层"，提出半因果语言建模目标统一因果与非因果模型优点。

## 摘要
基础模型因跨广泛下游有效而备受关注，但尽管架构趋同，多数预训练模型仍为特定任务或模态设计。本文提出用语言模型作为对接各种基础模型的通用接口：一组预训练编码器感知不同模态（如视觉、语言），并与扮演通用任务层的语言模型对接。提出半因果（semi-causal）语言建模目标联合预训练接口与模块化编码器，兼收因果与非因果建模优点：既继承 in-context learning 能力，又获得非因果编码器的迁移能力。

## 关键技术细节
- 架构：模块化双向编码器（perceiver/encoder）作为"模块"，挂接到一个因果语言模型"通用任务层"。
- 半因果目标：编码器部分用非因果（双向）建模，语言模型部分用因果建模，联合训练。
- 能力：兼具 in-context learning / few-shot（来自因果 LM）与强迁移微调（来自非因果编码器）。
- 支持纯语言与视觉-语言多模态任务。
- 属微软 UniLM 系列，预示"LLM 作为多模型/多模态协调中枢"的架构思路。

## 原始链接
- url: https://arxiv.org/abs/2206.06336
- pdf_url: https://arxiv.org/pdf/2206.06336
- github_url: https://github.com/microsoft/unilm

## 本地落盘文件
- ../../../sources/llm/2022/metalm.pdf
