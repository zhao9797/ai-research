---
title: "The Llama 4 herd: the beginning of a new era of natively multimodal AI innovation"
org: Meta AI
country: US
date: 2025-04
type: blog
categories: [架构, 预训练数据]
url: https://ai.meta.com/blog/llama-4-multimodal-intelligence/
downloaded: [llama4-blog.html]
---

## 一句话定位
Llama 4 是 Meta 首个原生多模态 MoE 模型族：Scout（17B 激活/16 专家/10M 上下文）、Maverick（17B 激活/128 专家）、Behemoth（288B 激活/16 专家，教师模型），采用早融合 + iRoPE。

## 摘要（3-6 句）
Llama 4 是 Meta 第一代原生多模态、采用 Mixture-of-Experts (MoE) 架构的开源模型。官方发布 Llama 4 Scout 和 Llama 4 Maverick，并预览仍在训练的 Llama 4 Behemoth（作为前两者的「教师」做 codistillation）。Scout 是同级最佳多模态模型，10M token 上下文；Maverick 在广泛基准上击败 GPT-4o 和 Gemini 2.0 Flash，性价比领先（实验性聊天版 LMArena ELO 1417）。Llama 4 用早融合 (early fusion) 把文本与视觉 token 统一进单一骨干。

## 关键技术细节
- Llama 4 Scout：17B 激活参数、16 专家；支持业界领先的 10M token 上下文窗口；可单张 H100（Int4 量化）部署。
- Llama 4 Maverick：17B 激活参数、128 专家（更多但更小专家）；多模态对标 GPT-4o / Gemini 2.0 Flash；性价比突出。
- Llama 4 Behemoth：288B 激活参数、16 专家（约 2T 总参级），作为教师模型，多个 STEM 基准超过 GPT-4.5 / Claude Sonnet 3.7 / Gemini 2.0 Pro。
- 原生多模态：early fusion，文本 + 视觉 token 共用统一 backbone 联合预训练。
- iRoPE：interleaved attention（交错的注意力层，部分层不用位置编码 NoPE）+ RoPE，目标支持「近无限」上下文长度。
- MoE：每 token 选少量专家激活，总参远大于激活参数，提升训练/推理效率。

## 原始链接
- url: https://ai.meta.com/blog/llama-4-multimodal-intelligence/

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/llama4-blog.html
