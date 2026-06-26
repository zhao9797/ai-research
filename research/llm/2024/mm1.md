---
title: "MM1: Methods, Analysis & Insights from Multimodal LLM Pre-training"
org: Apple
country: US
date: 2024-03
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2403.09611
pdf_url: https://arxiv.org/pdf/2403.09611
github_url:
downloaded: [2403.09611.pdf]
---

## 一句话定位
MM1：Apple 关于如何构建高性能多模态 LLM 的系统消融研究，得出"图像-caption + 交错图文 + 纯文本混合"对预训练至关重要等设计教训，最大 30B（含 MoE）。

## 摘要
本文研究构建高性能多模态大模型（MLLM）。通过对图像编码器、视觉语言连接器、各类预训练数据的细致消融，得出多条关键设计教训：例如大规模多模态预训练用图像-caption、交错图文、纯文本数据的精心混合，对取得 SOTA few-shot 结果至关重要；图像编码器连同图像分辨率与 image token 数影响很大，而视觉语言连接器设计相对次要。放大该配方后构建出 MM1（最大 30B，含稠密与 MoE 变体），在预训练指标上 SOTA、SFT 后在多模态基准上有竞争力。得益于大规模预训练，MM1 具备增强的 in-context learning 与多图推理（支持 few-shot CoT）。

## 关键技术细节
- 规模：3B、7B、30B；含稠密与 MoE 变体。
- 数据混合（关键发现）：image-caption + interleaved image-text + text-only 的混合对 few-shot/纯文本能力都重要。
- 重要性排序：图像分辨率 + image token 数 + 图像编码器 >> 视觉语言连接器设计。
- 能力：few-shot in-context learning、多图推理、few-shot CoT。
- 这是 Apple 多模态路线的公开基础（后续 MM1.5）。

## 原始链接
- url: https://arxiv.org/abs/2403.09611
- pdf_url: https://arxiv.org/pdf/2403.09611

## 一手源存档（sources/）
- [2403.09611.pdf](https://arxiv.org/pdf/2403.09611)  （arXiv 原文 PDF，不入 git）
