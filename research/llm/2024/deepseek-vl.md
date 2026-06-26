---
title: "DeepSeek-VL: Towards Real-World Vision-Language Understanding"
org: DeepSeek-AI
country: 中国
date: 2024-03
type: arxiv
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2403.05525
pdf_url: https://arxiv.org/pdf/2403.05525
github_url: https://github.com/deepseek-ai/DeepSeek-VL
downloaded: [files/deepseek-vl.pdf]
---

## 一句话定位
DeepSeek 第一代开源视觉语言模型，强调真实世界场景数据构建与混合视觉编码器（SigLIP + SAM-B）。

## 摘要
DeepSeek-VL 面向真实世界视觉语言理解，围绕三个维度构建：数据（覆盖网页截图、PDF、OCR、图表、专家知识与教材）、模型架构（混合视觉编码器，高效处理 1024×1024 高分辨率）、训练策略（从语言模型出发联合训练，避免视觉训练损害语言能力）。提供 1.3B 与 7B 两档。

## 关键技术细节（带数字）
- 规模：1.3B 与 7B；语言侧基于 DeepSeek-LLM。
- 视觉编码：hybrid vision encoder（SigLIP-L 语义 + SAM-B 高分辨细节），支持 1024×1024。
- 数据：真实场景导向（web 截图、PDF、OCR、图表、教材/专家知识）；并从真实用户场景构造 use-case taxonomy 做指令微调。
- 训练策略：联合视觉-语言预训练，保持语言能力的训练配方。

## 原始链接
- arXiv: https://arxiv.org/abs/2403.05525
- PDF: https://arxiv.org/pdf/2403.05525
- GitHub: https://github.com/deepseek-ai/DeepSeek-VL

## 一手源存档（sources/）
- deepseek-vl.pdf  （PDF 不入 git，走 HF bucket）
