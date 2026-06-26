---
title: "MiniCPM3-4B (Model Card)"
org: 面壁智能 (ModelBest) / OpenBMB
country: 中国
date: 2024-09
type: model-card
categories: [架构, 后训练]
url: https://huggingface.co/openbmb/MiniCPM3-4B
pdf_url:
github_url: https://github.com/OpenBMB/MiniCPM
downloaded: [files/minicpm3-hf-readme.md]
---

## 一句话定位
面壁第三代端侧基座 MiniCPM3-4B，整体能力超越 Phi-3.5-mini 与多数 7B-9B 模型，引入 MLA 压 KV cache，原生支持函数调用与代码解释器。

## 摘要
MiniCPM3-4B 是 MiniCPM 系列第三代，整体性能超越 Phi-3.5-mini-Instruct 与 GPT-3.5-Turbo-0125，并与多个 7B–9B 模型相当。支持 32K 上下文（配合 LLMxMapReduce 理论可处理无限上下文），具备函数调用（function calling）与代码解释器能力。

## 关键技术细节（带数字）
- 规模：4B 参数。
- 上下文：32K（配合 LLMxMapReduce 理论可处理无限长文，无需巨量显存）。
- 能力：原生 function calling + 代码解释器（agent / tool use）。
- 性能：综合超越 Phi-3.5-mini-Instruct、GPT-3.5-Turbo-0125，比肩 7B-9B 模型。

## 原始链接
- HF model card: https://huggingface.co/openbmb/MiniCPM3-4B
- GitHub: https://github.com/OpenBMB/MiniCPM

## 一手源存档（sources/）
- [minicpm3-hf-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/minicpm3-hf-readme.md)
