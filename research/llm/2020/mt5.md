---
title: mT5 — A massively multilingual pre-trained text-to-text transformer
org: Google Research
country: US
date: 2020-10
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2010.11934
pdf_url: https://arxiv.org/pdf/2010.11934
github_url: https://github.com/google-research/multilingual-t5
downloaded: [arxiv-2010.11934.pdf]
---

## 一句话定位
mT5 是 T5 的多语言版本，在覆盖 101 种语言的 mC4 语料上预训练，最大 13B 参数，是当时最强的多语言 text-to-text 预训练模型。

## 摘要（3-6 句）
mT5 沿用 T5 的统一“text-to-text”框架与架构，在新构建的 mC4 多语言语料（101 种语言，来自 Common Crawl）上预训练。模型规模从 small 到 13B（XXL），在多项多语言基准（XNLI、XQuAD、MLQA、TyDi QA、PAWS-X、WikiAnn NER）上取得 SOTA。论文还分析并缓解了零样本跨语言生成中的“意外翻译”（accidental translation）问题。

## 关键技术细节
- 架构：T5（encoder-decoder Transformer），统一 text-to-text 目标（span corruption 去噪）。
- 规模：small (300M) / base (580M) / large (1.2B) / XL (3.7B) / XXL (13B)。
- 数据：mC4 语料，101 种语言，源自 Common Crawl；用 SentencePiece 训练统一词表（约 250K wordpiece，覆盖所有语言）。
- 语言采样：用温度系数 α=0.3 的指数平滑对高/低资源语言重采样平衡。
- 下游：XNLI、XQuAD、MLQA、TyDi QA、PAWS-X、WikiAnn NER 等多语言任务 SOTA。
- 提出缓解“意外翻译”（zero-shot 生成时误翻成英语）的方法。

## 原始链接
- url: https://arxiv.org/abs/2010.11934
- pdf_url: https://arxiv.org/pdf/2010.11934
- github_url: https://github.com/google-research/multilingual-t5

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2010.11934.pdf
