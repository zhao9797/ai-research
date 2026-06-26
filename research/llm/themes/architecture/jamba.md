---
title: "Jamba: A Hybrid Transformer-Mamba Language Model"
org: AI21 Labs
country: other
date: 2024-03
type: report
categories: [架构]
url: https://arxiv.org/abs/2403.19887
pdf_url: https://arxiv.org/pdf/2403.19887
github_url: https://huggingface.co/ai21labs/Jamba-v0.1
downloaded: [jamba.pdf]
---

## 一句话定位
Jamba 是首个生产级 Transformer-Mamba 混合 MoE 大模型：交替堆叠 Mamba 层、注意力层和 MoE 层，52B 总参/12B 激活，单卡 80GB 支持 256K 上下文。

## 摘要（3-6 句）
Jamba 把 Transformer 注意力层、Mamba（SSM）层和 MoE 层按比例交替堆叠成混合架构，兼顾 Transformer 的高质量与 Mamba 的高吞吐、低显存。该混合让模型在长上下文下显存占用远低于纯 Transformer。Jamba 总参数 52B、每 token 激活 12B，支持 256K 上下文，单张 80GB GPU 即可放下，并在标准基准上与同规模模型相当或更优，同时吞吐更高。模型以开放权重发布。

## 关键技术细节
- 架构 block：每个 Jamba block 含若干层，按比例混合 attention : Mamba ≈ 1:7，并周期性插入 MoE 层。
- 规模：52B 总参 / 12B 激活；16 专家、每 token top-2。
- 长上下文：支持 256K token；混合 SSM 大幅降低 KV cache，单 80GB GPU 可处理 140K+ 上下文。
- 吞吐：长上下文下吞吐显著高于同规模纯 Transformer。
- 开放权重发布（Apache 2.0）。

## 原始链接
- url: https://arxiv.org/abs/2403.19887
- pdf_url: https://arxiv.org/pdf/2403.19887
- github_url: https://huggingface.co/ai21labs/Jamba-v0.1

## 一手源存档（sources/）
- jamba.pdf  （PDF 不入 git，走 HF bucket）
