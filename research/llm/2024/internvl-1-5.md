---
title: "How Far Are We to GPT-4V? Closing the Gap to Commercial Multimodal Models with Open-Source Suites (InternVL 1.5)"
org: 上海人工智能实验室 (Shanghai AI Laboratory) / OpenGVLab
country: 中国
date: 2024-04
type: arxiv
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2404.16821
pdf_url: https://arxiv.org/pdf/2404.16821
github_url: https://github.com/OpenGVLab/InternVL
downloaded: [files/internvl-1-5.pdf]
---

## 一句话定位
InternVL 1.5——缩小开源与 GPT-4V 差距的开源多模态套件，三大改进：强视觉编码器 InternViT-6B、动态高分辨率、高质量双语数据集。

## 摘要
InternVL 1.5 通过三方面缩小与商用多模态模型差距：(1) 强视觉编码器——对 InternViT-6B 用连续学习策略提升视觉理解；(2) 动态高分辨率——按图像宽高比/分辨率切成 1–40 个 448×448 tile（最高约 4K 输入）；(3) 高质量双语数据集——覆盖常见场景、文档图像，标注中英问答。在多个基准上超越部分商用闭源模型。

## 关键技术细节（带数字）
- 视觉编码器：InternViT-6B（6B 参数，连续学习增强）。
- 语言侧：InternLM2-20B-Chat，整体约 26B。
- 动态分辨率：按宽高比切 1–40 个 448×448 tile（≈ 最高 4K 输入）。
- 数据：高质量中英双语数据集（自然场景 + 文档 OCR）。
- 性能：18 个多模态基准里 8 项达开源/商用最优区间，OCR/文档类强。

## 原始链接
- arXiv: https://arxiv.org/abs/2404.16821
- PDF: https://arxiv.org/pdf/2404.16821
- GitHub: https://github.com/OpenGVLab/InternVL

## 一手源存档（sources/）
- internvl-1-5.pdf  （PDF 不入 git，走 HF bucket）
