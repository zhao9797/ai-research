---
title: "Jamba: A Hybrid Transformer-Mamba Language Model"
org: AI21 Labs
country: US
date: 2024-03
type: paper
categories: [架构]
url: https://arxiv.org/abs/2403.19887
pdf_url: https://arxiv.org/pdf/2403.19887
github_url:
downloaded: [2403.19887.pdf]
---

## 一句话定位
Jamba：首个大规模混合 Transformer-Mamba + MoE 架构基础模型，单 80GB GPU 可放下，支持 256K 上下文。

## 摘要
Jamba 是基于新型混合 Transformer-Mamba MoE 架构的基础大模型：交错排列 Transformer 块与 Mamba 块，兼得两类模型优点；在部分层加入 MoE 以提升容量而控制激活参数。这种灵活架构可按资源/目标定制配置；其实现配置可装进单张 80GB GPU。相比纯 Transformer，Jamba 吞吐高、显存占用小，同时在标准基准与长上下文评测上达 SOTA，支持最长 256K 上下文。文中研究了如何组合 Transformer/Mamba 层、如何混合专家等架构决策。权重以宽松许可公开。

## 关键技术细节
- 架构：Jamba block = 交错的 Transformer 层与 Mamba（SSM）层，比例 1:7（每 8 层 1 个 attention）；部分 MLP 替换为 MoE。
- MoE：16 个专家，每 token 选 top-2。
- 规模：52B 总参数、12B 激活参数；单 80GB GPU 可部署（256K 上下文）。
- 长上下文：支持 256K token；混合架构显著降低 KV cache 与显存。
- 吞吐：长上下文下吞吐远高于同规模纯 Transformer（如 Mixtral）。

## 原始链接
- url: https://arxiv.org/abs/2403.19887
- pdf_url: https://arxiv.org/pdf/2403.19887

## 一手源存档（sources/）
- [2403.19887.pdf](https://arxiv.org/pdf/2403.19887)  （arXiv 原文 PDF，不入 git）
