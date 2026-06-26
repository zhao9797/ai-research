---
title: The Pile — An 800GB Dataset of Diverse Text for Language Modeling
org: EleutherAI
country: US
date: 2020-12
type: paper
categories: [预训练数据]
url: https://arxiv.org/abs/2101.00027
pdf_url: https://arxiv.org/pdf/2101.00027
github_url: https://github.com/EleutherAI/the-pile
downloaded: [arxiv-2101.00027.pdf, eleuther-the-pile.html]
---

## 一句话定位
EleutherAI 开源的 825 GiB 多样化英文语料 The Pile，由 22 个高质量子数据集组成，是开源大模型（GPT-Neo/GPT-J/GPT-NeoX 等）预训练数据的事实标准。

## 摘要（3-6 句）
The Pile 是一个 825 GiB（约 800GB）的多样化开源语言建模数据集，由 22 个较小的高质量子数据集合并而成，强调来源多样性（学术、网络、对话、代码、医学、法律等）以提升通用语言模型的跨域能力。论文给出数据集构成、去重与清洗方法，并通过在 The Pile 上评测 GPT-2/GPT-3 说明现有模型在多样化文本上仍有提升空间。该数据集托管于 the-eye，arXiv 论文于 2020-12 提交（编号 2101.00027）。

## 关键技术细节
- 规模：825.18 GiB 文本（约 800GB），由 22 个子集组成。
- 代表性子集：Pile-CC（清洗版 Common Crawl）、PubMed Central、ArXiv、GitHub（代码）、FreeLaw、Stack Exchange、USPTO、PubMed Abstracts、Wikipedia(en)、OpenWebText2、Books3、Project Gutenberg(PG-19)、OpenSubtitles、YouTube字幕、DM Mathematics、Ubuntu IRC、EuroParl、HackerNews、PhilPapers、NIH ExPorter、Enron Emails 等。
- 设计理念：来源多样性优于单一网络爬取，提升下游通用性与知识覆盖。
- 处理：各子集独立清洗，按质量赋采样权重；做了文档级去重。
- 评测：用 The Pile 的测试集评估 GPT-2/GPT-3，提出新的多域困惑度基准（BPB，bits per byte）。
- 用途：成为 GPT-Neo（2021）、GPT-J、GPT-NeoX、以及众多开源 LLM 的预训练语料。

## 原始链接
- url: https://arxiv.org/abs/2101.00027
- pdf_url: https://arxiv.org/pdf/2101.00027
- 官方站: https://pile.eleuther.ai/
- github_url: https://github.com/EleutherAI/the-pile

## 一手源存档（sources/）
- [arxiv-2101.00027.pdf](https://arxiv.org/pdf/2101.00027)  （arXiv 原文 PDF，不入 git）
- [eleuther-the-pile.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2020/eleuther-the-pile.html)
