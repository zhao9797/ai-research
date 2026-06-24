---
title: Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding
org: 阶跃星辰 (StepFun)
country: China
date: 2025-07
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2507.19427
pdf_url: https://arxiv.org/pdf/2507.19427
github_url: https://github.com/stepfun-ai/Step3
downloaded: [step-3.pdf]
---

## 一句话定位
阶跃 321B VLM，硬件感知的模型-系统协同设计，提出 MFA（多矩阵分解注意力）与 AFD（注意力-FFN 解耦推理系统），把长上下文解码成本压到低于 DeepSeek-V3 / Qwen3-235B。发布 2025-07-25。

## 摘要
Step-3 是 321B 参数 VLM，以硬件感知的 model-system co-design 最小化解码成本。两大创新：(1) Multi-Matrix Factorization Attention (MFA)——显著降低 KV cache 与计算，同时保持高注意力表达力；(2) Attention-FFN Disaggregation (AFD)——把 attention 与 FFN 层解耦为专门子系统的分布式推理系统。该协同设计在解码成本上显著优于 DeepSeek-V3 与 Qwen3 MoE 235B，且优势随上下文增长扩大。Step-3 每 token 激活 38B（多于 V3 与 Qwen3-235B），在 Hopper GPU 上实现高解码吞吐。

## 关键技术细节
- 架构：321B 总参 VLM，每 token 激活 38B。
- MFA：Multi-Matrix Factorization Attention，降低 KV cache 与计算，保留表达力。
- AFD：Attention-FFN Disaggregation，attention 与 FFN 解耦到专门子系统的分布式推理。
- 协同设计目标：hardware-aligned attention arithmetic intensity + MoE 稀疏 + AFD，最大化成本效益。
- 对比：解码成本显著低于 DeepSeek-V3、Qwen3-235B（长上下文优势更大）；Hopper GPU 高吞吐。

## 原始链接
- url: https://arxiv.org/abs/2507.19427
- pdf_url: https://arxiv.org/pdf/2507.19427
- github_url: https://github.com/stepfun-ai/Step3

## 本地落盘文件
- ../../../sources/llm/2025/step-3.pdf
