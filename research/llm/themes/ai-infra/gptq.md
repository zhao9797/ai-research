---
title: "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"
org: IST Austria / ETH Zurich / Neural Magic
country: EU
date: 2022-10
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2210.17323
pdf_url: https://arxiv.org/pdf/2210.17323
downloaded: [gptq-2210.17323.pdf]
---

## 一句话定位
基于二阶信息的一次性权重量化方法，可把 175B 模型在数小时内量化到 3-4 bit 且几乎不掉点，是开源 LLM 4-bit 部署的基石。

## 摘要（3-6 句）
GPTQ 是 PTQ（post-training quantization）方法，基于近似二阶（Hessian）信息逐层逐列量化权重并即时补偿误差（源自 OBQ/OBS 思路的加速版）。它能在约 4 GPU 小时内将 OPT-175B / BLOOM-176B 量化到 3-4 bit，精度损失可忽略，相对 FP16 推理可在单卡上跑大模型并加速。论文展示 3-bit 量化也基本可用，是后续 4-bit 权重量化生态（含 ExLlama、AutoGPTQ）的源头。

## 关键技术细节
- 逐列贪心量化 + Cholesky 重排，利用逆 Hessian 做误差补偿；one-shot、无需重训。
- 175B 模型约 4 GPU·hr 完成量化；INT4/INT3 权重，几乎无 perplexity 损失。
- 仅量化权重（weight-only），激活仍 FP16；推理时反量化或用专用 kernel。
- 单张 A100/A6000 即可推理 175B 模型，端到端约 3.25× 加速（A100，INT3）。

## 原始链接
- url: https://arxiv.org/abs/2210.17323
- pdf_url: https://arxiv.org/pdf/2210.17323

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/gptq-2210.17323.pdf
