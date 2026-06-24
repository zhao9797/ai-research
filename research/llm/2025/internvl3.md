---
title: "InternVL3: Exploring Advanced Training and Test-Time Recipes for Open-Source Multimodal Models"
org: 上海人工智能实验室 (Shanghai AI Lab) / OpenGVLab
country: China
date: 2025-04
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2504.10479
pdf_url: https://arxiv.org/pdf/2504.10479
github_url: https://github.com/OpenGVLab/InternVL
downloaded: [internvl3.pdf]
---

## 一句话定位
上海 AI Lab/OpenGVLab 的 InternVL3，原生多模态预训练范式：在单一预训练阶段同时从多模态与纯文本语料联合习得语言与多模态能力，免去文本 LLM 事后改造为 MLLM 的对齐难题。发布 2025-04-14。

## 摘要
InternVL3 是 InternVL 系列的重要进展，采用 native multimodal pre-training 范式：不再把纯文本 LLM 事后改造为支持视觉输入的 MLLM，而是在单一预训练阶段从多样多模态数据与纯文本语料联合习得多模态与语言能力，有效解决传统事后训练 pipeline 的复杂性与对齐挑战。结合 variable visual position encoding、先进后训练（SFT + MPO）与 test-time scaling，InternVL3 在 MMMU 等 benchmark 上达开源 MLLM 顶尖水平。

## 关键技术细节
- 训练范式：native multimodal pre-training，多模态 + 纯文本单阶段联合预训练。
- 位置编码：V2PE（Variable Visual Position Encoding）支持更长多模态上下文。
- 后训练：监督微调 + Mixed Preference Optimization (MPO) + test-time scaling（如 best-of-N）。
- 模型规模：1B–78B 多档（基于 InternViT + Qwen2.5 等 LLM 基座）。
- 成绩：开源 MLLM 顶尖（MMMU 等），缩小与闭源差距。
- 开源：GitHub OpenGVLab/InternVL。

## 原始链接
- url: https://arxiv.org/abs/2504.10479
- pdf_url: https://arxiv.org/pdf/2504.10479
- github_url: https://github.com/OpenGVLab/InternVL

## 本地落盘文件
- ../../../sources/llm/2025/internvl3.pdf
