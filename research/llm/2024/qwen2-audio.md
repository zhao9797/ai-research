---
title: "Qwen2-Audio Technical Report"
org: 阿里巴巴 Qwen Team
country: 中国
date: 2024-07
type: arxiv
categories: [架构, 后训练]
url: https://arxiv.org/abs/2407.10759
pdf_url: https://arxiv.org/pdf/2407.10759
github_url: https://github.com/QwenLM/Qwen2-Audio
downloaded: [files/qwen2-audio.pdf]
---

## 一句话定位
通义千问音频语言模型，用自然语言 prompt 简化预训练，支持"语音聊天"与"音频分析"两种交互模式。

## 摘要
Qwen2-Audio 接受多种音频信号输入，能做音频分析或对语音指令直接给出文本回答。相比复杂的层级标签，改用自然语言 prompt 统一不同数据与任务，并扩大数据量；增强指令跟随，提供两种模式：voice chat（自由语音交互，无需文字输入）与 audio analysis（音频分析）。后训练用 SFT + DPO。

## 关键技术细节（带数字）
- 架构：音频编码器（基于 Whisper-large-v3）+ Qwen 大语言模型。
- 预训练：用自然语言 prompt 统一任务（替代层级标签），扩大音频-文本数据规模。
- 交互模式：voice chat + audio analysis。
- 后训练：SFT + DPO（直接偏好优化）对齐人类偏好。
- 能力：语音/自然声音/音乐多类型音频理解，多基准 SOTA。

## 原始链接
- arXiv: https://arxiv.org/abs/2407.10759
- PDF: https://arxiv.org/pdf/2407.10759
- GitHub: https://github.com/QwenLM/Qwen2-Audio

## 一手源存档（sources/）
- qwen2-audio.pdf  （PDF 不入 git，走 HF bucket）
