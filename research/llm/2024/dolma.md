---
title: "Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research"
org: Allen Institute for AI (AI2)
country: US
date: 2024-01
type: paper
categories: [预训练数据]
url: https://arxiv.org/abs/2402.00159
pdf_url: https://arxiv.org/pdf/2402.00159
github_url: https://github.com/allenai/dolma
downloaded: [2402.00159.pdf]
---

## 一句话定位
Dolma：3 万亿 token 的开放英文预训练语料，连同数据构建文档与开源 curation 工具包发布，支撑 OLMo 训练。

## 摘要
当前最优模型的预训练语料信息很少公开：商业模型不披露数据，开放模型也常不放训练数据/复现配方。为推动 LM 预训练科学研究，AI2 策划并发布 Dolma —— 一个 3T token 英文语料，来自网页、科学论文、代码、公版图书、社交媒体、百科等多样混合。论文详尽记录设计原则、构建细节与内容统计，给出 Dolma 中间态的分析与实验，分享重要的数据 curation 实践，并开源整套 curation 工具包以支持复现与大规模数据研究。

## 关键技术细节
- 规模：约 3T token（来源：Common Crawl 网页、The Stack 代码、peS2o 论文、Project Gutenberg 图书、Reddit、Wikipedia/Wikibooks）。
- pipeline：语言识别 → 质量过滤 → 内容过滤 → 去重（URL/文档/段落级，Bloom filter）→ PII 处理 → 去毒。
- 工具：开源高性能 Rust curation 工具包（dolma toolkit）。
- 配套消融：对过滤/去重等做对照实验，指导后续 FineWeb、DCLM 等工作。
- 用途：OLMo 系列的训练数据基础。

## 原始链接
- url: https://arxiv.org/abs/2402.00159
- pdf_url: https://arxiv.org/pdf/2402.00159
- github: https://github.com/allenai/dolma

## 本地落盘文件
- ../../../sources/llm/2024/2402.00159.pdf
