---
title: "Qwen2.5 Technical Report"
org: 阿里巴巴 Qwen Team
country: 中国
date: 2024-12
type: arxiv
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2412.15115
pdf_url: https://arxiv.org/pdf/2412.15115
github_url: https://github.com/QwenLM/Qwen2.5
downloaded: [files/qwen2.5.pdf]
---

## 一句话定位
通义千问 2.5：预训练语料从 7T 扩到 18T token，后训练做 100 万+ SFT + 多阶段 RL，0.5B–72B 全尺寸，成为 2024 末最强开源系列之一。

## 摘要
Qwen2.5 是全尺寸 LLM 系列。预训练数据从上一代 7T tokens 扩展到 18T tokens，为常识、专家知识、推理打下基础；后训练采用超过 100 万样本的 SFT，加上多阶段强化学习（offline DPO + online GRPO）。同时衍生 Qwen2.5-Turbo / Qwen2.5-Plus API 版本，以及 Qwen2.5-Math、Qwen2.5-Coder、QwQ 等专项模型。

## 关键技术细节（带数字）
- 规模：0.5B / 1.5B / 3B / 7B / 14B / 32B / 72B 稠密；外加 Turbo / Plus（MoE）API 版。
- 训练数据：18T tokens（上代 7T）。
- 上下文：常规 128K，Turbo 支持 1M。
- 后训练：1M+ 样本 SFT + 多阶段 RL（DPO 离线 + GRPO 在线）。
- 架构：GQA、SwiGLU、RoPE、RMSNorm、QKV bias。
- 基准：Qwen2.5-72B-Instruct 在 MMLU-Pro/MATH/代码上比肩更大模型，逼近 Llama-3.1-405B。

## 原始链接
- arXiv: https://arxiv.org/abs/2412.15115
- PDF: https://arxiv.org/pdf/2412.15115
- GitHub: https://github.com/QwenLM/Qwen2.5

## 一手源存档（sources/）
- qwen2.5.pdf  （PDF 不入 git，走 HF bucket）
