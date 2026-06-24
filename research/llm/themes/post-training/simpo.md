---
title: SimPO: Simple Preference Optimization with a Reference-Free Reward
org: Princeton / University of Virginia
country: US
date: 2024-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2405.14734
pdf_url: https://arxiv.org/pdf/2405.14734
github_url: https://github.com/princeton-nlp/SimPO
downloaded: [simpo.pdf]
---

## 一句话定位
SimPO：用"长度归一化的平均对数似然"作为隐式奖励，去掉参考模型并加入目标奖励 margin γ，使偏好优化更简单、更省、效果常超 DPO。

## 摘要（3-6 句）
SimPO 改进 DPO 两点：(1) 用策略对序列的平均对数概率（按长度归一化）作为隐式奖励，与生成时的解码度量对齐，且天然抑制长度偏置；(2) 引入目标奖励差 margin γ，要求 chosen 比 rejected 高出 γ 才算满足。由此 SimPO 不再需要参考模型 π_ref，显存与计算更省、实现更简单。在 Mistral、Llama-3 等基座上，SimPO 在 AlpacaEval 2、Arena-Hard 上一致超过 DPO 及其多个变体，且生成长度不膨胀。

## 关键技术细节
- 隐式奖励：r(x,y) = (β/|y|)·Σ log π_θ(y_t|x,y_<t)，长度归一化的平均 logprob，无 π_ref。
- 目标 margin：损失 = −log σ(r(x,y_w) − r(x,y_l) − γ)，γ>0 拉开偏好间隔。
- 无参考模型：相比 DPO 省去冻结 ref 的前向，显存/算力更低。
- 抑制长度偏置：长度归一化避免 DPO 偏好更长回答的问题。
- 结果：Llama-3-8B-Instruct + SimPO 在 AlpacaEval 2 LC 达 44%+、Arena-Hard 33%+，超 DPO/IPO/KTO/ORPO 等。

## 原始链接
- url: https://arxiv.org/abs/2405.14734
- pdf_url: https://arxiv.org/pdf/2405.14734
- github_url: https://github.com/princeton-nlp/SimPO

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/simpo.pdf
