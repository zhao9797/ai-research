---
title: "CogVLM2: Visual Language Models for Image and Video Understanding"
org: 智谱 AI (Zhipu AI) / 清华大学
country: 中国
date: 2024-08
type: arxiv
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2408.16500
pdf_url: https://arxiv.org/pdf/2408.16500
github_url: https://github.com/THUDM/CogVLM2
downloaded: [files/cogvlm2.pdf]
---

## 一句话定位
智谱新一代视觉语言模型家族（CogVLM2 / CogVLM2-Video / GLM-4V），延续 visual expert 架构，支持 1344×1344 高分辨率与视频理解。

## 摘要
继 VisualGLM、CogVLM 之后，CogVLM2 家族面向图像与视频理解，包括 CogVLM2、CogVLM2-Video 与 GLM-4V。图像模型继承 visual expert 架构并改进预训练/后训练配方，输入分辨率最高 1344×1344；视频模型 CogVLM2-Video 用多帧 + 时间戳实现时序定位与视频问答。

## 关键技术细节（带数字）
- 家族：CogVLM2（图像）、CogVLM2-Video（视频）、GLM-4V。
- 架构：visual expert（在每个 Transformer 层加视觉专家 QKV/FFN，与语言权重并行）。
- 分辨率：输入最高 1344×1344。
- 视频：多帧采样 + 时间戳，支持时序定位/视频问答。
- 基准：图像在 OCRBench/TextVQA/DocVQA，视频在 MVBench/VideoMME 等达开源先进水平。

## 原始链接
- arXiv: https://arxiv.org/abs/2408.16500
- PDF: https://arxiv.org/pdf/2408.16500
- GitHub: https://github.com/THUDM/CogVLM2

## 一手源存档（sources/）
- cogvlm2.pdf  （PDF 不入 git，走 HF bucket）
