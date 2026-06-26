---
title: "Pixtral 12B"
org: Mistral AI
country: EU
date: 2024-10
type: report
categories: [架构]
url: https://arxiv.org/abs/2410.07073
pdf_url: https://arxiv.org/pdf/2410.07073
downloaded: [pixtral.pdf]
---

## 一句话定位
Pixtral 12B 是 Mistral 的多模态模型，配从零训练的原生分辨率/宽高比视觉编码器，128K 上下文可处理任意数量图像，且不牺牲纯文本能力。

## 摘要（3-6 句）
Pixtral 12B 是 120 亿参数多模态语言模型，能理解自然图像与文档，在多个多模态基准上领先，超过若干更大模型。与许多开源模型不同，Pixtral 同时是其规模下顶尖的纯文本模型，不为多模态牺牲语言能力。它用全新从零训练的视觉编码器，可按图像原生分辨率与宽高比摄入，token 数灵活；128K 长上下文窗口可处理任意数量图像。Pixtral 12B 明显超过同规模开源模型（Llama-3.2 11B、Qwen2-VL 7B），甚至超过 7 倍大的 Llama-3.2 90B。

## 关键技术细节
- 视觉编码器：从零训练的 Pixtral-ViT（约 400M），支持原生分辨率/宽高比，RoPE-2D 位置，token 数随图像大小可变。
- 语言主干：基于 Mistral Nemo 12B；128K 上下文。
- 可在长上下文里放入任意数量图像（图文交错）。
- 性能：超 Llama-3.2 11B、Qwen2-VL 7B；超过 7× 大的 Llama-3.2 90B；纯文本能力不退化。
- 同时开源 MM-MT-Bench 多模态评测基准。

## 原始链接
- url: https://arxiv.org/abs/2410.07073
- pdf_url: https://arxiv.org/pdf/2410.07073

## 一手源存档（sources/）
- pixtral.pdf  （PDF 不入 git，走 HF bucket）
