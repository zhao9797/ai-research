---
title: A General Theoretical Paradigm to Understand Learning from Human Preferences (IPO / ΨPO)
org: Google DeepMind
country: US
date: 2023-10
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2310.12036
pdf_url: https://arxiv.org/pdf/2310.12036
downloaded: [ipo.pdf]
---

## 一句话定位
IPO：提出统一偏好学习理论框架 ΨPO，并指出 DPO 的过拟合根源（Bradley-Terry 把偏好压成确定性），用平方损失正则化得到更稳健的 IPO。

## 摘要（3-6 句）
作者提出 ΨPO 通用理论框架，统一刻画 RLHF 与 DPO 为"对偏好的某种变换 + KL 正则"。分析表明 DPO 因隐含 Bradley-Terry 假设，会在偏好接近确定（几乎总是 chosen 优于 rejected）时无视 KL 正则、无限拉大 logit 差距而过拟合。为此 IPO（Identity-PO）改用恒等映射 + 平方误差目标，使 KL 正则始终有效，训练更稳健、对确定性偏好不过拟合。IPO 是 DPO 之后偏好优化理论分析与改进的代表工作。

## 关键技术细节
- ΨPO 目标：max E[Ψ(p*(y≻y'))] − τ·KL(π‖π_ref)，Ψ 为偏好概率的变换函数。
- RLHF/DPO 对应 Ψ=log(p/(1−p))（logit），在 p→1 时发散 → 过拟合、忽视正则。
- IPO 取 Ψ=identity，得到回归型损失：(h_θ(y_w,y_l) − τ⁻¹/2)²，其中 h 为对数比之差；KL 正则不被覆盖。
- 优点：无需显式 RM、无需采样，且对"确定性偏好/重复偏好对"鲁棒，不会无限拉大概率差。
- 实证：在合成与真实偏好上比 DPO 更不易过拟合。

## 原始链接
- url: https://arxiv.org/abs/2310.12036
- pdf_url: https://arxiv.org/pdf/2310.12036

## 一手源存档（sources/）
- ipo.pdf  （PDF 不入 git，走 HF bucket）
