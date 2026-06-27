---
title: "DeepSeek-VL2: Mixture-of-Experts Vision-Language Models for Advanced Multimodal Understanding"
org: DeepSeek-AI
country: China
date: 2024-12
type: report
categories: [架构]
url: https://arxiv.org/abs/2412.10302
pdf_url: https://arxiv.org/pdf/2412.10302
github_url: https://github.com/deepseek-ai/DeepSeek-VL2
downloaded: [deepseek-vl2.pdf]
---

## 一句话定位
DeepSeek-VL2 把 MoE + MLA 的语言侧与「动态拼图」高分辨率视觉编码结合，做成稀疏激活的视觉语言 MoE 模型，高效处理高分辨率任意宽高比图像。

## 摘要（3-6 句）
DeepSeek-VL2 在前代 DeepSeek-VL 基础上两大升级：视觉侧采用 dynamic tiling（动态切片）编码策略，处理不同宽高比的高分辨率图像；语言侧用带 MLA 的 DeepSeekMoE，把 KV cache 压成潜向量以高效推理高吞吐。在改进的视觉语言数据集上训练，DeepSeek-VL2 在视觉问答、OCR、文档/表格/图表理解、视觉定位等任务上表现优异，且因稀疏激活而具竞争性的性能-算力比。

## 关键技术细节
- 视觉：dynamic tiling 高分辨率编码，把大图切成多块 + 全局缩略图，支持任意宽高比。
- 语言：DeepSeekMoE（细粒度专家 + 共享专家）+ MLA（KV cache 压缩为潜向量）。
- 规模档位：DeepSeek-VL2-Tiny/Small/（VL2），激活参数分别约 1.0B / 2.8B / 4.5B（MoE 稀疏激活）。
- 任务：VQA、OCR、文档/表格/图表理解、visual grounding，性能-激活参数比突出。

## 原始链接
- url: https://arxiv.org/abs/2412.10302
- pdf_url: https://arxiv.org/pdf/2412.10302
- github_url: https://github.com/deepseek-ai/DeepSeek-VL2

## 一手源存档（sources/）
- deepseek-vl2.pdf  （PDF 不入 git，走 HF bucket）
