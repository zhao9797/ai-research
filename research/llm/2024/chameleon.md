---
title: "Chameleon: Mixed-Modal Early-Fusion Foundation Models"
org: Meta (FAIR)
country: US
date: 2024-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2405.09818
pdf_url: https://arxiv.org/pdf/2405.09818
github_url: https://github.com/facebookresearch/chameleon
downloaded: [2405.09818.pdf]
---

## 一句话定位
Chameleon：early-fusion、基于 token 的混合模态模型，单一模型用统一 token 空间理解并生成任意交错的图文序列。

## 摘要
Chameleon 是一族 early-fusion、基于 token 的混合模态模型，能以任意顺序理解并生成图像与文本。论文给出从头开始的稳定训练方法、对齐配方、以及为 early-fusion token 化混合模态量身定制的架构参数化。在视觉问答、图像描述、文本生成、图像生成、长篇混合模态生成等任务上评测：Chameleon 展现广泛通用能力，在图像描述上 SOTA，纯文本上超过 Llama-2 并与 Mixtral 8x7B、Gemini-Pro 竞争，还能进行非平凡的图像生成——全在单一模型内。在新的长篇混合模态生成评测上，按人评匹配或超过 Gemini Pro 与 GPT-4V。

## 关键技术细节
- early-fusion：图像经 image tokenizer（VQ）量化为离散 token，与文本 token 共享同一 Transformer 与词表，统一自回归建模。
- 规模：7B 与 34B。
- 训练稳定性创新：QK-Norm、调整 LayerNorm 位置、dropout 等，解决混合模态大规模训练的发散问题。
- 能力：图文任意交错理解 + 生成；图像描述 SOTA；纯文本超 Llama-2。
- 与 late-fusion（如把视觉特征接入文本 LLM）路线对比，主打统一 token 空间。

## 原始链接
- url: https://arxiv.org/abs/2405.09818
- pdf_url: https://arxiv.org/pdf/2405.09818
- github: https://github.com/facebookresearch/chameleon

## 本地落盘文件
- ../../../sources/llm/2024/2405.09818.pdf
