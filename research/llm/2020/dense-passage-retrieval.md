---
title: Dense Passage Retrieval for Open-Domain Question Answering (DPR)
org: Meta / Facebook AI Research (FAIR), University of Washington, Princeton
country: US
date: 2020-04
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2004.04906
pdf_url: https://arxiv.org/pdf/2004.04906
github_url: https://github.com/facebookresearch/DPR
downloaded: [arxiv-2004.04906.pdf]
---

## 一句话定位
DPR 证明用简单的双塔 BERT 编码器学习稠密向量检索即可大幅超越传统 BM25 稀疏检索，成为 RAG/REALM 等检索增强大模型的标准检索组件。

## 摘要（3-6 句）
DPR 用两个独立的 BERT 编码器分别把问题和段落映射到稠密向量，用点积相似度 + 最大内积搜索（MIPS）做检索，仅用相对少量问答对训练。相比 BM25，DPR 在 top-20 检索准确率上绝对提升 9-19 个百分点，并使端到端开放域 QA 在多个基准上达到新 SOTA。论文的训练技巧（in-batch negatives + 困难负样本）成为稠密检索训练的范式。

## 关键技术细节
- 结构：双塔（dual-encoder）——question encoder 与 passage encoder 各为独立 BERT，取 [CLS] 表示。
- 相似度：向量点积；用 FAISS 做 MIPS 在 2100 万 Wikipedia 段落中检索。
- 训练：对比学习，in-batch negatives（同 batch 其他问题的正段落作负例）+ BM25 困难负样本。
- 数据：用 Natural Questions、TriviaQA、WebQuestions、CuratedTrec、SQuAD 的问答对训练（无需额外预训练目标）。
- 结果：top-20 检索准确率较 BM25 高 9-19 个点；端到端 QA 在多个开放域基准达 SOTA。
- 是 RAG 检索器的基础组件。

## 原始链接
- url: https://arxiv.org/abs/2004.04906
- pdf_url: https://arxiv.org/pdf/2004.04906
- github_url: https://github.com/facebookresearch/DPR

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2004.04906.pdf
