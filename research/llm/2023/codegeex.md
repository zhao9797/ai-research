---
title: "CodeGeeX: A Pre-Trained Model for Code Generation with Multilingual Benchmarking on HumanEval-X"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua）
country: China
date: 2023-03
type: paper
categories: [AI infra, 架构, 预训练数据]
url: https://arxiv.org/abs/2303.17568
pdf_url: https://arxiv.org/pdf/2303.17568
github_url: https://github.com/THUDM/CodeGeeX
downloaded: [codegeex.pdf]
---

## 一句话定位
智谱/清华 CodeGeeX：13B 多语言代码生成模型，完全在华为昇腾 Ascend 910 国产芯片集群上训练，是 2023 中国"国产算力训练大模型"的代表性 infra 一手论文（KDD'23）。

## 摘要（3-6 句）
CodeGeeX 是 130 亿参数的多语言代码生成模型，在 23 种编程语言、850B token 上预训练（截至 2022 年 6 月）。在 HumanEval-X 上的代码生成与翻译任务超越同规模多语言代码模型。模型在 1,536 块昇腾 910 AI 处理器上、用 MindSpore 框架训练约两个月，并提供同时支持 Ascend 与 NVIDIA GPU 的推理实现，及覆盖 100+ 语言的 VS Code/JetBrains 插件。

## 关键技术细节
- 规模：13B 参数；架构 = 39 层左到右 Transformer 解码器 + 一个 Top Query Layer（取位置 n+1 的 query embedding 作最终输出）。
- hidden size 5120，40 个注意力头；LayerNorm（epsilon 1e-5，FP32 精度）。
- 数据：158B token 代码语料（The Pile + CodeParrot + 自采），覆盖 23 种编程语言；训练消耗 850B token（约 5+ epoch）。
- Tokenizer：GPT-2 BPE，多空白合并为额外 token，最终词表 52,224（含多语言自然语言 token，支持中/法/俄/日等）。
- 国产算力 infra：1,536 块昇腾 910（32GB）+ MindSpore v1.7.0，192 节点训练约两个月；模型并行 8 × 数据并行 192。
- 跨平台：发布支持 Ascend 与 NVIDIA GPU 的推理；FasterTransformer 加速。
- 配套基准 HumanEval-X：扩展 HumanEval 到多语言（Python/C++/Java/JS/Go 等）代码生成与翻译评测。
- 应用：每周生成约 47 亿 token，服务数万活跃用户。

## 原始链接
- url: https://arxiv.org/abs/2303.17568
- pdf_url: https://arxiv.org/pdf/2303.17568
- github_url: https://github.com/THUDM/CodeGeeX

## 本地落盘文件
- ../../../sources/llm/2023/codegeex.pdf
