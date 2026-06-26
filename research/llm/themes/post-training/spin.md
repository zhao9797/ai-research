---
title: Self-Play Fine-Tuning Converts Weak Language Models to Strong Language Models (SPIN)
org: UCLA
country: US
date: 2024-01
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2401.01335
pdf_url: https://arxiv.org/pdf/2401.01335
github_url: https://github.com/uclaml/SPIN
downloaded: [spin.pdf]
---

## 一句话定位
SPIN：自博弈微调——让模型把"自己上一轮生成"当作负样本、把人类 SFT 数据当作正样本做类 DPO 训练，无需新的人类偏好数据即可自我增强。

## 摘要（3-6 句）
SPIN 用自博弈机制提升 SFT 模型：在每一轮，把当前模型生成的回答视为"对手/负例"，把原始 SFT 数据中的人类回答视为"正例"，用一个判别式目标（与 DPO 同形）训练模型，使其区分自身生成与人类数据并向人类分布靠拢；下一轮再用更新后的模型生成新负例，迭代自博弈直到收敛于人类分布。整个过程只需原有 SFT 数据、不需额外人类偏好标注，就能让弱模型显著变强，部分指标超过用额外偏好数据做 DPO 的模型。

## 关键技术细节
- 目标：与 DPO 同形的对数比损失，正例=SFT 人类回答 y，负例=上一轮模型自生成 y'。
- 自博弈迭代：θ_t 生成负例 → 训练得 θ_{t+1} → 再生成 → 直到模型生成与人类数据不可区分。
- 数据：仅用已有 SFT 数据集（如 Ultrachat200k 子集），零额外人类/AI 偏好。
- 理论：全局最优当且仅当策略分布 = 目标数据分布。
- 结果：zephyr-7b-sft-full 经 SPIN 多轮后在 HuggingFace Open LLM Leaderboard、MT-Bench 上显著提升，优于在额外数据上 DPO。

## 原始链接
- url: https://arxiv.org/abs/2401.01335
- pdf_url: https://arxiv.org/pdf/2401.01335
- github_url: https://github.com/uclaml/SPIN

## 一手源存档（sources/）
- spin.pdf  （PDF 不入 git，走 HF bucket）
