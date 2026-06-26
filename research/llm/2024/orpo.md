---
title: "ORPO: Monolithic Preference Optimization without Reference Model"
org: KAIST AI
country: other
date: 2024-03
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2403.07691
pdf_url: https://arxiv.org/pdf/2403.07691
github_url: https://github.com/xfactlab/orpo
downloaded: [2403.07691.pdf]
---

## 一句话定位
ORPO：把偏好对齐融入 SFT 的单体（monolithic）算法——用 odds ratio 惩罚不被偏好的风格，无需单独的偏好对齐阶段，也无需参考模型。

## 摘要
近期偏好对齐算法有效，但 SFT 仍是收敛的前提。本文研究 SFT 在偏好对齐中的关键作用，指出对不被偏好的生成风格施加一个小惩罚就足以实现偏好对齐的 SFT。据此提出一个简单、无参考模型的单体 odds ratio 偏好优化算法 ORPO，消除了额外偏好对齐阶段的必要。理论与实证上证明 odds ratio 是在 SFT 中对比偏好/非偏好风格的合理选择（125M-7B 各尺寸）。仅用 UltraFeedback 对 Phi-2(2.7B)、Llama-2(7B)、Mistral(7B) 做 ORPO，即超过 >7B/13B 的 SOTA 模型：AlpacaEval2.0 最高 12.20%、IFEval 66.19%、MT-Bench 7.32。

## 关键技术细节
- 单体目标：L = L_SFT + λ·L_OR，其中 L_OR 用 chosen 与 rejected 的 odds ratio 对数构造惩罚。
- 无需参考模型、无需独立 RLHF/DPO 阶段——一次训练完成 SFT + 对齐。
- 适用尺度：125M-7B 验证有效。
- 结果：Mistral-ORPO-α/β(7B) 仅用 UltraFeedback 即超 >7B/13B SOTA；公开代码与检查点。

## 原始链接
- url: https://arxiv.org/abs/2403.07691
- pdf_url: https://arxiv.org/pdf/2403.07691
- github: https://github.com/xfactlab/orpo

## 一手源存档（sources/）
- [2403.07691.pdf](https://arxiv.org/pdf/2403.07691)  （arXiv 原文 PDF，不入 git）
