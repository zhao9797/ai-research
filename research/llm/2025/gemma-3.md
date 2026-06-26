---
title: Gemma 3 Technical Report
org: Google DeepMind
country: US
date: 2025-03
type: technical-report
categories: [架构, 后训练, 预训练数据]
url: https://arxiv.org/abs/2503.19786
pdf_url: https://arxiv.org/pdf/2503.19786
github_url:
downloaded: [files/gemma-3-report.pdf]
---

## 一句话定位
Google DeepMind 2025-03-12 的 Gemma 3 开放模型技术报告：1B–27B 轻量多模态模型，新增视觉理解、128K+ 长上下文，并通过提高 local:global 注意力比来抑制长上下文 KV-cache 爆炸。

## 摘要
Gemma 3 在 Gemma 家族中新增多模态（视觉）、更广语言覆盖与更长上下文（≥128K）。架构关键变化是提高局部注意力层与全局注意力层之比、并缩短局部注意力跨度，显著降低长上下文 KV-cache 内存。训练采用蒸馏，配合新的 post-training 配方提升数学/对话/指令遵循/多语言。Gemma3-4B-IT 媲美 Gemma2-27B-IT，Gemma3-27B-IT 媲美 Gemini-1.5-Pro。

## 关键技术细节（带数字）
- 规模：1B、4B、12B、27B 四档（新增 1B）；面向手机/笔记本/高端 GPU 等消费级硬件。
- 多模态：新增视觉理解（视觉编码器）；从纯文本扩展到图文。
- 上下文：≥128K tokens。
- 架构：提高 local:global 注意力层比例（每若干 local 层配 1 global 层），缩短 local attention 跨度，抑制长上下文 KV-cache 内存膨胀。
- 训练：知识蒸馏（distillation）训练；新 post-training 配方提升 math/chat/instruction-following/multilingual。
- 效果：Gemma3-4B-IT ≈ Gemma2-27B-IT；Gemma3-27B-IT ≈ Gemini-1.5-Pro（跨基准）。
- 全部模型开放发布。发布日期 2025-03-12。
- DeepMind 官方 PDF：https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf

## 原始链接
- arXiv：https://arxiv.org/abs/2503.19786
- PDF：https://arxiv.org/pdf/2503.19786
- DeepMind 官方 PDF：https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf

## 一手源存档（sources/）
- gemma-3-report.pdf  （PDF 不入 git，走 HF bucket）
