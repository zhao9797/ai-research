---
title: Mixtral of Experts (Mixtral 8x7B)
org: Mistral AI
country: EU
date: 2024-01
type: report
categories: [架构, AI infra]
url: https://arxiv.org/abs/2401.04088
pdf_url: https://arxiv.org/pdf/2401.04088
downloaded: [mixtral-2401.04088.pdf]
---

## 一句话定位
Mistral AI 的稀疏 MoE 模型，每层 8 个专家、每 token 选 2 个，47B 总参 / 13B 激活，性能持平或超过 Llama 2 70B，是西方开源 MoE 的代表与推理 infra 的常见基准。

## 摘要（3-6 句）
Mixtral 8x7B 与 Mistral 7B 同架构，但每层 FFN 换成 8 个专家，router 每 token 每层选 top-2 专家并合并输出。每 token 可访问 47B 参数但推理只激活 13B，因而以远低于 dense 70B 的算力达到甚至超过 Llama 2 70B / GPT-3.5（数学、代码、多语言尤其领先）。上下文 32K。开源 base 与 Instruct（DPO 对齐）版本，是 vLLM/SGLang/TensorRT-LLM 等推理系统 MoE 支持的常用模型。

## 关键技术细节
- SMoE：每层 8 experts，top-2 路由；47B 总参 / 13B active params；上下文 32K。
- 与 Mistral 7B 同骨架（GQA、SWA 思路），expert 替换 FFN。
- 性能：≥ Llama 2 70B 与 GPT-3.5，数学/代码/多语言显著领先；推理成本接近 13B dense。
- Mixtral 8x7B-Instruct 用 SFT + DPO 对齐；Apache-2.0 开源。

## 原始链接
- url: https://arxiv.org/abs/2401.04088
- pdf_url: https://arxiv.org/pdf/2401.04088

## 一手源存档（sources/）
- [mixtral-2401.04088.pdf](https://arxiv.org/pdf/2401.04088)  （arXiv 原文 PDF，不入 git）
