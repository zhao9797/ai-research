---
title: Phi-4-Mini Technical Report (Phi-4-Mini & Phi-4-Multimodal)
org: Microsoft
country: US
date: 2025-03
type: technical-report
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2503.01743
pdf_url: https://arxiv.org/pdf/2503.01743
github_url:
downloaded: [files/phi-4-mini.pdf]
---

## 一句话定位
Microsoft 2025-03 的 Phi-4-Mini 技术报告：3.8B 紧凑语言模型 + Phi-4-Multimodal，后者用 Mixture-of-LoRAs 把文本/视觉/语音三模态融入单一模型而互不干扰。

## 摘要
Phi-4-Mini 是 3.8B 模型，靠高质量 web + 合成数据（强调数学/编码），在数学/编码上媲美两倍大小模型。相较 Phi-3.5-Mini，词表扩到 200K 支持多语言，并用 GQA 提升长序列生成效率。Phi-4-Multimodal 用 LoRA 适配器 + 模态特定 router 把文本/视觉/语音整合进单模型，多种推理模式互不干扰，语音 LoRA 仅 4.6 亿参数即登顶 OpenASR 榜。

## 关键技术细节（带数字）
- Phi-4-Mini：3.8B 参数；训练于高质量 web + 合成数据（侧重 math/coding）。
- 词表：扩展到 200K tokens（支持多语言）；采用 group query attention（GQA）提升长序列生成效率。
- Phi-4-Multimodal：Mixture-of-LoRAs——LoRA 适配器 + modality-specific routers，整合 text/vision/speech-audio 到单模型，多模态推理互不干扰。
- 语音：speech/audio LoRA 仅 460M 参数即在 OpenASR leaderboard 居首。
- 支持组合：(vision+language)、(vision+speech)、(speech/audio) 等。
- 发布日期：2025-03（arXiv:2503.01743）。

## 原始链接
- arXiv：https://arxiv.org/abs/2503.01743
- PDF：https://arxiv.org/pdf/2503.01743

## 本地落盘文件
- ../../../sources/llm/2025/phi-4-mini.pdf
