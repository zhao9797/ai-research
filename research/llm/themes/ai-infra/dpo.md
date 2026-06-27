---
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
org: Stanford
country: US
date: 2023-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2305.18290
pdf_url: https://arxiv.org/pdf/2305.18290
downloaded: [dpo-2305.18290.pdf]
---

> 📄 主题索引条目 —— 完整六维精读见 [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](../../2023/dpo.md)。

## 一句话定位
把 RLHF 的「训奖励模型 + PPO」两阶段简化为单一分类损失，直接在偏好对上优化策略，无需采样/奖励模型，是 RLHF 之外最主流的对齐方法。
