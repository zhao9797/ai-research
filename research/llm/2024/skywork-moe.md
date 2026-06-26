---
title: "Skywork-MoE: A Deep Dive into Training Techniques for Mixture-of-Experts Language Models"
org: 昆仑万维天工 (Kunlun Inc. / Skywork Team)
country: 中国
date: 2024-06
type: arxiv
categories: [架构, AI infra]
url: https://arxiv.org/abs/2406.06563
pdf_url: https://arxiv.org/pdf/2406.06563
github_url: https://github.com/SkyworkAI/Skywork-MoE
downloaded: [files/skywork-moe.pdf]
---

## 一句话定位
昆仑万维天工的 146B MoE（16 专家），由 Skywork-13B 稠密 checkpoint upcycling 而来，提出 gating logit 归一化与自适应辅助损失系数两项训练技巧。

## 摘要
Skywork-MoE 是 146B 参数、16 专家的高性能 MoE LLM，由已有的 Skywork-13B 稠密 checkpoint 初始化（upcycling）。系统对比 upcycling 与从头训练两种初始化方式，结论是选择取决于已有稠密 checkpoint 质量与 MoE 训练预算。提出两项创新技巧：(1) gating logit normalization——提升专家多样化；(2) adaptive auxiliary loss coefficients——允许逐层调节辅助损失系数。实验验证两者有效。

## 关键技术细节（带数字）
- 规模：146B 总参，16 个专家（top-2 激活，约 22B 激活）。
- 初始化：从 Skywork-13B 稠密 checkpoint upcycling。
- 技巧 1：gating logit normalization（门控 logit 归一化，提升专家差异化）。
- 技巧 2：adaptive auxiliary loss coefficients（逐层自适应辅助损失系数）。
- 研究结论：upcycling vs from-scratch 的选择取决于稠密底座质量与 MoE 训练预算。

## 原始链接
- arXiv: https://arxiv.org/abs/2406.06563
- PDF: https://arxiv.org/pdf/2406.06563
- GitHub: https://github.com/SkyworkAI/Skywork-MoE

## 一手源存档（sources/）
- skywork-moe.pdf  （PDF 不入 git，走 HF bucket）
