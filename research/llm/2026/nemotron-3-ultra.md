---
title: "Nemotron 3 Ultra: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning"
org: NVIDIA
country: US
date: 2026-06
type: paper
categories: [架构, AI infra, 后训练, agentic训练, 预训练数据]
url: https://arxiv.org/abs/2606.15007
pdf_url: https://arxiv.org/pdf/2606.15007
github_url:
downloaded: [arxiv-2606.15007.pdf]
---

## 一句话定位
NVIDIA 2026-06 发布的 Nemotron 3 Ultra——550B 总 / 55B 激活的 MoE 混合 Mamba-Attention 模型，为长时自主 agentic 任务优化，1M 上下文，全开源（base/post-trained/quantized + 数据 + 配方）。

## 摘要
Nemotron 3 Ultra 是 Nemotron 3 家族中最大、最强的模型：550B 总参数、55B 激活参数的 MoE 混合 Mamba-Attention 语言模型。先在 20T 文本 token 上预训练，再扩展上下文至 1M token，随后用 SFT + RL + 多教师在线策略蒸馏（MOPD）做后训练。关键技术包括 LatentMoE、Multi-Token Prediction (MTP)、NVFP4 预训练、多环境 RLVR、MOPD 与推理预算控制（reasoning budget control）。相比当前公开 SOTA LLM，推理吞吐最高约 6×，同时精度持平。高吞吐 + 1M 上下文使其适合长时自主 agentic 任务。base、post-trained、quantized 检查点与训练数据/配方在 HuggingFace 开源。

## 关键技术细节
- 提交日期：2026-06-12（PDF 标注 2026-6-16）。机构：NVIDIA。
- 规模：550B 总参数 / 55B 激活参数；MoE 混合 Mamba-Attention 架构。
- 预训练：20T 文本 token；NVFP4 精度预训练。
- 上下文：预训练后扩展至 1M token。
- 架构创新：LatentMoE（兼顾每 FLOP 精度与每参数精度）、MTP（原生投机解码加速）。
- 后训练：SFT + RL（多环境 RLVR）+ 多教师在线策略蒸馏 MOPD（Multi-teacher On-Policy Distillation）；推理预算控制。
- 性能：推理吞吐相比公开 SOTA 最高约 6×，精度 on-par。
- 开源：base / post-trained / quantized 检查点 + 训练数据 + 配方（HuggingFace）。
- 定位：长时自主 agentic（写代码、做研究、完成复杂任务）。

## 原始链接
- url: https://arxiv.org/abs/2606.15007
- pdf_url: https://arxiv.org/pdf/2606.15007

## 本地落盘文件
- ../../../sources/llm/2026/arxiv-2606.15007.pdf
