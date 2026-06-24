---
title: Qwen2.5-Omni Technical Report
org: 阿里巴巴 Qwen Team
country: China
date: 2025-03
type: paper
categories: [架构, 后训练]
url: https://arxiv.org/abs/2503.20215
pdf_url: https://arxiv.org/pdf/2503.20215
github_url: https://github.com/QwenLM/Qwen2.5-Omni
downloaded: [qwen2.5-omni.pdf]
---

## 一句话定位
端到端全模态模型：同时感知文本/图像/音频/视频并流式生成文本与自然语音，提出 Thinker-Talker 架构与 TMRoPE 时间对齐位置编码。发布 2025-03-26。

## 摘要
Qwen2.5-Omni 是端到端多模态模型，可感知文本、图像、音频、视频，并以流式方式同时生成文本与自然语音。为支持多模态流式输入，音频与视觉编码器采用 block-wise 分块处理；为对齐视频与音频时间戳，提出 TMRoPE（Time-aligned Multimodal RoPE）。为在生成文本与语音时避免两种模态相互干扰，提出 Thinker-Talker 架构（Thinker 生成文本，Talker 自回归生成语音 token）。

## 关键技术细节
- 架构：Thinker-Talker——Thinker（LLM）产出文本与高层语义表示，Talker（双轨自回归 Transformer）流式生成语音 token。
- TMRoPE：时间对齐多模态旋转位置编码，音视频按时间交错排列对齐时间戳。
- 流式：音频/视觉编码器 block-wise 处理，支持实时流式输入输出。
- 模态：文本、图像、音频、视频输入；文本 + 自然语音输出。
- 开源：HuggingFace / GitHub（Qwen2.5-Omni-7B 等）。

## 原始链接
- url: https://arxiv.org/abs/2503.20215
- pdf_url: https://arxiv.org/pdf/2503.20215
- github_url: https://github.com/QwenLM/Qwen2.5-Omni

## 本地落盘文件
- ../../../sources/llm/2025/qwen2.5-omni.pdf
