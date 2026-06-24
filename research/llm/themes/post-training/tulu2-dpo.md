---
title: Camels in a Changing Climate: Enhancing LM Adaptation with Tulu 2
org: AI2 (Allen Institute for AI)
country: US
date: 2023-11
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2311.10702
pdf_url: https://arxiv.org/pdf/2311.10702
github_url: https://github.com/allenai/open-instruct
downloaded: [tulu2-dpo.pdf]
---

## 一句话定位
Tulu 2：AI2 的开源指令微调套件，首批在 70B 规模上验证 DPO 有效的工作之一，奠定 open-instruct 训练框架与 Tulu 系列。

## 摘要（3-6 句）
Tulu 2 在 Llama-2 基础上系统研究指令微调数据混合与偏好优化：用精选指令数据集做 SFT 得 Tulu 2，再用 UltraFeedback 做 DPO 得 Tulu 2+DPO。论文给出在 7B/13B/70B 规模下 DPO 的一致增益，是较早证明 DPO 可扩展到 70B 的工作。还发布 Tulu 2 套件（数据、模型、代码）与 open-instruct 框架，成为后续 Tulu 3 的基础。

## 关键技术细节
- 基座：Llama-2 7B/13B/70B。
- SFT 数据：精选混合（FLAN、Open Assistant、ShareGPT、Evol-Instruct、CoT 等）。
- DPO：在 UltraFeedback 偏好上做 DPO，70B+DPO 在 MT-Bench、AlpacaEval 上显著提升。
- 发现：DPO 在大模型上稳定有效，几乎不损公开任务能力；偏好数据质量是关键。
- 开源：Tulu 2 / Tulu 2-DPO 权重、数据、open-instruct 训练代码。

## 原始链接
- url: https://arxiv.org/abs/2311.10702
- pdf_url: https://arxiv.org/pdf/2311.10702
- github_url: https://github.com/allenai/open-instruct

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/tulu2-dpo.pdf
