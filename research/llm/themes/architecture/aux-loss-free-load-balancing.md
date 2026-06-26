---
title: "Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts"
org: DeepSeek-AI
country: China
date: 2024-08
type: paper
categories: [架构]
url: https://arxiv.org/abs/2408.15664
pdf_url: https://arxiv.org/pdf/2408.15664
downloaded: [aux-loss-free.pdf]
---

## 一句话定位
提出 Loss-Free Balancing：用每个专家的可动态调整偏置项做路由负载均衡，彻底去掉传统辅助损失带来的梯度干扰，被 DeepSeek-V3 采用。

## 摘要（3-6 句）
传统 MoE 用 auxiliary load-balancing loss 平衡专家负载，但该损失会向训练注入与语言建模无关的干扰梯度，损害性能。本文提出 Loss-Free Balancing：在路由打分上为每个专家加一个 bias，并根据近期负载自动上下调（过载专家减 bias、欠载专家加 bias），从而无需辅助损失即可保持均衡。该方法既保证负载均衡又不引入干扰梯度，在 1B 和 3B 规模、最多 200B+ tokens 上验证，困惑度优于传统辅助损失方法。

## 关键技术细节
- 机制：gating 分数 + 专家专属 bias b_i 决定 top-k 选择；bias 按专家近期负载用类似乘性/加性规则动态更新，不参与梯度。
- 优势：消除 auxiliary loss 的干扰梯度，负载均衡与模型质量解耦；保持 expert specialization。
- 验证规模：1B（最多约 100B token）与 3B（约 200B token）MoE，困惑度优于 aux-loss baseline，且负载更均衡。
- 直接被 DeepSeek-V3 用作其负载均衡策略（auxiliary-loss-free）。
- 作者：Lean Wang、Huazuo Gao、Chenggang Zhao 等。

## 原始链接
- url: https://arxiv.org/abs/2408.15664
- pdf_url: https://arxiv.org/pdf/2408.15664

## 一手源存档（sources/）
- aux-loss-free.pdf  （PDF 不入 git，走 HF bucket）
