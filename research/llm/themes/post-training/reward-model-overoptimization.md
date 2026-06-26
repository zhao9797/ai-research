---
title: Scaling Laws for Reward Model Overoptimization
org: OpenAI
country: US
date: 2022-10
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2210.10760
pdf_url: https://arxiv.org/pdf/2210.10760
downloaded: [reward-overoptimization.pdf]
---

## 一句话定位
RLHF 中"奖励黑客/过度优化"的定量研究：用 gold RM 作为真值，给出代理 RM 分数随 KL 增大而失真的 scaling law 公式。

## 摘要（3-6 句）
当用一个学习到的代理奖励模型（proxy RM）做 RLHF 或 best-of-n 时，优化越强（KL 越大），真实目标（由更大的 gold RM 度量）会先升后降——即 over-optimization / reward hacking。作者用合成设置（gold RM 生成偏好标签）系统量化该现象，给出 gold 分数关于 KL 距离的解析形式 scaling law（best-of-n 与 RL 形式不同），并研究 RM 规模、RM 训练数据量、策略规模对过优化点的影响。结论为 RLHF 的 KL 预算、RM 选型与早停提供了定量指导。

## 关键技术细节
- 方法：用一个大 "gold" RM 充当真实奖励，训练不同规模的 proxy RM 拟合其偏好标签，再用 proxy RM 做优化。
- 度量：以 KL 散度 d=KL(π‖π_init) 的平方根 √d 为横轴，gold 分数为纵轴。
- best-of-n 拟合：gold(d) ≈ d·(α_bon − β_bon·d)；RL 拟合：gold(d) ≈ d·(α_RL − β_RL·log d)（系数随 RM 规模变化）。
- 发现：proxy RM 越大、偏好数据越多，过优化点越靠后、峰值越高；策略规模对系数影响相对小。
- 实践含义：RLHF 需控制 KL 预算或加 RM ensemble/早停以避免奖励黑客。

## 原始链接
- url: https://arxiv.org/abs/2210.10760
- pdf_url: https://arxiv.org/pdf/2210.10760

## 一手源存档（sources/）
- reward-overoptimization.pdf  （PDF 不入 git，走 HF bucket）
