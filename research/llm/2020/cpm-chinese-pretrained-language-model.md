---
title: CPM — A Large-scale Generative Chinese Pre-trained Language Model
org: 清华大学 / 北京智源人工智能研究院 (BAAI) — TsinghuaAI
country: China
date: 2020-12
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2012.00413
pdf_url: https://arxiv.org/pdf/2012.00413
github_url: https://github.com/TsinghuaAI/CPM-1-Generate
downloaded: [arxiv-2012.00413.pdf]
---

## 一句话定位
CPM（Chinese Pretrained Model）是中国首个大规模生成式中文预训练语言模型，26 亿参数、100GB 中文语料，常被视为“中文版 GPT-3 起点”，由清华 + 智源联合发布并开源权重。

## 摘要（3-6 句）
CPM 针对 GPT-3 不开源且以英文为主的现状，构建了大规模中文预训练生成模型。最大版本 26 亿参数，在 100GB 中文语料上预训练，采用为中文设计的子词词表（结合分词避免纯字符序列过长）。CPM 在对话、作文、完形填空、问答等多个中文下游任务上具备强 few-shot/zero-shot 能力，且代码与模型参数公开，推动了中文大模型生态。

## 关键技术细节
- 架构：GPT 式 Transformer decoder（自回归语言模型）。
- 规模谱系：CPM-Small (109M) / CPM-Medium (334M) / CPM-Large (2.6B) 参数；CPM-Large 32 层。
- 训练数据：约 100GB 中文语料（百科、网页、电子书、新闻、对话等）。
- 中文 tokenizer：先用分词器分词再构建子词词表（约 3 万词表），避免直接按字导致序列过长，提升中文建模效率。
- 训练 infra：在 NVIDIA V100 GPU 上、基于 Megatron-LM 风格模型并行训练。
- 下游能力：few-shot/zero-shot 文本分类、对话、问答、完形填空、作文生成、实体生成等中文任务。
- 开源：模型权重与代码公开（GitHub TsinghuaAI/CPM-1-Generate）。

## 原始链接
- url: https://arxiv.org/abs/2012.00413
- pdf_url: https://arxiv.org/pdf/2012.00413
- github_url: https://github.com/TsinghuaAI/CPM-1-Generate

## 一手源存档（sources/）
- [arxiv-2012.00413.pdf](https://arxiv.org/pdf/2012.00413)  （arXiv 原文 PDF，不入 git）
