---
title: "Gemma: Open Models Based on Gemini Research and Technology"
org: Google DeepMind
country: US
date: 2024-03
type: report
categories: [架构, 后训练]
url: https://arxiv.org/abs/2403.08295
pdf_url: https://arxiv.org/pdf/2403.08295
github_url:
downloaded: [2403.08295.pdf]
---

## 一句话定位
Gemma 技术报告：基于 Gemini 研究的轻量开放模型（2B、7B），含预训练与微调权重。

## 摘要
Gemma 是源自 Gemini 研究与技术的轻量 SOTA 开放模型族，在语言理解、推理、安全等学术基准上表现强劲。发布 2B 与 7B 两档，提供预训练与微调检查点。Gemma 在 18 个文本任务中的 11 个上超过同规模开放模型，并给出全面的安全与责任评估及详细的模型开发说明。

## 关键技术细节
- 规模：2B 与 7B（论文称约 2B/7B）；decoder-only Transformer。
- 训练 token：7B 训 6T token，2B 训 2T token（公开英文网页/数学/代码）。
- 架构特性：RoPE、GeGLU 激活、RMSNorm；7B 用 multi-head attention，2B 用 multi-query attention；词表 256K（SentencePiece）。
- 后训练：SFT + RLHF。
- 评测：18 项文本任务中 11 项超同规模开放模型。

## 原始链接
- url: https://arxiv.org/abs/2403.08295
- pdf_url: https://arxiv.org/pdf/2403.08295

## 本地落盘文件
- ../../../sources/llm/2024/2403.08295.pdf
