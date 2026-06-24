---
title: "DeepSeek-VL2: Mixture-of-Experts Vision-Language Models for Advanced Multimodal Understanding"
org: DeepSeek-AI
country: 中国
date: 2024-12
type: arxiv
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2412.10302
pdf_url: https://arxiv.org/pdf/2412.10302
github_url: https://github.com/deepseek-ai/DeepSeek-VL2
downloaded: [files/deepseek-vl2.pdf]
---

## 一句话定位
DeepSeek-VL 的 MoE 升级版：动态分块视觉编码 + DeepSeekMoE(MLA) 语言侧，三档（Tiny/Small/标准）激活 1.0B/2.8B/4.5B。

## 摘要
DeepSeek-VL2 相比 DeepSeek-VL 有两大升级：视觉侧采用 dynamic tiling 视觉编码策略，处理不同宽高比的高分辨率图像；语言侧采用带 MLA 的 DeepSeekMoE 模型，把 KV cache 压成 latent 向量以高效推理。在改进的视觉-语言数据集上训练，多模态理解能力显著提升。

## 关键技术细节（带数字）
- 三档（激活参数）：DeepSeek-VL2-Tiny 1.0B、DeepSeek-VL2-Small 2.8B、DeepSeek-VL2 4.5B 激活。
- 语言侧：DeepSeekMoE + MLA（KV 压缩为 latent）。
- 视觉编码：dynamic tiling，适配任意宽高比高分辨率图像。
- 训练数据：改进的视觉-语言数据集，多模态理解 SOTA（同激活规模下）。

## 原始链接
- arXiv: https://arxiv.org/abs/2412.10302
- PDF: https://arxiv.org/pdf/2412.10302
- GitHub: https://github.com/deepseek-ai/DeepSeek-VL2

## 本地落盘文件
- ../../../sources/llm/2024/deepseek-vl2.pdf
