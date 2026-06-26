---
title: "Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond"
org: 阿里巴巴（Alibaba / Qwen Team）
country: China
date: 2023-08
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2308.12966
pdf_url: https://arxiv.org/pdf/2308.12966
github_url: https://github.com/QwenLM/Qwen-VL
downloaded: [qwen-vl.pdf]
---

## 一句话定位
基于 Qwen-LM 的视觉语言模型 Qwen-VL / Qwen-VL-Chat，新增视觉接收器与三阶段训练，支持 grounding 与文字识别，是阿里 2023 多模态一手论文。

## 摘要（3-6 句）
Qwen-VL 系列在 Qwen-LM 基座上，通过精心设计的视觉接收器、输入输出接口、三阶段训练流程与多语言多模态清洗语料，赋予其视觉理解能力。除常规图像描述与问答外，还通过对齐 image-caption-box 三元组实现 grounding 与文字阅读能力。Qwen-VL / Qwen-VL-Chat 在多项视觉中心基准上刷新同规模通才模型记录。

## 关键技术细节
- 基座：Qwen-7B 语言模型 + ViT 视觉编码器（OpenCLIP ViT-bigG 初始化）+ 位置感知的视觉-语言适配器（单层 cross-attention，压缩图像特征到 256 query）。
- 三阶段训练：① 视觉-语言预训练（冻结 LLM，仅训视觉编码器与适配器，大规模弱标注图文对）；② 多任务预训练（高分辨 448、grounding/OCR/VQA 等多任务，全参训练）；③ SFT/指令微调得 Qwen-VL-Chat。
- 能力：图像描述、VQA、视觉定位（grounding，box）、文档/文字阅读（OCR）、多图交错对话。
- 输入分辨率提升至 448×448（多数 LVLM 为 224）。
- 性能：在 Zero-shot Captioning、VQAv2、DocVQA、RefCOCO 等多基准上同规模 SOTA。

## 原始链接
- url: https://arxiv.org/abs/2308.12966
- pdf_url: https://arxiv.org/pdf/2308.12966
- github_url: https://github.com/QwenLM/Qwen-VL

## 一手源存档（sources/）
- qwen-vl.pdf  （PDF 不入 git，走 HF bucket）
