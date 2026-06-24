---
title: "Molmo and PixMo: Open Weights and Open Data for State-of-the-Art Vision-Language Models"
org: Allen Institute for AI (AI2)
country: US
date: 2024-09
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2409.17146
pdf_url: https://arxiv.org/pdf/2409.17146
github_url: https://molmo.allenai.org/blog
downloaded: [2409.17146.pdf]
---

## 一句话定位
Molmo + PixMo：完全开放（权重 + 数据）的视觉语言模型，关键贡献是不依赖闭源 VLM 蒸馏、靠人工采集的高质量数据集（含创新的 2D pointing 数据）。

## 摘要
当下最强 VLM 仍闭源，最强开放权重模型也严重依赖从闭源 VLM 蒸馏的合成数据。社区因此缺乏"从零构建高性能 VLM"的基础知识。Molmo 是开放程度领先的新 VLM 家族，核心贡献是 PixMo 数据集：高细节图像描述（预训练）、自由形式图像问答（微调）、以及创新的 2D pointing 数据，全部不借助外部 VLM 采集。最佳的 72B 模型不仅在开放权重+数据类中领先，还超过 Claude 3.5 Sonnet、Gemini 1.5 Pro/Flash 等更大闭源模型，仅次于 GPT-4o（学术基准 + 大规模人评）。权重、数据、代码全部开放。

## 关键技术细节
- 架构：开放 LLM（OLMo/Qwen2）+ CLIP/SigLIP 视觉编码器 + connector。
- PixMo 数据：PixMo-Cap（语音描述转写得到的高细节 caption）、PixMo-AskModelAnything（问答）、PixMo-Points（2D 指向）。
- 不蒸馏闭源 VLM：所有数据靠人工/语音采集，避免对 GPT-4V 等的依赖。
- 规模：1B（OLMoE-based）、7B、72B。
- 性能：72B 超 Claude 3.5 Sonnet、Gemini 1.5 Pro/Flash，仅次于 GPT-4o。

## 原始链接
- url: https://arxiv.org/abs/2409.17146
- pdf_url: https://arxiv.org/pdf/2409.17146
- blog: https://molmo.allenai.org/blog

## 本地落盘文件
- ../../../sources/llm/2024/2409.17146.pdf
