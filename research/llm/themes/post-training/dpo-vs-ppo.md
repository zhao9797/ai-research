---
title: Is DPO Superior to PPO for LLM Alignment? A Comprehensive Study
org: Tsinghua / OpenPsi / ICML 2024
country: China
date: 2024-04
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2404.10719
pdf_url: https://arxiv.org/pdf/2404.10719
downloaded: [dpo-vs-ppo.pdf]
---

## 一句话定位
系统对比 DPO 与 PPO：理论与实验表明 DPO 存在固有缺陷、在分布外样本上可被利用，而调优良好的 PPO 在困难任务（尤其代码竞赛）上明显更强。

## 摘要（3-6 句）
针对"DPO 是否优于 PPO"的争论，本文给出理论分析与大规模实验。理论上指出 DPO 可能找到利用分布外（偏好数据未覆盖）回答的有偏解。实验系统消融 PPO 的关键因素（优势归一化、大 batch、reference model 的指数滑动平均更新等），证明调优好的 PPO 在对话与代码任务上稳定超过 DPO；在最难的 CodeContests 上，34B PPO 模型超过 AlphaCode-41B。结论是高质量 RLHF 仍依赖在线 RL（PPO），DPO 的简单性以能力上限为代价。

## 关键技术细节
- 理论：DPO 的解集包含利用 OOD 回答的策略；偏好数据分布与模型采样分布不匹配会被 DPO 利用。
- PPO 关键技巧（消融得出）：优势归一化、大训练 batch size、用 EMA 更新参考模型；三者对 PPO 性能至关重要。
- 任务：SafeRLHF 对话、HH、APPS、CodeContests 等。
- 结果：CodeContests 上 34B PPO 模型 10@1k = 22.4%，超过 AlphaCode-41B（13.8%）；多数任务 PPO > DPO。
- 含义：DPO 易实现但能力上限受限；追求 SOTA 仍需在线 RL。

## 原始链接
- url: https://arxiv.org/abs/2404.10719
- pdf_url: https://arxiv.org/pdf/2404.10719

## 一手源存档（sources/）
- dpo-vs-ppo.pdf  （PDF 不入 git，走 HF bucket）
