---
title: Synthesizer — Rethinking Self-Attention in Transformer Models
org: Google Research
country: US
date: 2020-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2005.00743
pdf_url: https://arxiv.org/pdf/2005.00743
github_url:
downloaded: [arxiv-2005.00743.pdf]
---

## 一句话定位
Synthesizer 质疑“点积自注意力是否必要”，提出直接“合成”注意力权重（不依赖 token 间点积交互）的多种变体，发现随机/学习式合成注意力在许多任务上可与标准注意力媲美。

## 摘要（3-6 句）
论文系统研究了点积自注意力的必要性，提出 Synthesizer：不通过 query-key 点积，而是用稠密前馈（Dense Synthesizer）或可学习/随机矩阵（Random Synthesizer）直接合成对齐（注意力）矩阵。在机器翻译、语言建模、文本分类、对话生成、GLUE/SuperGLUE 等任务上，合成注意力在多数情况下与标准 Transformer 相当甚至更优，挑战了点积注意力不可或缺的假设。

## 关键技术细节
- Dense Synthesizer：用两层前馈直接由每个 token 的表示生成其对所有位置的注意力分布（不做 token 间交互）。
- Random Synthesizer：注意力矩阵为可学习（或固定随机）参数，与输入无关。
- Factorized 变体：对合成矩阵做低秩分解以省参。
- 可与标准点积注意力混合。
- 发现：在机器翻译、摘要、对话、语言建模与 GLUE/SuperGLUE 上，合成注意力多数情况下匹配或超过 vanilla Transformer。

## 原始链接
- url: https://arxiv.org/abs/2005.00743
- pdf_url: https://arxiv.org/pdf/2005.00743

## 一手源存档（sources/）
- [arxiv-2005.00743.pdf](https://arxiv.org/pdf/2005.00743)  （arXiv 原文 PDF，不入 git）
