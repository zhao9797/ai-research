---
title: QLoRA: Efficient Finetuning of Quantized LLMs
org: University of Washington
country: US
date: 2023-05
type: paper
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2305.14314
pdf_url: https://arxiv.org/pdf/2305.14314
github_url: https://github.com/artidoro/qlora
downloaded: [qlora.pdf]
---

## 一句话定位
QLoRA 用 4-bit NF4 + LoRA 在单张 48GB GPU 微调 65B，民主化大模型微调，催生 Guanaco。

## 摘要
QLoRA 在单张 48GB GPU 上微调 65B 模型且保持 16-bit 全量微调性能：把梯度通过冻结的 4-bit 量化预训练模型反传进 LoRA 适配器。最佳模型族 Guanaco 在 Vicuna 基准超所有此前开放模型，达 ChatGPT 99.3%，仅需单 GPU 24 小时微调。创新含：(a)4-bit NormalFloat(NF4) 信息论最优数据类型；(b)double quantization 量化量化常数省显存；(c)paged optimizers 管理显存尖峰。用 QLoRA 微调了 1000+ 模型。

## 关键技术细节
- NF4：4-bit NormalFloat，对正态分布权重信息论最优的量化数据类型。
- Double Quantization：再量化量化常数，平均每参数省约 0.37 bit。
- Paged Optimizers：用 NVIDIA 统一内存处理梯度检查点显存尖峰，避免 OOM。
- 显存：65B 微调从 >780GB 降到 <48GB（单卡）。
- Guanaco：QLoRA 微调 LLaMA，Vicuna 基准达 ChatGPT 99.3%，单 GPU 24h。
- 规模实验：1000+ 模型，8 个指令数据集，LLaMA/T5 多尺寸。

## 原始链接
- url: https://arxiv.org/abs/2305.14314
- pdf_url: https://arxiv.org/pdf/2305.14314
- github_url: https://github.com/artidoro/qlora

## 本地落盘文件
- ../../../sources/llm/2023/qlora.pdf
