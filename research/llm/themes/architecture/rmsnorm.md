---
title: "Root Mean Square Layer Normalization (RMSNorm)"
org: University of Edinburgh / University of Zurich
country: EU
date: 2019-10
type: paper
categories: [架构]
url: https://arxiv.org/abs/1910.07467
pdf_url: https://arxiv.org/pdf/1910.07467
github_url: https://github.com/bzhangGo/rmsnorm
downloaded: [rmsnorm.pdf]
---

## 一句话定位
RMSNorm 去掉 LayerNorm 的均值中心化，只用均方根缩放，计算更省，几乎成为现代 LLM（LLaMA、Qwen、DeepSeek 等）的标配归一化。

## 摘要（3-6 句）
LayerNorm 通过 re-centering（减均值）和 re-scaling（除标准差）稳定训练，但计算开销大、拖慢网络。作者假设 re-centering 不是必需的，提出 RMSNorm：只用输入的均方根 (RMS) 做归一化，去掉均值统计与偏置，从而 re-scaling 不变性保留、计算更简单。实验在多种任务上显示 RMSNorm 与 LayerNorm 质量相当，但训练/推理更快（7%–64% 加速）。

## 关键技术细节
- 公式：RMSNorm(x) = x / RMS(x) · g，其中 RMS(x)=sqrt(mean(x²))，g 为可学习增益；无减均值、无 bias。
- 省去均值与方差中两项统计，仅算一项 RMS，计算与内存更省。
- 加速：相比 LayerNorm 约 7%–64% 提速（取决于网络）。
- 现状：被 LLaMA 系、Qwen、Gemma、DeepSeek、Mistral 等绝大多数现代 LLM 采用为默认归一化。
- 作者：Biao Zhang、Rico Sennrich。

## 原始链接
- url: https://arxiv.org/abs/1910.07467
- pdf_url: https://arxiv.org/pdf/1910.07467
- github_url: https://github.com/bzhangGo/rmsnorm

## 一手源存档（sources/）
- rmsnorm.pdf  （PDF 不入 git，走 HF bucket）
