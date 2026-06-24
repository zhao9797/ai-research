---
title: Llama 2: Open Foundation and Fine-Tuned Chat Models
org: Meta AI
country: US
date: 2023-07
type: paper
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2307.09288
pdf_url: https://arxiv.org/pdf/2307.09288
downloaded: [llama-2.pdf]
---

## 一句话定位
Meta 第二代开放权重模型，含详尽 RLHF/安全对齐方法论，可商用，是 2023 开源 LLM 的事实标准底座。

## 摘要
Llama 2 是 7B–70B 的预训练与微调 LLM 集合。微调版 Llama 2-Chat 面向对话优化，在多数基准上超过开源对话模型，按人评在有用性与安全性上可替代闭源模型。报告详述微调与安全方法论。

## 关键技术细节
- 参数：7B / 13B / 34B（未发布权重）/ 70B；预训练 2.0T token（比 Llama1 多 40%）。
- 上下文长度：4096（Llama1 为 2048）。
- 架构：RMSNorm + SwiGLU + RoPE；34B 与 70B 使用 Grouped-Query Attention(GQA)。
- 后训练：SFT（27,540 条高质量标注）→ RLHF；用两个独立奖励模型（Helpfulness RM + Safety RM）。
- RL 算法：PPO + Rejection Sampling fine-tuning 结合。
- 新方法 Ghost Attention(GAtt)：多轮对话中保持系统指令一致性。
- 安全：Safety SFT、Safety RLHF、Safety Context Distillation。
- 预训练算力：累计约 3.3M GPU-hours（A100-80GB），碳排约 539 tCO2eq。

## 原始链接
- url: https://arxiv.org/abs/2307.09288
- pdf_url: https://arxiv.org/pdf/2307.09288

## 本地落盘文件
- ../../../sources/llm/2023/llama-2.pdf
