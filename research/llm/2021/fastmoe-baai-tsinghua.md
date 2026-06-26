---
title: "FastMoE: A Fast Mixture-of-Expert Training System"
org: 清华 (Tsinghua) / BAAI 智源
country: China
date: 2021-03
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2103.13262
pdf_url: https://arxiv.org/pdf/2103.13262
github_url: https://github.com/laekov/fastmoe
downloaded: [arxiv-2103.13262.pdf]
---

## 一句话定位
清华 + 智源的 FastMoE：首个基于 PyTorch 的开源分布式 MoE 训练系统，让 GPU/PyTorch 社区也能训练万亿级 MoE，不再依赖 Google TPU + Mesh TensorFlow——悟道 2.0 的底层 infra。

## 摘要（3-6 句）
FastMoE 是基于 PyTorch 的分布式 MoE 训练系统，填补此前唯一可用平台强依赖 Google TPU + Mesh TensorFlow、对 GPU/PyTorch 社区不开放的空白。系统支持把专家分布到多 GPU/多节点，提供灵活的专家定义接口与高性能 all-to-all 通信，可把模型扩到万亿参数。被用于训练智源悟道（WuDao）等大规模中文 MoE 模型。

## 关键技术细节
- 平台：PyTorch（开源），打破 TPU + Mesh TensorFlow 垄断。
- 分布式：支持专家在多 GPU / 多节点分片（expert parallelism），优化 all-to-all 通信。
- 提供灵活的 expert/gate 自定义接口，可嵌入现有 Transformer。
- 目标规模：万亿（trillion）参数 MoE。
- 是 BAAI 悟道 2.0（1.75T 参数）训练的底层系统之一；代码 laekov/fastmoe。
- 作者来自清华 + 智源（BAAI）+ Recurrent AI（Jie Tang/Zhilin Yang 等）。

## 原始链接
- url: https://arxiv.org/abs/2103.13262
- pdf_url: https://arxiv.org/pdf/2103.13262
- github_url: https://github.com/laekov/fastmoe

## 一手源存档（sources/）
- [arxiv-2103.13262.pdf](https://arxiv.org/pdf/2103.13262)  （arXiv 原文 PDF，不入 git）
