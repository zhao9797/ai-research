---
title: Hunyuan-TurboS: Advancing Large Language Models through Mamba-Transformer Synergy and Adaptive Chain-of-Thought
org: 腾讯混元 (Tencent Hunyuan)
country: China
date: 2025-05
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2505.15431
pdf_url: https://arxiv.org/pdf/2505.15431
github_url:
downloaded: [hunyuan-turbos.pdf]
---

## 一句话定位
腾讯首个工业级大规模 Mamba 模型：Transformer-Mamba 混合 MoE（560B 总参 / 56B 激活），自适应长短 CoT，业界首个落地的大规模 Mamba 模型。发布 2025-05-21。

## 摘要
Hunyuan-TurboS 是大型混合 Transformer-Mamba MoE 模型，结合 Mamba 的长序列效率与 Transformer 的上下文理解。具备 adaptive long-short CoT 机制，简单 query 快速响应、复杂问题深度思考。架构上 56B 激活 / 560B 总参，128 层（Mamba2 + Attention + FFN），创新 AMF/MF block 模式；Mamba2 保证线性复杂度，GQA 减小 KV cache，FFN 用 MoE。在 16T 高质量 token 上预训练，支持 256K 上下文，是首个工业落地的大规模 Mamba 模型。后训练含 SFT（3M 指令）+ Adaptive Long-short CoT Fusion + Multi-round Deliberation Learning + 两阶段大规模 RL。

## 关键技术细节
- 架构：Transformer-Mamba2 混合 MoE；560B 总参 / 56B 激活，128 层，AMF（Attention-Mamba-FFN）/ MF block 模式。
- Mamba2：线性复杂度长序列处理；GQA 减小 KV cache；FFN 为 MoE。
- 自适应 CoT：长短 CoT 动态切换，按 query 复杂度分配算力。
- 预训练数据：16T 高质量 tokens；上下文 256K。
- 后训练：SFT 3M 指令 + Adaptive Long-short CoT Fusion + Multi-round Deliberation Learning + 两阶段 RL（STEM + 通用指令遵循）。
- 意义：业界首个大规模工业部署的 Mamba 模型。

## 原始链接
- url: https://arxiv.org/abs/2505.15431
- pdf_url: https://arxiv.org/pdf/2505.15431

## 本地落盘文件
- ../../../sources/llm/2025/hunyuan-turbos.pdf
