---
title: "InternLM-XComposer: A Vision-Language Large Model for Advanced Text-image Comprehension and Composition"
org: 上海人工智能实验室（Shanghai AI Laboratory）
country: China
date: 2023-09
type: paper
categories: [架构, 后训练]
url: https://arxiv.org/abs/2309.15112
pdf_url: https://arxiv.org/pdf/2309.15112
github_url: https://github.com/InternLM/InternLM-XComposer
downloaded: [internlm-xcomposer.pdf]
---

## 一句话定位
书生·浦语-灵笔（InternLM-XComposer）：面向"图文交错理解与创作"的视觉语言大模型，可按写作指令自动生成配图文章，是上海 AI Lab 2023 多模态一手论文。

## 摘要（3-6 句）
InternLM-XComposer 是支持高级图文理解与创作的视觉语言大模型，具三大特性：(1) 图文交错创作——给定写作指令即生成图文连贯的文章，并智能判断在何处插入最合适的图像；(2) 富多语言知识的理解——基于多样训练与精心数据流程；(3) 强大的多模态对话能力。模型基于 InternLM 语言基座构建。

## 关键技术细节
- 基座：InternLM-7B 语言模型 + EVA-CLIP 视觉编码器 + Perceive Sampler（类 BLIP-2 的视觉采样器对齐）。
- 图文交错创作：模型自动在生成文本中选择插图位置，并从候选图库中检索/匹配最佳图像。
- 两阶段训练：视觉-语言预训练对齐 + 多任务监督微调（图文理解 + 创作 + 对话）。
- 多语言知识：中英双语图文理解，强调富知识对齐。
- 性能：在 MME、MMBench、SEED-Bench、CCBench 等多模态基准（含中文 CCBench）领先同期开源 VLM。
- 后续：InternLM-XComposer2（2024）进一步支持自由形式图文创作与 4K 高清。

## 原始链接
- url: https://arxiv.org/abs/2309.15112
- pdf_url: https://arxiv.org/pdf/2309.15112
- github_url: https://github.com/InternLM/InternLM-XComposer

## 本地落盘文件
- ../../../sources/llm/2023/internlm-xcomposer.pdf
