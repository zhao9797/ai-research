---
title: "Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution"
org: Qwen Team, Alibaba Group
country: China
date: 2024-09
type: report
categories: [架构]
url: https://arxiv.org/abs/2409.12191
pdf_url: https://arxiv.org/pdf/2409.12191
github_url: https://github.com/QwenLM/Qwen2-VL
downloaded: [qwen2-vl.pdf]
---

## 一句话定位
Qwen2-VL 引入 Naive Dynamic Resolution（任意分辨率→动态数量视觉 token）和 Multimodal RoPE (M-RoPE)，统一处理图像与视频，是中文阵营领先的开源 VLM。

## 摘要（3-6 句）
Qwen2-VL 是 Qwen-VL 的重大升级，摒弃固定分辨率方案。Naive Dynamic Resolution 让模型把不同分辨率图像动态映射成不同数量的视觉 token，更接近人类感知、表示更高效。M-RoPE（Multimodal Rotary Position Embedding）把位置信息分解为时间/高/宽多维，统一融合文本、图像、视频的位置。模型用统一范式处理图像与视频，提升视觉感知。Qwen2-VL 提供 2B/7B/72B 三档，72B 在多项多模态基准上达到或超过 GPT-4o、Claude-3.5-Sonnet。

## 关键技术细节
- Naive Dynamic Resolution：ViT 处理原生分辨率，动态生成可变数量视觉 token（相邻 patch 合并压缩）。
- M-RoPE：把 RoPE 拆成 temporal / height / width 三组，统一编码文本（1D）、图像（2D）、视频（3D）位置。
- 统一图像/视频处理范式；支持长视频理解。
- 规模：2B、7B、72B；72B 多模态基准对标并部分超越 GPT-4o、Claude-3.5-Sonnet。
- 视觉编码器约 675M ViT，跨尺度共享。

## 原始链接
- url: https://arxiv.org/abs/2409.12191
- pdf_url: https://arxiv.org/pdf/2409.12191
- github_url: https://github.com/QwenLM/Qwen2-VL

## 一手源存档（sources/）
- qwen2-vl.pdf  （PDF 不入 git，走 HF bucket）
