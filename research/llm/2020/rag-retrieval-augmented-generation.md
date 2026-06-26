---
title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (RAG)
org: Meta / Facebook AI Research (FAIR), UCL
country: US
date: 2020-05
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2005.11401
pdf_url: https://arxiv.org/pdf/2005.11401
github_url: https://github.com/huggingface/transformers/tree/main/examples/research_projects/rag
downloaded: [arxiv-2005.11401.pdf]
---

## 一句话定位
RAG 提出把参数化记忆（预训练 seq2seq 模型 BART）与非参数化记忆（可微检索的稠密向量索引 Wikipedia）结合的通用框架，奠定了“检索增强生成”这一术语与范式。

## 摘要（3-6 句）
RAG 把预训练的参数化生成器（BART）与非参数化外部记忆（基于 DPR 检索的稠密 Wikipedia 索引）端到端结合：给定输入用检索器取 top-k 文档，再以这些文档为条件由生成器产生输出。论文提出两种变体 RAG-Sequence（整段用同一组文档）与 RAG-Token（每个 token 可用不同文档）。在开放域问答（NQ、WebQ、CuratedTrec、TriviaQA）上刷新 SOTA，并在事实校验、生成式问答等知识密集任务上比纯参数化基线更准确、更具体、幻觉更少。

## 关键技术细节
- 组成：检索器 = DPR（稠密双塔，question encoder + 预编码文档索引，MIPS 检索）；生成器 = BART-large（参数化记忆）。
- 两种变体：RAG-Sequence（同一文档集生成整个序列）、RAG-Token（逐 token 边际化不同文档）。
- 知识库：Wikipedia，约 2100 万 100 词文档块，FAISS MIPS 索引。
- 训练：question encoder 与生成器联合微调，文档编码器与索引固定（避免重建索引）。
- 检索作为隐变量，对 top-k 文档做边际化。
- 结果：开放域 QA（NQ/WebQ/CuratedTrec）SOTA；生成更具事实性，幻觉少于 BART。
- 可通过替换索引实现知识更新（无需重训生成器）。

## 原始链接
- url: https://arxiv.org/abs/2005.11401
- pdf_url: https://arxiv.org/pdf/2005.11401

## 一手源存档（sources/）
- [arxiv-2005.11401.pdf](https://arxiv.org/pdf/2005.11401)  （arXiv 原文 PDF，不入 git）
