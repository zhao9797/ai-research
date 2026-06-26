---
title: 2 OLMo 2 Furious (OLMo 2 技术报告)
org: Allen Institute for AI (AI2)
country: US
date: 2025-01
type: technical-report
categories: [预训练数据, 架构, 后训练, AI infra]
url: https://arxiv.org/abs/2501.00656
pdf_url: https://arxiv.org/pdf/2501.00656
github_url: https://github.com/allenai/OLMo
downloaded: [files/olmo-2.pdf]
---

## 一句话定位
AI2 2025-01 的 OLMo 2 技术报告：完全开放（权重+全部训练数据+代码+日志）的稠密自回归 LM 家族（7B/13B/32B），主打训练稳定性改进、两阶段数据课程（Dolmino Mix）与 Tülu 3 风格 RLVR 后训练。

## 摘要
OLMo 2 是 AI2 下一代 fully-open 模型：7B/13B/32B 稠密模型，全部 artifact（权重、完整训练数据、训练代码与配方、训练日志、eval 套件）开源。报告深入分析预训练稳定性（架构与初始化改动如 RMSNorm/QK-norm），引入两阶段课程：大规模 web 预训练（olmo-mix-1124）+ 高质量 mid-training（dolmino-mix-1124，含数学专项 mix），后训练用 Tülu 3 配方（SFT + DPO + RLVR）。在同算力下达到 Pareto 前沿。

## 关键技术细节（带数字）
- 模型：OLMo-2 7B / 13B / 32B（dense autoregressive）；base + Instruct。
- 完全开放：权重、完整训练数据、训练代码（OLMo / OLMo-core）、训练日志、eval 代码（olmes）、数据工具（dolma）。
- 数据课程（两阶段）：预训练 olmo-mix-1124 + mid-training dolmino-mix-1124（高质量来源 + math mix）。
- 稳定性：架构/初始化改动（如 RMSNorm、QK-norm 等）提升预训练稳定性。
- 后训练：Tülu 3 风格——SFT + DPO + RLVR（Reinforcement Learning from Verifiable Rewards）。
- 训练：NVIDIA H100；同算力下处于性能-FLOPs Pareto 前沿。
- 发布日期：2025-01（arXiv:2501.00656）；后续 3 月发布 32B（见 ai2-olmo-2-32b.md）。

## 原始链接
- arXiv：https://arxiv.org/abs/2501.00656
- PDF：https://arxiv.org/pdf/2501.00656
- 官方：https://allenai.org/olmo2

## 一手源存档（sources/）
- olmo-2.pdf  （PDF 不入 git，走 HF bucket）
