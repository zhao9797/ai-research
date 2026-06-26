---
title: "Qwen2.5-Omni Technical Report"
org: Qwen Team, Alibaba Group
country: China
date: 2025-03
type: report
categories: [架构]
url: https://arxiv.org/abs/2503.20215
pdf_url: https://arxiv.org/pdf/2503.20215
github_url: https://github.com/QwenLM/Qwen2.5-Omni
downloaded: [qwen2.5-omni.pdf]
---

## 一句话定位
Qwen2.5-Omni 是端到端原生全模态（omni）模型：单模型感知文本/图像/音频/视频，并以流式方式同时生成文本与自然语音；核心创新是 Thinker-Talker 双脑架构 + TMRoPE（时间对齐多模态 RoPE），代表「native omni-modal」路线。

## 摘要（3-6 句）
Qwen2.5-Omni 是端到端多模态模型，可感知文本、图像、音频、视频多种模态，并以流式方式同时生成文本与自然语音。为支持多模态输入流式处理，音频与视觉编码器均采用 block-wise 分块处理，解耦长序列感知与生成。为同步视频与音频时间戳，将二者按时间交错排列，并提出 TMRoPE（Time-aligned Multimodal RoPE）位置编码。为并发生成文本与语音又互不干扰，提出 Thinker-Talker 架构：Thinker 是负责文本生成的 LLM，Talker 是双轨自回归模型，直接利用 Thinker 的隐表示产出音频 token；二者端到端训练与推理。流式音频解码用 sliding-window DiT 限制感受野以降低首包延迟。性能介于 Qwen2-7B 与 Qwen2.5-7B 之间，并在 Omni-Bench 等多模态基准达 SOTA；端到端语音指令跟随能力（MMLU、GSM8K）逼近其文本输入能力。

## 关键技术细节
- 规模档位：Qwen2.5-Omni-7B 与 3B；7B 整体性能介于 Qwen2-7B 与 Qwen2.5-7B 之间。
- 视觉编码器：复用 Qwen2.5-VL 的 ViT（约 675M 参数），处理图像与视频。
- 音频编码器：用 Qwen2-Audio 编码器、以 Whisper-large-v3 初始化；mel 频谱窗长 25ms、hop 10ms，每帧约对应原始音频 40ms。
- 两编码器在固定 LLM 上分别训练，各自先聚焦自身模态对齐。
- TMRoPE：把音视频按实际时间每 2 秒切块、视觉在前音频在后交错排列，位置编码与绝对时间戳对齐。
- Thinker-Talker：Thinker 为 Transformer 解码器（带音频/图像编码器）做文本生成；Talker 为双轨自回归模型，直接吃 Thinker 隐表示流式输出离散语音 token。
- 语音 codec：自研 qwen-tts-tokenizer，高效表示语音关键信息并可流式解码回语音。
- 流式语音解码：sliding-window DiT 限制感受野，降低初始包延迟。
- 性能：Omni-Bench 等多模态基准 SOTA；语音生成的流式 Talker 在鲁棒性与自然度上超过多数流式/非流式方案；端到端语音指令跟随逼近文本输入。

## 原始链接
- url: https://arxiv.org/abs/2503.20215
- pdf_url: https://arxiv.org/pdf/2503.20215
- github_url: https://github.com/QwenLM/Qwen2.5-Omni

## 一手源存档（sources/）
- qwen2.5-omni.pdf  （PDF 不入 git，走 HF bucket）
