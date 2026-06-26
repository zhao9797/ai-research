---
title: "Improving language models by retrieving from trillions of tokens (RETRO)"
org: DeepMind
country: US
date: 2021-12
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2112.04426
pdf_url: https://arxiv.org/pdf/2112.04426
github_url:
downloaded: [arxiv-2112.04426.pdf]
---

## 一句话定位
DeepMind 的 RETRO：用 2 万亿 token 检索数据库 + chunked cross-attention 增强自回归语言模型，以 25 倍更少的参数达到 GPT-3/Jurassic-1 的水平——半参数化（检索增强）扩展路线的代表。

## 摘要（3-6 句）
RETRO（Retrieval-Enhanced Transformer）通过对从大型语料库检索到的文档块（document chunks）进行条件化来增强自回归语言模型，检索依据是与前文 token 的局部相似度。用 2 万亿 token 的数据库，RETRO 在 Pile 上达到与 GPT-3、Jurassic-1 相当的性能，但参数量少 25 倍。RETRO 结合冻结的 BERT 检索器、可微编码器与 chunked cross-attention 机制；既可从零训练，也可快速给已有 Transformer "加装"检索（RETROfit）。论文提出把"从大型文本数据库检索"作为扩展语言模型的互补路径。

## 关键技术细节
- 检索数据库：2 万亿（2 trillion）token。
- 参数效率：以 ~25× 更少参数达到 GPT-3/Jurassic-1 水平。
- 机制：把输入切成 chunk，按前一 chunk 检索相似文本，用 chunked cross-attention 注入当前 chunk 预测。
- 检索器：冻结的 BERT（frozen BERT retriever）做最近邻检索（不微调检索器）。
- RETROfit：可给预训练 Transformer 后加检索能力，无需从头训。
- 数据：MassiveText（与 Gopher 同源）作为检索库与训练集。
- 是"检索增强 / 半参数化"对抗"纯参数扩展"的关键一手论文。

## 原始链接
- url: https://arxiv.org/abs/2112.04426
- pdf_url: https://arxiv.org/pdf/2112.04426

## 一手源存档（sources/）
- [arxiv-2112.04426.pdf](https://arxiv.org/pdf/2112.04426)  （arXiv 原文 PDF，不入 git）
