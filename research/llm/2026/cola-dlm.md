---
title: "Continuous Latent Diffusion Language Model (Cola-DLM)"
org: 字节跳动 Seed (ByteDance Seed)
country: China
date: 2026-05
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2605.06548
pdf_url: https://arxiv.org/pdf/2605.06548
github_url: https://github.com/ByteDance-Seed/Cola-DLM
downloaded: [cola-dlm.pdf]
---

## 一句话定位
字节 Seed 的 Cola-DLM，层次化连续潜空间扩散语言模型，用 Text VAE + block-causal DiT prior 组合，通过 Flow Matching 在连续文本潜空间上做扩散建模。

## 摘要
Cola-DLM（Continuous Latent Diffusion Language Model，arXiv 2026-05-07，作者 Hongcan Guo 等 11 人，ByteDance Seed）是一个层次化的连续潜空间扩散语言模型。它把 Text VAE 与 block-causal Diffusion Transformer (DiT) prior 结合：VAE 把文本映射为连续潜序列并把潜变量解码回 token，DiT 则通过 Flow Matching 在潜空间做先验传输（latent prior transport）。这条路线偏离主流离散 token 自回归/掩码扩散，探索在连续潜空间上以扩散方式建模语言。HF ByteDance-Seed 官方组织发布 checkpoint（createdAt 2026-05-15），含 ColaDiTModel 与 ColaTextVAEModel 两部分。

## 关键技术细节
- **架构-两组件**：(1) ColaTextVAEModel——Text VAE，文本↔连续潜序列双向映射（编码 + 条件解码）；(2) ColaDiTModel——block-causal 1-D Diffusion Transformer prior，over 连续文本潜变量。
- **建模方式**：DiT 通过 Flow Matching 做 latent prior transport（潜先验传输）。
- **范式**：连续潜空间扩散语言模型（区别于离散 token AR / 掩码扩散）。
- **层次化**：hierarchical continuous latent-space diffusion。
- **开源**：HF ByteDance-Seed + GitHub ByteDance-Seed/Cola-DLM；项目页 hongcanguo.github.io/Cola-DLM。

## 原始链接
- url: https://arxiv.org/abs/2605.06548
- pdf_url: https://arxiv.org/pdf/2605.06548
- github_url: https://github.com/ByteDance-Seed/Cola-DLM

## 本地落盘文件
- ../../../sources/llm/2026/cola-dlm.pdf
