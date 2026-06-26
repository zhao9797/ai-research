---
title: "InternLM-XComposer2: Mastering Free-form Text-Image Composition and Comprehension in Vision-Language Large Model"
org: 上海人工智能实验室 (Shanghai AI Laboratory)
country: 中国
date: 2024-01
type: arxiv
categories: [架构, 后训练]
url: https://arxiv.org/abs/2401.16420
pdf_url: https://arxiv.org/pdf/2401.16420
github_url: https://github.com/InternLM/InternLM-XComposer
downloaded: [files/internlm-xcomposer2.pdf]
---

## 一句话定位
书生·浦语视觉版第二代，提出 Partial LoRA（仅在视觉 token 上加 LoRA）平衡多模态理解与纯文本能力，擅长自由形式图文创作。

## 摘要
InternLM-XComposer2 是擅长自由形式图文创作与理解的视觉语言大模型。核心创新 Partial LoRA（PLoRA）：仅对视觉 token 应用额外 LoRA 参数，保留预训练语言知识，在视觉理解与纯文本能力间取得平衡。基于 InternLM2-7B，能根据大纲、参考图文等灵活生成图文穿插内容。

## 关键技术细节（带数字）
- 基座：InternLM2-7B + CLIP ViT-L 视觉编码器。
- 核心：Partial LoRA（PLoRA）——仅在视觉 token 上加 LoRA，文本 token 走原权重。
- 任务：free-form 图文创作（按大纲/参考材料生成图文穿插长文）与图文理解。
- 性能：7B 量级在多模态理解基准上比肩甚至超过更大模型（如 GPT-4V、Gemini-Pro 部分项）。

## 原始链接
- arXiv: https://arxiv.org/abs/2401.16420
- PDF: https://arxiv.org/pdf/2401.16420
- GitHub: https://github.com/InternLM/InternLM-XComposer

## 一手源存档（sources/）
- internlm-xcomposer2.pdf  （PDF 不入 git，走 HF bucket）
