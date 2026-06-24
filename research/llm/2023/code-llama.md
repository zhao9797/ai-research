---
title: "Code Llama: Open Foundation Models for Code"
org: Meta AI
country: US
date: 2023-08
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2308.12950
pdf_url: https://arxiv.org/pdf/2308.12950
downloaded: [code-llama.pdf]
---

## 一句话定位
Meta 基于 Llama 2 的代码专用模型族，支持填充与最长 100k 上下文，开源代码模型 SOTA。

## 摘要
Code Llama 是基于 Llama 2 的代码 LLM 族，提供 foundation(Code Llama)、Python 专精(Code Llama-Python)、指令版(Code Llama-Instruct)，各有 7B/13B/34B/70B。全部在 16k token 序列上训练，可外推到 100k token 输入。7B/13B/70B 支持基于上下文的填充(infilling)。HumanEval 67%、MBPP 65%，开源 SOTA。

## 关键技术细节
- 规模：7B/13B/34B/70B × 3 个变体(base/Python/Instruct)。
- 训练：从 Llama 2 继续训练，500B 代码 token（Python 版再 +100B）。
- 长上下文：16k 训练序列，RoPE base 调整(θ=1e6)后可处理至 100k。
- 填充(FIM)：7B/13B/70B 支持 fill-in-the-middle，用于代码补全。
- 评测：HumanEval 最高 67%、MBPP 65%；Code Llama-Python 7B 在 HumanEval/MBPP 超 Llama 2 70B；MultiPL-E 全面领先。
- 许可：可研究+商用。

## 原始链接
- url: https://arxiv.org/abs/2308.12950
- pdf_url: https://arxiv.org/pdf/2308.12950

## 本地落盘文件
- ../../../sources/llm/2023/code-llama.pdf
