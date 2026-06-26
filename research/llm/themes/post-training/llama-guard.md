---
title: "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations"
org: Meta
country: US
date: 2023-12
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2312.06674
pdf_url: https://arxiv.org/pdf/2312.06674
downloaded: [llama-guard.pdf]
---

## 一句话定位
Llama Guard：基于 LLM 的输入/输出安全分类器，把内容审核做成可指令化的安全分类任务，用安全分类法（taxonomy）对提示与回答打标。

## 摘要（3-6 句）
Llama Guard 是基于 Llama-2-7B 微调的安全护栏模型，用一套安全风险分类法（taxonomy）对用户输入（prompt classification）和模型输出（response classification）分别判定是否安全及违规类别。它把审核任务表述为指令遵循形式：把分类法描述放进 prompt，模型输出 safe/unsafe 与类别，从而支持零样本/少样本适配新策略与新类别。在公开与内部基准上其表现优于现有审核 API。Llama Guard 开源权重，成为开源安全护栏与 agent 安全的基础组件，后续迭代到 Llama Guard 2/3。

## 关键技术细节
- 基座：Llama-2-7B 指令微调。
- 任务：prompt-classification（用户输入是否违规）与 response-classification（模型回答是否违规）两类。
- Taxonomy：人写安全类别（暴力、性、犯罪策划、武器、自伤等）；分类法写入 prompt，可在推理期调整/扩展。
- 指令化：输出格式为 safe/unsafe + 违规类别编号，支持 zero/few-shot 迁移到新策略。
- 评测：在 OpenAI Mod、ToxicChat 等优于 Perspective API、OpenAI Moderation 等基线。
- 开源权重，可作为 RLHF/agent 流水线的输入输出过滤器。

## 原始链接
- url: https://arxiv.org/abs/2312.06674
- pdf_url: https://arxiv.org/pdf/2312.06674

## 一手源存档（sources/）
- llama-guard.pdf  （PDF 不入 git，走 HF bucket）
