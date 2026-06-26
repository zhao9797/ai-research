---
title: "Skywork: A More Open Bilingual Foundation Model"
org: 昆仑万维 · 天工（Kunlun · Skywork Team）
country: China
date: 2023-10
type: paper
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2310.19341
pdf_url: https://arxiv.org/pdf/2310.19341
github_url: https://github.com/SkyworkAI/Skywork
downloaded: [skywork-13b.pdf, skywork-readme.md]
---

## 一句话定位
昆仑万维 Skywork-13B（3.2T token 双语训练）技术报告，开源 SkyPile-150B 中文语料与中间检查点，并提出数据泄漏检测方法。

## 摘要（3-6 句）
Skywork-13B 是一组在 3.2 万亿 token 中英文语料上训练的 13B 大模型，是同规模中训练最充分、最开放的模型之一。采用两阶段训练（通用训练→领域增强训练）的分段语料方法。模型在中文语言建模多领域达到 SOTA。报告提出一种新的数据泄漏（测试集污染）检测方法，并开源 Skywork-13B、训练中间检查点，以及 SkyPile 语料中超 150B token 的高质量中文网页文本（已知最大开源中文数据集）。

## 关键技术细节
- 规模与数据：13B 参数；预训练 3.2T token（中英为主 + 代码）；构建 SkyPile 语料总量 >6T token。
- 两阶段训练：Stage-1 通用训练，Stage-2 领域增强（STEM 等）训练，分段语料。
- 开源数据集 SkyPile-150B：约 600GB、~150B token 高质量中文网页文本（强调以质量为先而非单纯去重）。
- Tokenizer：BPE；在 LLaMA 词表基础上加入 BERT 的 8000 单字符 token 并扩充常用词，最终词表 65,536（17 个保留）。
- 子模型：Skywork-13B-Base / Chat / Math / MM（多模态），均有量化版本支持消费级 GPU。
- Math 模型：13B 规模中 GSM8K 排名第一，MATH、CMATH 表现优异。
- 数据泄漏检测：提出基于语言模型 loss 的污染检测方法，揭示业界测试集污染问题。
- 开放训练监控：以 loss 为核心性能指标，公开多阶段中间 checkpoint。

## 原始链接
- url: https://arxiv.org/abs/2310.19341
- pdf_url: https://arxiv.org/pdf/2310.19341
- github_url: https://github.com/SkyworkAI/Skywork

## 一手源存档（sources/）
- skywork-13b.pdf  （PDF 不入 git，走 HF bucket）
- [skywork-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/skywork-readme.md)
