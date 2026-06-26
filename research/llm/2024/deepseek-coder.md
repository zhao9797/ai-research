---
title: "DeepSeek-Coder: When the Large Language Model Meets Programming -- The Rise of Code Intelligence"
org: DeepSeek-AI
country: 中国
date: 2024-01
type: arxiv
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2401.14196
pdf_url: https://arxiv.org/pdf/2401.14196
github_url: https://github.com/deepseek-ai/DeepSeek-Coder
downloaded: [files/deepseek-coder.pdf]
---

## 一句话定位
DeepSeek 第一代开源代码模型（1.3B–33B），项目级语料 + 仓库级依赖排序 + FIM 训练，开源代码模型 SOTA。

## 摘要
DeepSeek-Coder 系列从头训练，规模 1.3B 到 33B，在 2T token 上预训练。语料为高质量项目级代码语料，采用 fill-in-the-blank（FIM）任务与 16K 窗口提升生成与补全能力。多基准评测显示其在开源代码模型中达到 SOTA，并超越 CodeLlama-34B 等。

## 关键技术细节（带数字）
- 规模：1.3B / 5.7B / 6.7B / 33B。
- 训练数据：2T tokens，87% 代码 + 13% 中英自然语言；覆盖 87 种编程语言。
- 仓库级预训练：基于依赖关系的拓扑排序，构造跨文件上下文。
- 训练任务：next-token + Fill-in-the-Middle（FIM）；窗口 16K。
- 性能：开源代码模型 SOTA，DeepSeek-Coder-Base-33B 超过 CodeLlama-34B。

## 原始链接
- arXiv: https://arxiv.org/abs/2401.14196
- PDF: https://arxiv.org/pdf/2401.14196
- GitHub: https://github.com/deepseek-ai/DeepSeek-Coder

## 一手源存档（sources/）
- deepseek-coder.pdf  （PDF 不入 git，走 HF bucket）
