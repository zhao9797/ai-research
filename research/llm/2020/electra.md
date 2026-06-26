---
title: ELECTRA — Pre-training Text Encoders as Discriminators Rather Than Generators
org: Google Brain / Stanford
country: US
date: 2020-03
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2003.10555
pdf_url: https://arxiv.org/pdf/2003.10555
github_url: https://github.com/google-research/electra
downloaded: [arxiv-2003.10555.pdf]
---

## 一句话定位
ELECTRA 用“替换 token 检测”（RTD）替代 BERT 的掩码语言建模，让预训练在所有 token 上都产生学习信号，从而以远低的算力达到甚至超过 BERT/RoBERTa 的效果。

## 摘要（3-6 句）
ELECTRA 提出一种更高效的判别式预训练任务：用一个小的生成器对部分 token 做掩码替换，再训练主模型（判别器）逐 token 判断每个位置是“原始”还是“被替换”。由于损失作用于全部 token（而非 BERT 仅 15% 的掩码位置），样本效率大幅提升。在相同算力下 ELECTRA 显著优于 BERT/XLNet/RoBERTa；ELECTRA-small 单 GPU 训练 4 天即超过用 30 倍算力的 GPT；ELECTRA-large 在 GLUE、SQuAD 上达到 SOTA。

## 关键技术细节
- 任务：Replaced Token Detection (RTD)——生成器（小型 MLM）替换部分 token，判别器对每个 token 做二分类（原始/替换）。
- 全 token 损失：所有位置都参与训练，而 BERT 仅在 15% 掩码位置学习，故样本效率高。
- 生成器与判别器共享 token embedding；生成器规模约为判别器 1/4-1/2 时最优。
- 规模：small / base / large；ELECTRA-small 在单块 GPU 上 4 天训练即超过 GPT（约 1/30 算力）。
- ELECTRA-large 用约 1/4 RoBERTa 算力达到相近 GLUE，并在 SQuAD 2.0 上刷新 SOTA。
- 数据：与 BERT/RoBERTa 相同语料（Wikipedia + BookCorpus，large 用更大语料）。

## 原始链接
- url: https://arxiv.org/abs/2003.10555
- pdf_url: https://arxiv.org/pdf/2003.10555
- github_url: https://github.com/google-research/electra

## 一手源存档（sources/）
- [arxiv-2003.10555.pdf](https://arxiv.org/pdf/2003.10555)  （arXiv 原文 PDF，不入 git）
