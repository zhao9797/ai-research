---
title: "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"
org: IST Austria / ETH Zurich 等
country: EU
date: 2022-10
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2210.17323
pdf_url: https://arxiv.org/pdf/2210.17323
github_url: https://github.com/IST-DASLab/gptq
downloaded: [gptq.pdf]
---

## 一句话定位
GPTQ：基于二阶信息的一次性权重量化，把 175B GPT/OPT 量化到 3-4 bit，几乎无损，单 GPU 即可推理。

## 摘要
GPT/OPT 类生成式预训练 Transformer 性能突破但计算与存储成本极高，巨大体量使即便推理也需多张高性能 GPU，限制可用性。现有压缩方法受限于 GPT 模型的规模与复杂度。本文提出 GPTQ：基于近似二阶信息的一次性（one-shot）权重量化方法，既高精度又高效。GPTQ 可在约几个 GPU 小时内量化 1750 亿参数的 GPT 模型，并把位宽降到每权重 3–4 bit。

## 关键技术细节
- 方法：逐层求解量化最优问题，用近似 Hessian（OBQ 思想的高效版）按列贪心量化并补偿误差；一次性 PTQ，无需重训。
- 速度：175B 模型量化约 4 个 GPU 小时即可完成。
- 位宽：3-bit / 4-bit 权重量化，相对 FP16 几乎无困惑度损失。
- 部署：使 OPT-175B / BLOOM-176B 可在单张 A100/A6000 上推理；提供定制 CUDA kernel 加速。
- 影响：成为开源社区 4-bit 量化（GPTQ-for-LLaMa、AutoGPTQ 等）的事实标准之一。

## 原始链接
- url: https://arxiv.org/abs/2210.17323
- pdf_url: https://arxiv.org/pdf/2210.17323
- github_url: https://github.com/IST-DASLab/gptq

## 一手源存档（sources/）
- gptq.pdf  （PDF 不入 git，走 HF bucket）
