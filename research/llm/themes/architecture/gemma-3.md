---
title: "Gemma 3 Technical Report"
org: Google DeepMind
country: US
date: 2025-03
type: report
categories: [架构, 后训练]
url: https://arxiv.org/abs/2503.19786
pdf_url: https://arxiv.org/pdf/2503.19786
github_url: https://blog.google/technology/developers/gemma-3/
downloaded: [gemma3.pdf, gemma3-blog.html]
---

## 一句话定位
Gemma 3（1B–27B）给 Gemma 加上多模态、128K 上下文和更高比例的局部注意力（5:1 local:global）以压 KV cache，蒸馏训练，4B-IT 即可匹敌 Gemma2-27B-IT。

## 摘要（3-6 句）
Gemma 3 是 Gemma 家族的多模态扩展，规模 1B 到 27B，新增视觉理解、更广语言覆盖和至少 128K 的更长上下文。为应对长上下文下 KV cache 爆炸，架构提高了局部 vs 全局注意力层的比例并缩短局部注意力跨度。Gemma 3 用蒸馏训练，预训练与指令版均超过 Gemma 2。新的后训练配方显著提升数学、对话、指令遵循和多语言能力，使 Gemma3-4B-IT 媲美 Gemma2-27B-IT，Gemma3-27B-IT 在多基准上接近 Gemini-1.5-Pro。所有模型对社区发布。

## 关键技术细节
- 注意力：local:global = 5:1（每 5 层滑动窗口局部注意力配 1 层全局），局部窗口缩短（1024），大幅降低长上下文 KV 内存。
- 多模态：集成 SigLIP 视觉编码器（冻结），支持图像理解；4B/12B/27B 多模态，1B 纯文本。
- 上下文：128K（1B 为 32K）；用 RoPE base 频率缩放扩展长上下文。
- 规模：1B、4B、12B、27B；蒸馏训练（从更大教师）。
- 后训练：新配方（含 RL 类方法）提升数学/对话/指令/多语言；Gemma3-4B-IT ≈ Gemma2-27B-IT。
- 发布 2025-03-12，开放权重。

## 原始链接
- url: https://arxiv.org/abs/2503.19786
- pdf_url: https://arxiv.org/pdf/2503.19786
- github_url: https://blog.google/technology/developers/gemma-3/

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/gemma3.pdf
- ../../../../sources/llm/themes/architecture/gemma3-blog.html
