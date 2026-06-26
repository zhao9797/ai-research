---
title: "Atlas: Few-shot Learning with Retrieval Augmented Language Models"
org: Meta AI
country: US
date: 2022-08
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2208.03299
pdf_url: https://arxiv.org/pdf/2208.03299
github_url: https://github.com/facebookresearch/atlas
downloaded: [atlas.pdf]
---

## 一句话定位
Meta 的检索增强语言模型 Atlas：用远小的参数 + 可更新文档索引，在 few-shot 知识密集任务上媲美甚至超越超大模型。

## 摘要
大模型在多任务上 few-shot 表现亮眼，但知识密集任务（QA、事实核查）通常需要巨量参数来存储知识。检索增强模型以少得多的参数在知识密集任务上表现优异，但其在 few-shot 设置下是否有效尚不清楚。Atlas 是精心设计并预训练的检索增强语言模型，能用极少训练样本学习知识密集任务。在 MMLU、KILT、NaturalQuestions 等广泛任务上评测，研究文档索引内容的影响并显示索引可轻松更新。仅用 64 个样本即在 NaturalQuestions 上达到 42%+ 准确率。

## 关键技术细节
- 架构：检索器（Contriever，dense retriever）+ 阅读器（T5/Fusion-in-Decoder，11B）联合预训练。
- few-shot：64 例即在 NQ 上 >42%，超过 540B PaLM（参数少约 50 倍）。
- 可更新知识：文档索引可热更新，无需重训模型即引入新知识——区别于参数化记忆。
- 联合预训练：检索器与阅读器用 MLM/PLM 目标联合训练，研究多种检索器监督方式（如 attention distillation）。
- 在 MMLU 上 few-shot 表现强；KILT 多任务 SOTA。
- 意义：RAG 在 few-shot 与可更新知识上的早期系统性论证。

## 原始链接
- url: https://arxiv.org/abs/2208.03299
- pdf_url: https://arxiv.org/pdf/2208.03299
- github_url: https://github.com/facebookresearch/atlas

## 一手源存档（sources/）
- atlas.pdf  （PDF 不入 git，走 HF bucket）
