---
title: "Scaling Language Models: Methods, Analysis & Insights from Training Gopher"
org: DeepMind
country: US
date: 2021-12
type: paper
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2112.11446
pdf_url: https://arxiv.org/pdf/2112.11446
github_url:
downloaded: [arxiv-2112.11446.pdf]
---

## 一句话定位
DeepMind 的 280B 稠密 Transformer Gopher，系统研究了模型规模从千万到 2800 亿参数的能力变化，并配套发布高质量数据集 MassiveText。

## 摘要（3-6 句）
论文在 152 个任务上评估了一系列规模递增的 Transformer 语言模型，最大为 2800 亿参数的 Gopher。规模带来的收益在阅读理解、事实核查、有毒语言识别上最大，但逻辑和数学推理收益较小。论文对训练数据集与模型行为（偏见、毒性）做了整体分析，并讨论了语言模型在 AI 安全与下游危害缓解上的应用。

## 关键技术细节
- 模型规模族：从几千万到 280B；Gopher = 280B 参数。
- Gopher 架构：80 层（layers），d_model=16,384，128 个注意力头（heads），Key/Value size=128，max LR=4e-5，batch size 由 3M tokens 提升到 6M tokens。
- 训练：所有模型训练 300B tokens，上下文窗口 2048 tokens，优化器 Adam。
- 精度：<7.1B 用 float32 参数 + bfloat16 激活；7.1B 和 280B 用 bfloat16 参数+激活，bfloat16 参数用随机舍入（stochastic rounding）更新。
- Tokenizer：SentencePiece，词表 32,000，byte-level backoff 支持 open-vocabulary。
- 数据集：MassiveText（含质量过滤、去重、test-set overlap 移除的多源中英文本管线）。
- Infra：JAX + Haiku，用 pmap 表达数据并行与模型并行；全部在 TPUv3 上训练；Gopher 的半精度参数+单精度 Adam 状态占 2.5 TiB（远超单 TPUv3 core 的 16 GiB）。采用优化器状态分片（ZeRO 式）+ 模型并行（Megatron 式），pod 内用数据/模型并行，跨 1024-chip pod 用流水并行（pipelining）。

## 原始链接
- url: https://arxiv.org/abs/2112.11446
- pdf_url: https://arxiv.org/pdf/2112.11446

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2112.11446.pdf
