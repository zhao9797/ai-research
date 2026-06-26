---
title: Nemotron-4 340B Technical Report
org: NVIDIA
country: US
date: 2024-06
type: report
categories: [后训练, 预训练数据, 架构]
url: https://arxiv.org/abs/2406.11704
pdf_url: https://arxiv.org/pdf/2406.11704
github_url: https://huggingface.co/nvidia/Nemotron-4-340B-Instruct
downloaded: [nemotron4-340b.pdf]
---

## 一句话定位
NVIDIA Nemotron-4 340B：开放权重的 340B 模型族，后训练高度依赖合成数据（>98% 对齐数据为模型生成），并开源奖励模型与合成数据生成管线。

## 摘要（3-6 句）
Nemotron-4 340B 包含 Base、Instruct、Reward 三个开放模型。最大亮点是后训练几乎完全用合成数据：超过 98% 的对齐数据由模型自身生成（合成 prompt + 合成回答），仅约 2 万条人类标注用于引导。对齐流程含 SFT、偏好微调（DPO 与 NVIDIA 提出的 RPO，Reward-aware Preference Optimization），并训练一个高质量奖励模型 Nemotron-4-340B-Reward 来评估与过滤合成数据。NVIDIA 同时开源合成数据生成 pipeline，鼓励社区用其造对齐数据。

## 关键技术细节
- 模型：Base / Instruct / Reward 三档，340B 稠密，开放权重；上下文 4K。
- 预训练：约 9T tokens，多语言+代码。
- 合成数据后训练：>98% 对齐数据由模型生成；用 Reward 模型按 helpfulness/correctness/coherence/complexity/verbosity 五属性打分过滤。
- 偏好优化：DPO + RPO（reward-aware preference optimization，利用 RM 分数差作为目标 margin 的偏好优化）。
- 奖励模型：Nemotron-4-340B-Reward 在 RewardBench 上当时领先。
- 开源：合成数据生成 pipeline、HelpSteer2 等数据集。

## 原始链接
- url: https://arxiv.org/abs/2406.11704
- pdf_url: https://arxiv.org/pdf/2406.11704
- model: https://huggingface.co/nvidia/Nemotron-4-340B-Instruct

## 一手源存档（sources/）
- nemotron4-340b.pdf  （PDF 不入 git，走 HF bucket）
