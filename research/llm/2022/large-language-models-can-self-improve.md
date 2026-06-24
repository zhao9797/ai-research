---
title: Large Language Models Can Self-Improve
org: Google / UIUC    country: US    date: 2022-10    type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2210.11610    pdf_url: https://arxiv.org/pdf/2210.11610    github_url:
downloaded: [lm-self-improve.pdf]
---

## 一句话定位
证明 LLM 可仅用无标注数据自我改进：用 CoT + self-consistency 生成高置信答案再自训练，540B 模型推理能力显著提升。

## 摘要
LLM 在各任务上表现优异，但微调需大量监督。人类却能不靠外部输入、通过自我思考提升推理。本文证明 LLM 也能仅用无标注数据自我改进：用预训练 LLM 对无标注问题用 CoT 提示 + self-consistency 生成"高置信"的带推理答案，再用这些自生成的解作为目标输出微调自身。该方法提升 540B 模型的通用推理能力（GSM8K 74.4%→82.1%，DROP 78.2%→83.0%，OpenBookQA 90.0%→94.4%，ANLI-A3 63.4%→67.9%），在无任何真值标签下达到 SOTA 级表现。

## 关键技术细节
- 流程：无标注问题 → CoT 多路径采样 → self-consistency 选高置信答案 → 用 (问题, 推理, 答案) 自训练（微调）。
- 关键：用模型自身的高一致性输出作为"伪标签"，无需人工真值。
- 提升（PaLM-540B）：GSM8K +7.7%、DROP +4.8%、OpenBookQA +4.4%、ANLI-A3 +4.5%。
- 还研究 self-generated 数据的多样性/格式（含 self-consistency、混合格式、问题生成）对增益的影响。
- 是"自训练 / self-improvement / 拒绝采样微调（RFT）"路线在 LLM 推理上的奠基工作之一。

## 原始链接
- url: https://arxiv.org/abs/2210.11610
- pdf_url: https://arxiv.org/pdf/2210.11610

## 本地落盘文件
- ../../../sources/llm/2022/lm-self-improve.pdf
