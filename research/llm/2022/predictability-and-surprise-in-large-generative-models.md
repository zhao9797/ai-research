---
title: Predictability and Surprise in Large Generative Models
org: Anthropic
country: US
date: 2022-02
type: paper
categories: [架构]
url: https://arxiv.org/abs/2202.07785
pdf_url: https://arxiv.org/pdf/2202.07785
github_url:
downloaded: [predictability-and-surprise.pdf]
---

## 一句话定位
Anthropic 指出大生成模型的"可预测损失 vs 不可预测具体能力"悖论及其政策含义，是涌现能力讨论的安全/治理侧奠基论文。

## 摘要
大规模预训练近来成为创造 GPT-3、MT-NLG、Gopher 等通用生成模型的技术。本文强调这类模型的一个反直觉性质并讨论其政策含义：它们的损失在宽训练分布上高度可预测（即"缩放律"），但具体能力、输入、输出却不可预测。作者认为高层可预测性与有用能力的出现驱动了此类模型的快速发展，而不可预测性使其部署后果难以预料。论文用文献与现实案例展示这种组合如何导致社会有害行为。

## 关键技术细节
- 核心张力：scaling laws → 训练损失可预测；但下游具体能力（尤其涌现能力）出现的时点/形态不可预测。
- 这种"可预测 + 不可预测"组合既驱动行业投入，又制造部署风险。
- 给出政策建议：信息披露、风险评估、第三方审计、部署前红队等治理机制。
- 与同年 Emergent Abilities (2206.07682)、Predictability 形成"能力涌现"叙事的能力侧与治理侧两翼。
- 代表 Anthropic 早期"安全 + 治理"研究取向。

## 原始链接
- url: https://arxiv.org/abs/2202.07785
- pdf_url: https://arxiv.org/pdf/2202.07785

## 一手源存档（sources/）
- predictability-and-surprise.pdf  （PDF 不入 git，走 HF bucket）
