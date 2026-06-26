---
title: "RLHF Workflow: From Reward Modeling to Online RLHF"
org: Salesforce / UIUC (RLHFlow)
country: US
date: 2024-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2405.07863
pdf_url: https://arxiv.org/pdf/2405.07863
github_url: https://github.com/RLHFlow/Online-RLHF
downloaded: [rlhf-workflow.pdf]
---

## 一句话定位
开源完整"在线迭代 RLHF（Online Iterative RLHF）"工作流：用代理偏好模型在线生成偏好对做迭代 DPO，证明在线 > 离线，产出 SOTA 开源对齐模型 SFR-Iterative-DPO。

## 摘要（3-6 句）
本技术报告给出一套可复现的在线迭代 RLHF 全流程：训练偏好模型作为人类反馈的代理，再用它对当前策略采样的回答在线打偏好标签，做迭代 DPO（Online Iterative DPO），并用拒绝采样选样本。相比只用固定离线偏好数据的 DPO，在线迭代显著更好。基于全开源数据训练的 LLaMA-3-8B-SFR-Iterative-DPO 在 AlpacaEval-2、Arena-Hard、MT-Bench 等达到甚至超过许多更大模型与闭源模型。论文与代码（RLHFlow）面向社区可复现。

## 关键技术细节
- 偏好模型作为人类代理：训练 RM/pairwise preference model，对在线采样回答打标。
- 在线迭代 DPO：每轮用最新策略采样 → 代理 RM 标偏好 → DPO 更新 → 重复（缓解离线 DPO 的分布漂移与覆盖不足）。
- 全开源数据：仅用公开数据集训练，保证可复现。
- 结果：Llama-3-8B-SFR-Iterative-DPO-R 在 AlpacaEval-2 LC 31.3%、Arena-Hard 29.1%、MT-Bench 8.46，超同规模并逼近更大模型。
- 交付：RLHFlow 代码库（reward modeling + online RLHF 全流程）。

## 原始链接
- url: https://arxiv.org/abs/2405.07863
- pdf_url: https://arxiv.org/pdf/2405.07863
- github_url: https://github.com/RLHFlow/Online-RLHF

## 一手源存档（sources/）
- rlhf-workflow.pdf  （PDF 不入 git，走 HF bucket）
