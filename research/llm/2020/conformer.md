---
title: Conformer — Convolution-augmented Transformer for Speech Recognition
org: Google
country: US
date: 2020-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2005.08100
pdf_url: https://arxiv.org/pdf/2005.08100
github_url:
downloaded: [arxiv-2005.08100.pdf]
---

## 一句话定位
Conformer 把卷积模块嵌入 Transformer，使模型同时捕捉局部（卷积）与全局（自注意力）特征，成为语音识别的标准骨干，并广泛影响后续语音/多模态架构。

## 摘要（3-6 句）
Conformer 在 Transformer 编码器中插入卷积模块，结合自注意力建模长程全局依赖与卷积建模局部特征。每个 Conformer block 采用“夹心”结构：两个半步前馈模块包裹自注意力与卷积模块。在 LibriSpeech 语音识别基准上，Conformer 以更少参数取得 SOTA：无语言模型时 test-clean/test-other 词错率 2.1%/4.3%，加语言模型后 1.9%/3.9%。

## 关键技术细节
- 模块结构：Feed-Forward（半步）→ Multi-Head Self-Attention（带相对位置编码）→ Convolution Module（含逐点卷积 + GLU + 深度可分卷积 + BatchNorm + Swish）→ Feed-Forward（半步）→ LayerNorm。
- 半步残差前馈（Macaron 式）：两个 FFN 各乘 0.5 系数夹住注意力与卷积。
- 规模：small (10M) / medium (30M) / large (118M) 参数。
- 结果（LibriSpeech）：large 模型 test-clean/test-other WER 2.1%/4.3%（无 LM）、1.9%/3.9%（有 LM）。
- 卷积模块捕捉局部、自注意力捕捉全局，二者互补是关键。

## 原始链接
- url: https://arxiv.org/abs/2005.08100
- pdf_url: https://arxiv.org/pdf/2005.08100

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2005.08100.pdf
