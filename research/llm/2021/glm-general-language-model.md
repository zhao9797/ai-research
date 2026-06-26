---
title: "GLM: General Language Model Pretraining with Autoregressive Blank Infilling"
org: 清华 (Tsinghua) / BAAI 智源
country: China
date: 2021-03
type: paper
categories: [架构]
url: https://arxiv.org/abs/2103.10360
pdf_url: https://arxiv.org/pdf/2103.10360
github_url: https://github.com/THUDM/GLM
downloaded: [arxiv-2103.10360.pdf]
---

## 一句话定位
清华 + 智源的 GLM：用"自回归空白填充"（autoregressive blank infilling）统一自编码/自回归/编码器-解码器三类预训练范式，是后续 GLM-130B / ChatGLM 的架构基石。

## 摘要（3-6 句）
GLM 提出 General Language Model 框架，用自回归空白填充目标统一 BERT（自编码）、GPT（自回归）、T5（编码器-解码器）三类预训练。通过随机遮盖文本片段（spans）并以自回归方式还原，并加入 2D 位置编码与片段乱序，使同一模型在 NLU、条件生成、无条件生成上都强。在 SuperGLUE、abstractive summarization、语言建模等多类任务上以相当或更少参数超过 BERT/T5/GPT。

## 关键技术细节
- 核心目标：autoregressive blank infilling——遮盖连续 spans，自回归还原被遮盖内容。
- 2D 位置编码：分别编码片段在原文中的位置与片段内位置。
- 多任务预训练：短 span（NLU）+ 长 span（生成）混合，统一三种范式。
- 在 SuperGLUE 上以相近参数超过 BERT-Large；同模型可做生成。
- 是 GLM-130B（2022）与 ChatGLM 系列的架构起点；代码 THUDM/GLM。
- 发表于 ACL 2022。

## 原始链接
- url: https://arxiv.org/abs/2103.10360
- pdf_url: https://arxiv.org/pdf/2103.10360
- github_url: https://github.com/THUDM/GLM

## 一手源存档（sources/）
- [arxiv-2103.10360.pdf](https://arxiv.org/pdf/2103.10360)  （arXiv 原文 PDF，不入 git）
