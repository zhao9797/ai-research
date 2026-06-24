---
title: "Expanding Performance Boundaries of Open-Source Multimodal Models with Model, Data, and Test-Time Scaling (InternVL 2.5)"
org: 上海人工智能实验室 (Shanghai AI Laboratory) / OpenGVLab
country: 中国
date: 2024-12
type: arxiv
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2412.05271
pdf_url: https://arxiv.org/pdf/2412.05271
github_url: https://github.com/OpenGVLab/InternVL
downloaded: [files/internvl-2-5.pdf]
---

## 一句话定位
InternVL 2.5——延续 InternVL 1.5/2.0 架构，从模型、数据、测试时扩展三方面提升，78B 版成为首个 MMMU 超 70 的开源多模态模型。

## 摘要
InternVL 2.5 沿用 InternVL 2.0 的 "ViT-MLP-LLM" 架构，系统性探索模型规模、数据质量与测试时扩展（test-time scaling，如 CoT + 多数投票）。InternVL2.5-78B 在 MMMU 上突破 70%（CoT 下），成为首个达到该水平的开源 MLLM，整体性能比肩 GPT-4o、Claude-3.5-Sonnet。

## 关键技术细节（带数字）
- 规模谱系：1B / 2B / 4B / 8B / 26B / 38B / 78B（ViT-MLP-LLM）。
- 视觉编码器：InternViT-300M / InternViT-6B。
- 语言侧：Qwen2.5 与 InternLM2.5 系列。
- 测试时扩展：CoT + Majority Voting 进一步提升（78B MMMU 突破 70%）。
- 数据：强调数据质量过滤（去除异常样本）、多模态数据配方。
- 性能：InternVL2.5-78B 比肩 GPT-4o / Claude-3.5-Sonnet，OCR/文档/多学科推理领先开源。

## 原始链接
- arXiv: https://arxiv.org/abs/2412.05271
- PDF: https://arxiv.org/pdf/2412.05271
- GitHub: https://github.com/OpenGVLab/InternVL

## 本地落盘文件
- ../../../sources/llm/2024/internvl-2-5.pdf
