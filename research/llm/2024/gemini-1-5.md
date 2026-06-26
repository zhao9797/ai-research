---
title: "Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context"
org: Google DeepMind
country: US
date: 2024-03
type: report
categories: [架构]
url: https://arxiv.org/abs/2403.05530
pdf_url: https://arxiv.org/pdf/2403.05530
github_url:
downloaded: [2403.05530.pdf]
---

## 一句话定位
Gemini 1.5 技术报告：高算力效率的多模态 MoE 模型，把长上下文推到至少 10M token 且近乎完美召回，远超同期 Claude 3（200K）与 GPT-4 Turbo（128K）。

## 摘要
报告介绍 Gemini 1.5 系列：能跨数百万 token 上下文（含多文档、数小时视频/音频）召回与推理的高算力效率多模态模型。含更新版 Gemini 1.5 Pro 与更轻量的 Gemini 1.5 Flash。在跨模态长上下文检索上近乎完美召回，刷新长文档 QA、长视频 QA、长上下文 ASR 的 SOTA，并匹配或超过 Gemini 1.0 Ultra。研究长上下文极限时发现，next-token 预测持续改善、召回率在至少 10M token 仍 >99%。还展示给定一本 Kalamang（<200 使用者）语法手册即可达到人类学习者水平的英→Kalamang 翻译这类涌现能力。

## 关键技术细节
- 架构：稀疏 MoE Transformer（多模态）；Pro 与 Flash 两档（Flash 经在线蒸馏）。
- 上下文：标准支持至 1M（Pro）/ 实验至 10M token；10M 仍 >99% NIAH 召回。
- 跨模态长上下文：可处理数小时视频、数十小时音频、数百万 token 文本/代码。
- 涌现：仅凭语法书学会极低资源语言翻译（MTOB 基准）。
- 与同期对比：上下文长度为 Claude 3.0（200K）、GPT-4 Turbo（128K）的数量级跨越。

## 原始链接
- url: https://arxiv.org/abs/2403.05530
- pdf_url: https://arxiv.org/pdf/2403.05530

## 一手源存档（sources/）
- [2403.05530.pdf](https://arxiv.org/pdf/2403.05530)  （arXiv 原文 PDF，不入 git）
