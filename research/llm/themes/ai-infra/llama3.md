---
title: The Llama 3 Herd of Models
org: Meta AI
country: US
date: 2024-07
type: report
categories: [架构, AI infra, 预训练数据, 后训练]
url: https://arxiv.org/abs/2407.21783
pdf_url: https://arxiv.org/pdf/2407.21783
github_url: https://github.com/meta-llama/llama-models
downloaded: [llama3-2407.21783.pdf]
---

## 一句话定位
Meta 的 Llama 3 全家桶报告，405B dense 旗舰在 16384×H100 上以 4D 并行训练 15.6T token，详尽披露训练 infra、并行策略、数据配比与后训练流程。

## 摘要（3-6 句）
Llama 3 是支持多语言、代码、推理、工具调用的基础模型家族，最大为 405B dense Transformer、128K 上下文，质量比肩 GPT-4。报告极为详尽地公开了训练栈：15.6T token 预训练、4D 并行（TP+PP+CP+FSDP）、最高 16384×H100 集群、BF16、定制网络与容错。后训练用多轮 SFT + DPO（弃用复杂 PPO 以求稳定）。它是西方厂商少见的工业级 infra 全披露，对并行、数据、稳定性、后训练都有可抄的数字。

## 关键技术细节
- 旗舰 405B dense：126 层、hidden 16384、128 heads（GQA，8 KV heads）、词表 128K；上下文 8K→128K。
- 预训练数据：约 15.6T token；多语言/代码/数学比例与去重、质量分类详述。
- 训练 infra：最高 16384×H100，4D 并行 = Tensor + Pipeline + Context + Data(FSDP)；BF16；MFU 约 38-43%；自研容错与网络（RoCE）调优；峰值 3.8×10^25 FLOPs。
- 后训练：6 轮迭代 SFT + Rejection Sampling + DPO（不用 PPO）；Llama Guard 3 安全模型。

## 原始链接
- url: https://arxiv.org/abs/2407.21783
- pdf_url: https://arxiv.org/pdf/2407.21783
- github_url: https://github.com/meta-llama/llama-models

## 一手源存档（sources/）
- [llama3-2407.21783.pdf](https://arxiv.org/pdf/2407.21783)  （arXiv 原文 PDF，不入 git）
