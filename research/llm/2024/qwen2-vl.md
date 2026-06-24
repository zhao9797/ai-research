---
title: "Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution"
org: 阿里巴巴 Qwen Team
country: 中国
date: 2024-09
type: arxiv
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2409.12191
pdf_url: https://arxiv.org/pdf/2409.12191
github_url: https://github.com/QwenLM/Qwen2-VL
downloaded: [files/qwen2-vl.pdf]
---

## 一句话定位
通义千问第二代视觉语言模型，提出 Naive Dynamic Resolution（任意分辨率→可变视觉 token）与多模态旋转位置编码 M-RoPE。

## 摘要
Qwen2-VL 重新定义"预设分辨率"做法：引入 Naive Dynamic Resolution 机制，可把不同分辨率图像动态处理为不同数量的视觉 token，更贴近人类感知；并集成 Multimodal Rotary Position Embedding（M-RoPE）融合文本/图像/视频的位置信息。提供 2B/7B/72B 三档。

## 关键技术细节（带数字）
- 规模：2B / 7B / 72B。
- 视觉编码：Naive Dynamic Resolution（任意分辨率 → 动态数量视觉 token），ViT 约 675M。
- 位置编码：M-RoPE（多模态旋转位置编码，分解时间/高/宽维度）。
- 视频：支持动态帧率与长视频理解。
- 性能：Qwen2-VL-72B 在 DocVQA/MathVista/MTVQA 等多基准达 SOTA，比肩 GPT-4o、Claude-3.5-Sonnet。

## 原始链接
- arXiv: https://arxiv.org/abs/2409.12191
- PDF: https://arxiv.org/pdf/2409.12191
- GitHub: https://github.com/QwenLM/Qwen2-VL

## 本地落盘文件
- ../../../sources/llm/2024/qwen2-vl.pdf
