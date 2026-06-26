---
title: OpenAI GPT-4.5 System Card
org: OpenAI
country: US
date: 2025-02
type: system-card
categories: [预训练数据, AI infra, 后训练]
url: https://openai.com/index/gpt-4-5-system-card/
pdf_url: https://cdn.openai.com/gpt-4-5-system-card-2272025.pdf
github_url:
downloaded: [files/openai-gpt-4.5-system-card.pdf]
---

## 一句话定位
OpenAI 2025-02-27 发布的 GPT-4.5（研究预览）官方 system card，定位为目前规模最大、知识最广的非推理 GPT 模型，强调无监督学习/规模化预训练与新的对齐技术。

## 摘要
GPT-4.5 通过扩展无监督学习（更多算力+数据+架构与优化创新）提升世界知识、写作与对话情商，减少幻觉。配套披露用新的可扩展对齐技术（从更小模型蒸馏数据训练更大模型）。System card 给出 Preparedness Framework 风险评估：归类为 Medium risk（首个被部署的 Medium 风险模型，自评 self-improvement/cyber/CBRN/persuasion 各维度）。不披露参数等架构数字。

## 关键技术细节（带数字）
- 训练范式：scaling 无监督学习（pretraining + 指令微调/RLHF），非推理（non-reasoning）模型。
- 对齐：用从更小模型生成的训练数据/新可扩展对齐技术训练更大模型（蒸馏式对齐）。
- 幻觉：SimpleQA 准确率较 GPT-4o 提升、幻觉率下降（card 内给出 PersonQA/SimpleQA 数值对比）。
- 安全：Preparedness Framework 评级 Medium（CBRN/Cybersecurity/Persuasion/Model Autonomy 四维评估）。
- 不含总参/层数/MoE/训练 token 等架构数字。
- 发布日期：2025-02-27。

## 原始链接
- 官方页面：https://openai.com/index/gpt-4-5-system-card/
- 官方 PDF：https://cdn.openai.com/gpt-4-5-system-card-2272025.pdf

## 一手源存档（sources/）
- openai-gpt-4.5-system-card.pdf  （PDF 不入 git，走 HF bucket）
