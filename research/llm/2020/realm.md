---
title: REALM — Retrieval-Augmented Language Model Pre-Training
org: Google Research
country: US
date: 2020-02
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2002.08909
pdf_url: https://arxiv.org/pdf/2002.08909
github_url: https://github.com/google-research/language/tree/master/language/realm
downloaded: [arxiv-2002.08909.pdf]
---

## 一句话定位
REALM 首次在预训练阶段就端到端学习一个神经检索器，让语言模型在掩码预测时从大规模语料中检索并利用外部文档，是检索增强语言模型（RAG 路线）的开创性工作。

## 摘要（3-6 句）
REALM 在掩码语言建模预训练中引入一个可学习的知识检索器：模型先从一个文本知识库（如 Wikipedia）检索相关文档，再以检索到的文档为条件预测被掩码的词。检索器与语言模型联合端到端训练（检索作为隐变量，通过对掩码预测的边际似然反向传播）。在开放域问答（Natural Questions、WebQuestions、CuratedTrec）上，REALM 显著超过当时最大的 T5 等模型，且参数量更小、可解释性更好。

## 关键技术细节
- 结构：神经检索器（基于 BERT 的双塔/最大内积搜索 MIPS）+ 知识增强编码器。
- 训练目标：掩码语言建模，检索文档作为隐变量，对边际似然反向传播来训练检索器。
- 关键工程：检索索引随训练异步刷新（每数百步重建 MIPS 索引），用最大内积搜索（MIPS）从 1300 万级文档块中检索 top-k。
- 知识库：Wikipedia（约 1300 万文档块）。
- 下游：开放域 QA 微调（Natural Questions、WebQuestions、CuratedTrec），以更少参数超过 T5-11B 等大模型 4-16 个点。
- 提出 salient span masking（掩盖命名实体/日期等显著片段）以引导模型学习世界知识。

## 原始链接
- url: https://arxiv.org/abs/2002.08909
- pdf_url: https://arxiv.org/pdf/2002.08909

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2002.08909.pdf
