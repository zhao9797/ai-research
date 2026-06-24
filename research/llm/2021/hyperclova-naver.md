---
title: "What Changes Can Large-scale Language Models Bring? Intensive Study on HyperCLOVA: Billions-scale Korean Generative Pretrained Transformers"
org: NAVER
country: other
date: 2021-09
type: paper
categories: [预训练数据, 后训练]
url: https://arxiv.org/abs/2109.04650
pdf_url: https://arxiv.org/pdf/2109.04650
github_url:
downloaded: [arxiv-2109.04650.pdf]
---

## 一句话定位
韩国 NAVER 的 HyperCLOVA：首个面向韩语的十亿至千亿级 GPT-3 式生成模型，用 NAVER 自有大规模韩语语料训练，并探索 prompt-based 学习与 in-context 调优。

## 摘要（3-6 句）
HyperCLOVA 研究大规模语言模型能为非英语（韩语）带来哪些变化。基于以韩语为中心的大规模语料训练 GPT-3 式自回归模型，验证其 in-context learning 能力。论文还提出针对性的 prompt 优化与 prompt-based learning 流程，并讨论以大模型为中心构建 No-Code AI 平台的可能。是非英语母语大模型的代表性一手工作。

## 关键技术细节
- 由 NAVER CLOVA / NAVER AI Lab / NAVER Search 等联合完成。
- 模型族：十亿到千亿级（billions-scale）韩语 GPT 系；最大达 82B 级（论文报告多档规模）。
- 语料：NAVER 自建的大规模韩语语料（以韩语为主，区别于英语为主的 GPT-3）。
- 方法：探索 prompt-based learning、prompt tuning、in-context learning 在韩语上的效果。
- 配套韩语专用 tokenizer（morpheme-aware BPE 方向）。
- 强调大模型对非英语生态与产业（No-Code AI）的意义。

## 原始链接
- url: https://arxiv.org/abs/2109.04650
- pdf_url: https://arxiv.org/pdf/2109.04650

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2109.04650.pdf
