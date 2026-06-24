---
title: Gemini: A Family of Highly Capable Multimodal Models
org: Google DeepMind
country: US
date: 2023-12
type: report
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2312.11805
pdf_url: https://arxiv.org/pdf/2312.11805
downloaded: [gemini.pdf]
---

## 一句话定位
Google DeepMind 原生多模态旗舰，首个 MMLU 超人类专家的模型，Ultra/Pro/Nano 三档覆盖云到端。

## 摘要
Gemini 系列在图像、音频、视频、文本理解上能力突出，分 Ultra/Pro/Nano 三种规模。最强的 Gemini Ultra 在 32 个基准中 30 个刷新 SOTA，是首个在 MMLU 上达到人类专家水平的模型，并在 20 个多模态基准上全部刷新 SOTA。原生多模态训练（非后期拼接）。

## 关键技术细节
- 规模档位：Ultra（最强）/ Pro（均衡）/ Nano（端侧，含 Nano-1 1.8B 与 Nano-2 3.25B，4-bit 量化部署）。
- 原生多模态：从一开始就在文本+图像+音频+视频上联合训练，而非视觉适配器拼接。
- 架构：Transformer decoder，强化注意力机制以支持 32K 上下文。
- infra：在多个 TPUv4 与 TPUv5e Pod 上训练，跨数据中心；用 Jax + Pathways；强调大规模训练的稳定性与硬件故障容错（SDC 静默错误检测）。
- 评测：Gemini Ultra MMLU 90.0%（首超人类专家 89.8%）；MMMU 多模态 SOTA。
- 后训练：SFT + RLHF 优化指令遵循与安全。

## 原始链接
- url: https://arxiv.org/abs/2312.11805
- pdf_url: https://arxiv.org/pdf/2312.11805

## 本地落盘文件
- ../../../sources/llm/2023/gemini.pdf
