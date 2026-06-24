---
title: "Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond"
org: Qwen Team, Alibaba Group
country: China
date: 2023-08
type: paper
categories: [架构]
url: https://arxiv.org/abs/2308.12966
pdf_url: https://arxiv.org/pdf/2308.12966
github_url: https://github.com/QwenLM/Qwen-VL
downloaded: [qwen-vl.pdf]
---

## 一句话定位
Qwen-VL 是 Qwen 系列首个视觉语言模型：以 Qwen-7B 为基座，接 OpenCLIP ViT-bigG 视觉编码器和一个「位置感知」单层 cross-attention 适配器（压缩到 256 视觉 token），通过 3 阶段训练赋予 LLM 看图、定位（grounding）、读字（OCR）能力，是 Qwen2-VL / Qwen2.5-VL 的起点。

## 摘要（3-6 句）
Qwen-VL 系列是一组大规模视觉语言模型（LVLM），以 Qwen-LM 为基座、通过精心设计的 (i) 视觉感受器、(ii) 输入输出接口、(iii) 三阶段训练流程、(iv) 多语言多模态清洗语料赋予其视觉能力。除常规图像描述与问答外，通过对齐「图像-描述-框」三元组实现 grounding 与文字阅读能力。最终的 Qwen-VL 与指令微调版 Qwen-VL-Chat 在同规模通用模型中于一系列视觉中心基准（caption、VQA、visual grounding）和多种设定（zero-shot、few-shot）上刷新记录；在真实对话基准上 Qwen-VL-Chat 优于现有视觉对话机器人。

## 关键技术细节
- 参数构成：总计 9.6B = 视觉编码器 1.9B（OpenCLIP ViT-bigG）+ VL 适配器 0.08B + LLM 7.7B（Qwen-7B 基座）。
- 视觉编码器：ViT 架构，用 OpenCLIP ViT-bigG 预训练权重初始化；输入分辨率从 224×224 提升到 448×448 以减少图像下采样信息损失。
- 位置感知 VL 适配器：单层随机初始化的 cross-attention，用一组可训练向量作 query、视觉特征作 key，将变长视觉特征压缩到固定 256 个 token；引入位置编码缓解压缩中的位置信息丢失。两个特殊 token 区分图像/文本输入边界。
- 3 阶段训练流程：Stage 1 图文对预训练（冻结 LLM）；Stage 2 多任务预训练（更大分辨率 + 交错图文 + 细粒度 VL 标注，含 grounding/OCR）；Stage 3 指令微调得到 Qwen-VL-Chat。
- 预训练数据：原始 5B 图文对，清洗后保留 1.4B；语言分布 77.3% 英文 / 22.7% 中文。
- 能力亮点：细粒度视觉理解、边界框 grounding、文字阅读（OCR），多语言。
- 代码与模型开源（含 Qwen-VL、Qwen-VL-Chat）。

## 原始链接
- url: https://arxiv.org/abs/2308.12966
- pdf_url: https://arxiv.org/pdf/2308.12966
- github_url: https://github.com/QwenLM/Qwen-VL

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/qwen-vl.pdf
