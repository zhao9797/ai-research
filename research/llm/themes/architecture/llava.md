---
title: "Visual Instruction Tuning (LLaVA)"
org: University of Wisconsin–Madison / Microsoft Research / Columbia University
country: US
date: 2023-04
type: paper
categories: [架构, 后训练]
url: https://arxiv.org/abs/2304.08485
pdf_url: https://arxiv.org/pdf/2304.08485
github_url: https://github.com/haotian-liu/LLaVA
downloaded: [llava.pdf]
---

## 一句话定位
LLaVA 用一个简单的线性/MLP 投影把 CLIP 视觉特征接到 LLM，并首创用纯文本 GPT-4 生成多模态指令数据做视觉指令微调，是最具影响力的开源 VLM 范式。

## 摘要（3-6 句）
指令微调能提升 LLM 的零样本能力，但多模态领域少有探索。LLaVA 首次用纯语言的 GPT-4 生成图文指令跟随数据，再用这些数据做视觉指令微调，得到端到端训练的大型多模态模型——把视觉编码器和 LLM 用投影层相连。架构极简：CLIP ViT 视觉特征经一个投影矩阵（后续版本用 MLP）映射到 LLM 词嵌入空间。LLaVA 在多模态对话上表现出接近 GPT-4 的行为，并在科学问答等基准上 SOTA。

## 关键技术细节
- 架构：冻结/可调 CLIP ViT-L/14 视觉编码器 + 投影层（v1 线性、v1.5 改 MLP）+ Vicuna/LLaMA LLM。
- 数据：用 GPT-4（纯文本）从 COCO 标注/框生成约 158K 视觉指令样本（对话、细节描述、复杂推理）。
- 两阶段训练：① 特征对齐预训练（只训投影层）；② 端到端指令微调（投影层 + LLM）。
- 结果：多模态对话接近 GPT-4 相对分数；ScienceQA 等 SOTA。
- 影响：LLaVA「ViT+投影+LLM+指令微调」成为开源 VLM 的主流配方。

## 原始链接
- url: https://arxiv.org/abs/2304.08485
- pdf_url: https://arxiv.org/pdf/2304.08485
- github_url: https://github.com/haotian-liu/LLaVA

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/llava.pdf
