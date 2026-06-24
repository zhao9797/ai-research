---
title: "Pixtral 12B"
org: Mistral AI
country: EU
date: 2024-10
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2410.07073
pdf_url: https://arxiv.org/pdf/2410.07073
github_url:
downloaded: [2410.07073.pdf]
---

## 一句话定位
Pixtral 12B：Mistral 首个多模态模型，从零训练的新视觉编码器可按原生分辨率/宽高比处理图像，128K 上下文可处理任意数量图片，且不牺牲纯文本能力，Apache 2.0。

## 摘要
Pixtral-12B 是 12B 参数多模态模型，训练用于理解自然图像与文档，在多项多模态基准上领先、超过若干更大模型。不同于许多开源模型，Pixtral 同时也是其尺寸下的顶尖纯文本模型，不为多模态牺牲语言性能。它用一个从零训练的新视觉编码器，能以原生分辨率与宽高比摄入图像，给用户处理图像所用 token 数的灵活性。128K 长上下文窗口可处理任意数量图像。Pixtral 12B 大幅超过同尺寸开放模型（Llama-3.2 11B、Qwen-2-VL 7B），也超过大得多的 Llama-3.2 90B（小 7×）。还贡献开源基准 MM-MT-Bench。

## 关键技术细节
- 视觉编码器：Pixtral-ViT，4 亿参数，从零训练；支持原生分辨率/宽高比与可变 token 数（RoPE-2D）。
- LLM 主干：基于 Mistral NeMo 12B。
- 上下文：128K，可处理任意数量图像。
- 性能：超 Llama-3.2 11B、Qwen-2-VL 7B；超 Llama-3.2 90B（小 7×）；纯文本不退化。
- 贡献：MM-MT-Bench 多模态实用评测基准；标准化评测协议。
- 许可：Apache 2.0。

## 原始链接
- url: https://arxiv.org/abs/2410.07073
- pdf_url: https://arxiv.org/pdf/2410.07073

## 本地落盘文件
- ../../../sources/llm/2024/2410.07073.pdf
