---
title: "Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned"
org: Anthropic
country: US
date: 2022-08
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2209.07858
pdf_url: https://arxiv.org/pdf/2209.07858
github_url: https://github.com/anthropics/hh-rlhf
downloaded: [anthropic-red-teaming.pdf]
---

## 一句话定位
Anthropic 红队方法论与数据集：系统研究不同规模/类型模型的红队可攻击性，发现 RLHF 模型越大越难攻破，是 Constitutional AI 的前身工作之一。

## 摘要
描述对语言模型红队（red teaming）以同时发现、度量、减少潜在有害输出的早期努力。三大贡献：(1) 研究 3 种规模（2.7B、13B、52B）× 4 种模型类型（纯 LM；提示为 HHH 的 LM；带拒绝采样的 LM；用 RLHF 训练为有用无害的模型）的红队缩放行为，发现 RLHF 模型随规模增大越来越难红队，其他类型则随规模平坦；(2) 公开 38,961 条红队攻击数据供分析；(3) 详尽描述红队的指令、流程、统计方法与不确定性。

## 关键技术细节
- 模型矩阵：2.7B / 13B / 52B × {plain LM, HHH-prompted LM, rejection sampling, RLHF}。
- 核心发现：RLHF 模型越大越难被红队攻破（harmlessness 随规模上升）；其余三类对规模不敏感。
- 公开数据：38,961 条人类红队对话攻击，含攻击成功度评分。
- 方法论：众包红队、攻击有害度标注、统计不确定性量化。
- 定位：Constitutional AI (2212.08073) 与 HH-RLHF 安全管线的前置研究，奠定 Anthropic"可量化危害 + 红队"安全方法。

## 原始链接
- url: https://arxiv.org/abs/2209.07858
- pdf_url: https://arxiv.org/pdf/2209.07858
- github_url: https://github.com/anthropics/hh-rlhf

## 一手源存档（sources/）
- anthropic-red-teaming.pdf  （PDF 不入 git，走 HF bucket）
