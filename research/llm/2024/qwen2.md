---
title: "Qwen2 Technical Report"
org: 阿里巴巴 Qwen Team
country: 中国
date: 2024-07
type: arxiv
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2407.10671
pdf_url: https://arxiv.org/pdf/2407.10671
github_url: https://github.com/QwenLM/Qwen2
downloaded: [files/qwen2.pdf]
---

## 一句话定位
阿里通义千问第二代开源系列（0.5B–72B，含一个 57B-A14B MoE），旗舰 Qwen2-72B 多基准领先同期开源模型。

## 摘要
Qwen2 是覆盖 0.5B 到 72B 的稠密模型系列，外加一个 57B-A14B MoE 模型。旗舰 Qwen2-72B 基座 MMLU 84.2、GPQA 37.9、HumanEval 64.6、GSM8K 89.5、BBH 82.4；指令版 MT-Bench 9.1、Arena-Hard 48.1、LiveCodeBench 35.7。多语言能力覆盖约 30 种语言。

## 关键技术细节（带数字）
- 规模：0.5B / 1.5B / 7B / 72B 稠密 + 57B-A14B MoE（激活 14B）。
- 注意力：全系列 GQA；引入 Dual Chunk Attention + YARN 扩展上下文。
- 训练数据：7T tokens（0.5B 版用 12T）。
- 上下文：最高 128K（72B/7B Instruct）。
- 后训练：SFT + DPO（含 online merging optimizer）。
- 基准：Qwen2-72B 基座 MMLU 84.2 / GSM8K 89.5 / HumanEval 64.6；多语言约 30 种。

## 原始链接
- arXiv: https://arxiv.org/abs/2407.10671
- PDF: https://arxiv.org/pdf/2407.10671
- GitHub: https://github.com/QwenLM/Qwen2

## 本地落盘文件
- ../../../sources/llm/2024/qwen2.pdf
