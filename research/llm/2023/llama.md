---
title: LLaMA: Open and Efficient Foundation Language Models
org: Meta AI
country: US
date: 2023-02
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2302.13971
pdf_url: https://arxiv.org/pdf/2302.13971
downloaded: [llama.pdf]
---

## 一句话定位
Meta 第一代开放基础模型 LLaMA，证明纯公开数据可训出 SOTA，开启开源 LLM 浪潮。

## 摘要
LLaMA 是 7B 到 65B 参数的基础语言模型系列，训练于数万亿 token，且仅用公开可得数据集（无私有数据）。LLaMA-13B 在多数基准上超过 GPT-3(175B)，LLaMA-65B 与 Chinchilla-70B、PaLM-540B 竞争。全部模型向研究界开放。

## 关键技术细节
- 参数规模：7B / 13B / 33B / 65B 四档。
- 训练 token：1.0T（小模型）到 1.4T（33B/65B），全部公开数据。
- 数据配比：CommonCrawl 67%、C4 15%、GitHub 4.5%、Wikipedia 4.5%、Books 4.5%、ArXiv 2.5%、StackExchange 2%。
- 架构改进：Pre-normalization(RMSNorm)、SwiGLU 激活、Rotary 位置编码(RoPE)，去掉绝对位置编码。
- tokenizer：BPE（SentencePiece），词表约 32K。
- infra：65B 模型用 2048 张 A100-80GB，约 21 天，约 1.4T token；用 xformers 高效 causal attention 与激活重计算优化显存。
- 关键结论：13B 超 GPT-3(175B)，证明小模型+更多 token 的计算最优路线。

## 原始链接
- url: https://arxiv.org/abs/2302.13971
- pdf_url: https://arxiv.org/pdf/2302.13971

## 本地落盘文件
- ../../../sources/llm/2023/llama.pdf
