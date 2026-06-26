---
title: "InternLM2 Technical Report"
org: 上海人工智能实验室 (Shanghai AI Laboratory)
country: 中国
date: 2024-03
type: arxiv
categories: [预训练数据, 架构, 后训练, AI infra]
url: https://arxiv.org/abs/2403.17297
pdf_url: https://arxiv.org/pdf/2403.17297
github_url: https://github.com/InternLM/InternLM
downloaded: [files/internlm2.pdf]
---

## 一句话定位
上海 AILab 书生·浦语第二代（1.8B/7B/20B），200K 长上下文 + 创新的 COOL RLHF（条件在线 RLHF）对齐方案，并完整披露数据处理与训练 infra。

## 摘要
InternLM2 开源（1.8B/7B/20B），在多项主客观评测、长上下文建模与开放式主观评测上超越同期开源模型。报告详述预训练数据准备（文本/代码/长文本）、训练 infra（InternEvo）、长上下文从 4K→32K 预训练后在 200K "大海捞针"上表现优异，以及对齐：SFT + 新提出的 COOL RLHF（Conditional Online RLHF，用条件奖励模型缓解多目标偏好冲突、用在线 RLHF 缓解 reward hacking）。

## 关键技术细节（带数字）
- 规模：1.8B / 7B / 20B。
- 上下文：4K → 32K 预训练，外推到 200K（Needle-in-a-Haystack 通过）。
- 预训练数据：约 2.6T tokens（文本 + 代码 + 长文本）。
- Infra：InternEvo 训练框架（数据/张量/流水/序列并行 + ZeRO）。
- 对齐：SFT + COOL RLHF（Conditional OnLine RLHF）—— 条件奖励模型 + 多轮在线 PPO，缓解偏好冲突与 reward hacking。
- 工具：原生支持代码解释器与 agent 能力。

## 原始链接
- arXiv: https://arxiv.org/abs/2403.17297
- PDF: https://arxiv.org/pdf/2403.17297
- GitHub: https://github.com/InternLM/InternLM

## 一手源存档（sources/）
- internlm2.pdf  （PDF 不入 git，走 HF bucket）
