---
title: "DeepSeek-OCR 2: Visual Causal Flow"
org: DeepSeek (深度求索)
country: China
date: 2026-01
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2601.20552
pdf_url: https://arxiv.org/pdf/2601.20552
github_url: https://github.com/deepseek-ai/DeepSeek-OCR
downloaded: [deepseek-ocr-2.pdf]
---

## 一句话定位
DeepSeek-OCR 2，提出 DeepEncoder V2，让视觉编码器具备因果推理能力、按图像语义动态重排视觉 token，打破固定光栅扫描顺序。

## 摘要
DeepSeek-OCR 2（arXiv 2026-01-28，作者 Haoran Wei、Yaofeng Sun、Yukun Li）研究一种能按图像语义动态重排视觉 token 的新型编码器 DeepEncoder V2。传统 VLM 总是以固定光栅扫描顺序（左上到右下）+ 固定位置编码处理视觉 token，这与人类视觉感知相悖——人类视觉遵循灵活但语义连贯的扫描模式，尤其对复杂版面会做因果信息驱动的顺序处理。受此认知机制启发，DeepEncoder V2 让编码器具备因果推理能力，在送入 LLM 前智能重排视觉 token。该工作探索新范式：2D 图像理解能否被建模为视觉因果流（Visual Causal Flow）。承接 DeepSeek-OCR（arXiv 2025-10，Contexts Optical Compression）。

## 关键技术细节
- **核心-DeepEncoder V2**：视觉编码器具备因果推理能力，按图像语义动态重排视觉 token。
- **打破固定顺序**：传统 VLM 固定 raster-scan（左上→右下）+ 固定位置编码；DeepEncoder V2 按语义重排。
- **动机**：复杂版面下人类视觉做因果信息驱动的顺序处理。
- **范式-Visual Causal Flow**：探索把 2D 图像理解建模为视觉因果流。
- **承接**：DeepSeek-OCR（2025-10，Contexts Optical Compression）的第二代。
- **作者**：Haoran Wei 等（DeepSeek-OCR 系列原作者）。

## 原始链接
- url: https://arxiv.org/abs/2601.20552
- pdf_url: https://arxiv.org/pdf/2601.20552
- github_url: https://github.com/deepseek-ai/DeepSeek-OCR

## 本地落盘文件
- ../../../sources/llm/2026/deepseek-ocr-2.pdf
