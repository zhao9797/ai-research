---
title: "PaLM: Scaling Language Modeling with Pathways"
org: Google Research
country: US
date: 2022-04
type: paper
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2204.02311
pdf_url: https://arxiv.org/pdf/2204.02311
github_url:
downloaded: [palm.pdf]
---

## 一句话定位
谷歌 540B 稠密 Transformer，用 Pathways 系统在 6144 块 TPU v4 上训练，展示规模带来的"突破性"few-shot 与多步推理能力。

## 摘要
PaLM 是 5400 亿参数的稠密激活 Transformer 语言模型，使用 Pathways 系统在 6144 块 TPU v4 芯片上跨多个 TPU Pod 高效训练。在数百个语言理解与生成基准上取得 SOTA few-shot 结果；在多步推理任务（配合 CoT）上超越微调 SOTA，并在 BIG-bench 上超越人类平均水平。许多 BIG-bench 任务随规模呈现"不连续"（涌现式）提升。PaLM 在多语言与代码生成上也表现强劲。论文附带偏见与毒性的全面分析。

## 关键技术细节
- 架构：稠密 decoder-only Transformer；三种规模 8B / 62B / 540B。
- 540B 配置：118 层，隐藏维度 18432，48 注意力头（多查询注意力 MQA）。
- 架构改进：SwiGLU 激活、RoPE 位置编码、并行 Attention+FFN 层、共享输入输出嵌入、无偏置、SentencePiece 256K 词表。
- 训练数据：780B token，混合网页、书籍、维基、对话、GitHub 代码。
- Infra：6144 块 TPU v4（跨 2 个 Pod），Pathways 系统，模型 FLOPs 利用率（MFU）达 46.2%，是当时大模型训练效率的标杆。
- 并行：数据并行 + 模型并行（每 Pod 内 12-way 模型并行 + 256-way 数据并行）。
- 能力：在 GSM8K（配 CoT + 外部计算器）达 58%；BIG-bench 超人类平均。

## 原始链接
- url: https://arxiv.org/abs/2204.02311
- pdf_url: https://arxiv.org/pdf/2204.02311

## 一手源存档（sources/）
- palm.pdf  （PDF 不入 git，走 HF bucket）
