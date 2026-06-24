---
title: "Qwen-Audio: Advancing Universal Audio Understanding via Unified Large-Scale Audio-Language Models"
org: 阿里巴巴（Alibaba / Qwen Team）
country: China
date: 2023-11
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2311.07919
pdf_url: https://arxiv.org/pdf/2311.07919
github_url: https://github.com/QwenLM/Qwen-Audio
downloaded: [qwen-audio.pdf]
---

## 一句话定位
阿里 Qwen-Audio：把音频-语言预训练扩到 30+ 任务与多种音频类型（语音/自然声/音乐/歌曲），用多任务统一框架解决任务干扰，是 2023 中国音频大模型一手论文。

## 摘要（3-6 句）
针对缺乏可处理多类音频与任务的预训练音频模型这一瓶颈，Qwen-Audio 将音频-语言预训练扩展到覆盖 30+ 任务、多种音频类型（人声、自然声、音乐、歌曲），以实现通用音频理解。为避免直接共训所有任务/数据集带来的干扰，作者设计了多任务训练框架（用分层标签的条件解码序列共享/区分知识）。在此基础上得到 Qwen-Audio-Chat，支持多轮音频与文本对话。

## 关键技术细节
- 架构：Qwen-7B 语言模型 + 音频编码器（Whisper-large-v2 初始化）。
- 多任务统一框架：用分层的标签序列（hierarchical tags）作为解码条件，区分共享知识与任务特定知识，缓解任务/数据集间干扰。
- 覆盖 30+ 音频任务：ASR、语音翻译、声音/场景识别、音乐/乐器/情绪分析等。
- 不需任务特定微调即可在多基准达 SOTA（如 Aishell-1、AISHELL-2、各语音翻译/分类基准）。
- Qwen-Audio-Chat：经指令微调，支持多轮、多音频输入的语音+文本对话。

## 原始链接
- url: https://arxiv.org/abs/2311.07919
- pdf_url: https://arxiv.org/pdf/2311.07919
- github_url: https://github.com/QwenLM/Qwen-Audio

## 本地落盘文件
- ../../../sources/llm/2023/qwen-audio.pdf
