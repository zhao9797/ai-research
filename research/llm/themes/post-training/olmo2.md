---
title: 2 OLMo 2 Furious
org: AI2 (Allen Institute for AI)
country: US
date: 2025-01
type: report
categories: [后训练, 预训练数据, 架构]
url: https://arxiv.org/abs/2501.00656
pdf_url: https://arxiv.org/pdf/2501.00656
github_url: https://github.com/allenai/OLMo
downloaded: [olmo2.pdf]
---

## 一句话定位
OLMo 2：AI2 全开放（数据/代码/权重/日志）模型族，后训练直接套用 Tulu 3 配方（SFT + DPO + RLVR），是可复现"开放后训练"的完整端到端样本。

## 摘要（3-6 句）
OLMo 2（7B/13B，后续 32B）是完全开放的语言模型，预训练、架构与训练稳定性都有改进（RMSNorm 位置调整、QK-Norm、Z-loss 等以稳住训练）。其指令版 OLMo 2-Instruct 直接采用 Tulu 3 后训练流水线：SFT → DPO → RLVR（可验证奖励 RL），并开源全部后训练数据与代码。OLMo 2 在同等算力下达到开放权重模型的帕累托前沿，是研究"预训练 + 完全开放后训练"的端到端可复现基线。

## 关键技术细节
- 模型：OLMo 2 7B / 13B（含 32B 后续），稠密；改进训练稳定性（reordered norm、QK-Norm、Z-loss、init 调整）。
- 预训练：约 4–5T tokens（OLMo-Mix-1124 + Dolmino 中途数据），两阶段（高质量数据 mid-training）。
- 后训练：完全复用 Tulu 3 配方——SFT（Tulu 3 SFT mix）→ DPO（偏好数据）→ RLVR（数学等可验证任务 0/1 奖励 RL）。
- 全开放：权重、训练数据、训练/评测代码、中间 checkpoint、训练日志全部公开。
- 评测：OLMo 2-Instruct 在开放权重同规模中领先，逼近 Llama 3.1 / Qwen 2.5 Instruct。

## 原始链接
- url: https://arxiv.org/abs/2501.00656
- pdf_url: https://arxiv.org/pdf/2501.00656
- github_url: https://github.com/allenai/OLMo

## 一手源存档（sources/）
- olmo2.pdf  （PDF 不入 git，走 HF bucket）
