---
title: Qwen Technical Report
org: 阿里巴巴（Alibaba / Qwen Team）
country: China
date: 2023-09
type: paper
categories: [预训练数据, 架构, 后训练, agentic训练]
url: https://arxiv.org/abs/2309.16609
pdf_url: https://arxiv.org/pdf/2309.16609
github_url: https://github.com/QwenLM/Qwen
downloaded: [qwen-technical-report.pdf]
---

## 一句话定位
阿里 Qwen 系列首份技术报告，覆盖 1.8B/7B/14B 基座、Qwen-Chat（SFT+RLHF）、以及 Code-Qwen / Math-Qwen 专用模型，是 2023 年中国开源大模型最完整的一手技术文档之一。

## 摘要（3-6 句）
报告介绍了 Qwen 大模型系列的首个版本，包含不同参数规模的基座预训练模型与经人类对齐的 Qwen-Chat 对话模型。基座模型在多项下游任务上表现优越，Chat 模型（尤其经 RLHF 训练的版本）具有很强竞争力，并具备先进的工具使用与规划能力，可用于构建 agent 应用（如调用 code interpreter）。此外还开发了编码专用模型 Code-Qwen / Code-Qwen-Chat 和数学专用模型 Math-Qwen-Chat。报告同时介绍了 tokenizer、上下文长度扩展、奖励模型与 RLHF 等技术细节。

## 关键技术细节
- 模型规格（Table 1）：1.8B（hidden 2048 / 16 heads / 24 层 / 训练 2.2T token）、7B（hidden 4096 / 32 heads / 32 层 / 2.4T token）、14B（hidden 5120 / 40 heads / 40 层 / 3.0T token）；batch size 4M，学习率 3.0e-4。
- 预训练数据：trillions of tokens，多领域文本与代码；用 exact-match + MinHash 模糊去重；语言判别后增配高质量数据。
- Tokenizer：基于 BPE，起点为 tiktoken 的 cl100k_base，扩充中文等多语言词表，数字按单字拆分，最终词表约 152K（压缩率优于 XLM-R 等）。
- 架构：改进版 Transformer；untied input/output embedding；RoPE（FP32 逆频率矩阵以重视性能）；除 QKV 层保留 bias 外其余层去 bias（增强外推）；Pre-Norm + RMSNorm；SwiGLU（FFN 维度由 4h 降为 8/3 h）。
- 上下文：基座训练 context length 2048；推理期用免训练技术（如 NTK-aware 插值、LogN 注意力缩放、window attention）扩展长上下文。
- 后训练：SFT + 训练奖励模型（RM）模拟人类偏好 + RLHF；含 Qwen-Chat 与 Qwen-Chat-RLHF。
- agentic：Chat 模型原生支持 tool use、code interpreter、ReAct 式 agent；在工具调用/agent 基准上接近甚至超过更大模型。
- 专用模型：Code-Qwen-7B/14B（代码继续预训练），Math-Qwen-7B/14B-Chat（数学，GSM8K 接近 GPT-3.5）。

## 原始链接
- url: https://arxiv.org/abs/2309.16609
- pdf_url: https://arxiv.org/pdf/2309.16609
- github_url: https://github.com/QwenLM/Qwen

## 本地落盘文件
- ../../../sources/llm/2023/qwen-technical-report.pdf
