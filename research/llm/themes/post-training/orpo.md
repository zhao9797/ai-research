---
title: ORPO: Monolithic Preference Optimization without Reference Model
org: KAIST
country: other
date: 2024-03
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2403.07691
pdf_url: https://arxiv.org/pdf/2403.07691
github_url: https://github.com/xfactlab/orpo
downloaded: [orpo.pdf]
---

## 一句话定位
ORPO（Odds Ratio Preference Optimization）：把 SFT 与偏好对齐合并为单阶段、无参考模型的训练，用 odds ratio 惩罚项让 SFT 损失同时区分 chosen/rejected。

## 摘要（3-6 句）
ORPO 指出标准 SFT 会无差别地提高所有回答（包括不被偏好的）概率，导致后续仍需单独的偏好对齐阶段。ORPO 在普通 SFT 的交叉熵损失上加一个基于 odds ratio 的惩罚项，直接在一次训练中既学会正确回答、又拉开 chosen 与 rejected 的胜率差距，无需参考模型、无需独立的偏好阶段。这使对齐流程从"SFT→DPO/PPO 两段"简化为单段，计算更省。在多规模上 ORPO 微调的模型超过同等的 SFT+DPO 流程。

## 关键技术细节
- 损失：L = L_SFT + λ·L_OR，其中 L_OR = −log σ(log(odds_θ(y_w|x)/odds_θ(y_l|x)))，odds = p/(1−p)。
- 无参考模型：不需要冻结的 π_ref（区别于 DPO），显存更省。
- 单阶段：在 SFT 数据（带 chosen/rejected）上一次训练完成对齐。
- λ 控制偏好惩罚强度，典型小值即可。
- 结果：Llama-2/Mistral 上 ORPO 在 AlpacaEval、MT-Bench 超过 SFT 及 SFT+DPO；Zephyr-style 复现简单。

## 原始链接
- url: https://arxiv.org/abs/2403.07691
- pdf_url: https://arxiv.org/pdf/2403.07691
- github_url: https://github.com/xfactlab/orpo

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/orpo.pdf
