---
title: "Ring-lite: Scalable Reasoning via C3PO-Stabilized Reinforcement Learning for LLMs"
org: 蚂蚁集团 Ling Team / inclusionAI (Ant Group)
country: China
date: 2025-06
type: paper
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2506.14731
pdf_url: https://arxiv.org/pdf/2506.14731
github_url: https://github.com/inclusionAI/Ring
downloaded: [ring-lite.pdf]
---

## 一句话定位
蚂蚁基于 Ling-lite（16.8B/2.75B 激活 MoE）做 RL 的推理模型，提出 C3PO 稳定 MoE RL 训练，仅激活同类 1/3 参数即达小规模推理 SOTA。发布 2025-06-17。

## 摘要
Ring-lite 是基于公开 Ling-lite（16.8B 总参 / 2.75B 激活 MoE）经 RL 优化的推理模型，在 AIME、LiveCodeBench、GPQA-Diamond 等难 benchmark 上匹敌小规模 SOTA 推理模型，而仅激活同类模型 1/3 的参数。提出整合蒸馏与 RL 的联合训练 pipeline，揭示 MoE RL 训练的未公开挑战：(1) 发现 RL 训练优化不稳定，提出 C3PO（Constrained Contextual Computation Policy Optimization）通过算法-系统协同提升稳定性与吞吐；(2) 实证应按 entropy loss 而非验证指标选蒸馏 checkpoint 做 RL，性能-效率更优；(3) 设计两阶段训练范式协调数学与代码能力。

## 关键技术细节
- 基座：Ling-lite，16.8B 总参 / 2.75B 激活 MoE。
- RL 算法：C3PO（Constrained Contextual Computation Policy Optimization），算法-系统协同稳定 MoE RL、提升吞吐。
- 训练 pipeline：蒸馏 + RL 联合；按 entropy loss 选蒸馏 checkpoint；两阶段（数学 → 代码协调）。
- 效率：仅激活同类模型 ~1/3 参数即达 SOTA。
- 开源：GitHub inclusionAI/Ring（蚂蚁 Ring 系列推理模型）。

## 原始链接
- url: https://arxiv.org/abs/2506.14731
- pdf_url: https://arxiv.org/pdf/2506.14731
- github_url: https://github.com/inclusionAI/Ring

## 一手源存档（sources/）
- ring-lite.pdf  （PDF 不入 git，走 HF bucket）
