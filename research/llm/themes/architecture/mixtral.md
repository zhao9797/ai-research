---
title: "Mixtral of Experts"
org: Mistral AI
country: EU
date: 2024-01
type: report
categories: [架构]
url: https://arxiv.org/abs/2401.04088
pdf_url: https://arxiv.org/pdf/2401.04088
downloaded: [mixtral.pdf]
---

## 一句话定位
Mixtral 8x7B 是开源稀疏 MoE 标杆：每层 8 个专家、每 token 选 2 个，47B 总参/13B 激活，性能匹敌或超过 Llama-2 70B 和 GPT-3.5。

## 摘要（3-6 句）
Mixtral 8x7B 是稀疏 MoE 语言模型，架构与 Mistral 7B 相同，区别在于每层有 8 个前馈专家，路由器为每个 token 在每层选 2 个专家处理并合并输出。虽然每 token 只用 2 个专家，但不同位置可选不同专家，因此每 token 可访问 47B 参数、实际只激活 13B。Mixtral 在多数基准上匹敌或超过 Llama-2 70B 和 GPT-3.5，尤其在数学、代码、多语言上更强；同时发布指令微调版 Mixtral 8x7B-Instruct。模型以 Apache 2.0 开放。

## 关键技术细节
- 结构：每层 8 个专家，top-2 路由；47B 总参、13B 激活/ token；32K 上下文。
- 推理：激活参数等同 ~13B dense，速度/成本接近小模型，质量接近 70B。
- 基于 Mistral 7B 架构（GQA、SwiGLU、RoPE、sliding-window attention 的演进）。
- 性能：≥ Llama-2 70B 与 GPT-3.5；数学/代码/多语言突出。
- Instruct 版用 SFT + DPO 对齐；Apache 2.0 开放权重。

## 原始链接
- url: https://arxiv.org/abs/2401.04088
- pdf_url: https://arxiv.org/pdf/2401.04088

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/mixtral.pdf
