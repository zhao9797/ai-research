---
title: "PaLM: Scaling Language Modeling with Pathways"
org: Google Research
country: US
date: 2022-04
type: report
categories: [架构, AI infra, 预训练数据]
url: https://arxiv.org/abs/2204.02311
pdf_url: https://arxiv.org/pdf/2204.02311
downloaded: [palm.pdf]
---

## 一句话定位
PaLM 是 540B dense Transformer，用 Pathways 系统跨 6144 块 TPU v4 训练，确立了 SwiGLU、并行注意力/FFN、MQA、RoPE 等一整套现代 dense 架构组件。

## 摘要（3-6 句）
PaLM（Pathways Language Model）是 5400 亿参数的 dense decoder-only Transformer，用 Google 的 Pathways 系统在两个 TPU v4 Pod（共 6144 芯片）上高效训练，达到当时极高的硬件利用率。PaLM 在数百个语言理解与生成基准上取得突破性的少样本表现，在多步推理（尤其配合思维链）上随规模出现能力涌现。论文确立了一套被后续 dense 模型广泛沿用的架构与训练工程组件。

## 关键技术细节
- 规模：540B 参数 dense Transformer；780B token 预训练。
- 架构组件：SwiGLU 激活、parallel attention+FFN 层（并行而非串行，加速）、Multi-Query Attention（MQA）、RoPE 位置编码、共享输入输出 embedding、无 bias。
- infra：Pathways 系统，6144 TPU v4（两 Pod），跨 Pod 数据并行 + Pod 内模型并行，硬件 FLOPs 利用率约 46.2%。
- 能力涌现：思维链 (chain-of-thought) 推理在 540B 规模显著涌现；BIG-bench 多任务突破。
- 是 PaLM 2、Gemini 之前 Google 旗舰 dense 模型，组件影响 LLaMA 等开源模型。

## 原始链接
- url: https://arxiv.org/abs/2204.02311
- pdf_url: https://arxiv.org/pdf/2204.02311

## 一手源存档（sources/）
- palm.pdf  （PDF 不入 git，走 HF bucket）
