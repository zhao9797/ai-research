---
title: "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM"
org: NVIDIA / Stanford / Microsoft Research
country: US
date: 2021-04
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2104.04473
pdf_url: https://arxiv.org/pdf/2104.04473
github_url: https://github.com/NVIDIA/Megatron-LM
downloaded: [arxiv-2104.04473.pdf]
---

## 一句话定位
NVIDIA Megatron-LM 的 3D 并行扩展论文：提出 interleaved pipeline schedule，组合张量 + 流水 + 数据并行，在 3072 张 A100 上以 502 petaFLOP/s（52% 峰值利用率）训练万亿参数模型。

## 摘要（3-6 句）
论文研究如何在 GPU 集群上高效训练超大语言模型，组合张量并行（tensor）、流水并行（pipeline）与数据并行（data），并提出新的 interleaved pipelining schedule 降低气泡（bubble）。在 3072 张 GPU 上对 1 万亿参数模型可达 502 petaFLOP/s 的聚合吞吐（每 GPU 52% 峰值），相对此前方法在千卡规模显著提升扩展性。系统建立在 NVIDIA DGX A100 服务器之上。

## 关键技术细节
- 3D 并行：tensor-slicing + pipeline + data parallelism 组合（PTD-P）。
- 创新：interleaved（virtual pipeline）调度，减少 pipeline bubble，提升吞吐。
- 规模/吞吐：1T 参数模型在 3072 × A100 上 502 petaFLOP/s，per-GPU 52% 峰值利用率。
- 硬件：NVIDIA DGX A100（8×80GB A100/节点）。
- 给出各并行维度的 tradeoff 分析与最优配置指引。
- 是 MT-NLG 530B 与众多大模型训练的并行方法论基础；代码 NVIDIA/Megatron-LM。
- 发表于 SC'21。

## 原始链接
- url: https://arxiv.org/abs/2104.04473
- pdf_url: https://arxiv.org/pdf/2104.04473
- github_url: https://github.com/NVIDIA/Megatron-LM

## 一手源存档（sources/）
- [arxiv-2104.04473.pdf](https://arxiv.org/pdf/2104.04473)  （arXiv 原文 PDF，不入 git）
