---
title: Phi-4-reasoning Technical Report
org: Microsoft
country: US
date: 2025-04
type: technical-report
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2504.21318
pdf_url: https://arxiv.org/pdf/2504.21318
github_url:
downloaded: [files/phi-4-reasoning.pdf]
---

## 一句话定位
Microsoft 2025-04 的 Phi-4-reasoning 技术报告：14B 推理模型，靠 SFT（用 o3-mini 生成的推理示范 + 精选"teachable"prompts）+ 短期 outcome-based RL，以小博大逼近 DeepSeek-R1。

## 摘要
Phi-4-reasoning 在 Phi-4 之上做 SFT：精选"可教（teachable）"的合适复杂度/多样性 prompts，并用 o3-mini 生成推理链作为示范数据，训练出能高效利用 inference-time compute 的详细推理链。Phi-4-reasoning-plus 再加一段 outcome-based RL（生成更长推理 trace）进一步提升。两者均显著超越更大的 DeepSeek-R1-Distill-Llama-70B，并接近完整 DeepSeek-R1。

## 关键技术细节（带数字）
- 参数：14B（基于 Phi-4）。
- SFT 数据：精选"teachable"prompts + 用 o3-mini 生成的推理示范（reasoning demonstrations）。
- Phi-4-reasoning-plus：额外一段短期 outcome-based 强化学习（RL），生成更长推理 trace。
- 效果：均超越更大的 DeepSeek-R1-Distill-Llama-70B，接近完整 DeepSeek-R1；并向通用基准迁移。
- 评测覆盖：数学/科学推理、编码、算法、规划、空间理解。
- 发布日期：2025-04（arXiv:2504.21318）。

## 原始链接
- arXiv：https://arxiv.org/abs/2504.21318
- PDF：https://arxiv.org/pdf/2504.21318

## 一手源存档（sources/）
- phi-4-reasoning.pdf  （PDF 不入 git，走 HF bucket）
