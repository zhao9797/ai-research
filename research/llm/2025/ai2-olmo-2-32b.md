---
title: OLMo 2 32B - First fully open model to outperform GPT-3.5 and GPT-4o mini
org: Allen Institute for AI (AI2)
country: US
date: 2025-03
type: blog
categories: [预训练数据, 后训练, AI infra]
url: https://allenai.org/blog/olmo2-32B
pdf_url:
github_url: https://github.com/allenai/OLMo
downloaded: [files/ai2-olmo-2-32b-blog.md]
---

## 一句话定位
AI2 2025-03-13 发布的 OLMo 2 32B 官方博客：OLMo 2 家族最大、最强模型，宣称首个在多技能学术基准上超越 GPT-3.5-Turbo 与 GPT-4o mini 的"完全开放"模型，训练算力仅同级一小部分。

## 摘要
OLMo 2 32B 把 OLMo 2 训练配方扩到 32B：训练至 6T tokens，用 Tülu 3.1 做后训练。它是首个完全开放（数据/代码/权重/细节全公开）且在一套多技能学术基准上超越 GPT-3.5-Turbo 与 GPT-4o mini 的模型，性能逼近 Qwen 2.5 72B / Llama 3.1-3.3 70B，而训练成本仅为 Qwen 2.5 32B 的约三分之一。7B/13B/32B 全家族均可在单个 H100 GPU 节点上微调。

## 关键技术细节（带数字）
- 参数：32B（OLMo 2 家族最大）。
- 预训练：训练至 6T tokens（沿用 11 月 7B/13B 的 OLMo 2 配方扩展）。
- 后训练：Tülu 3.1。
- 算力：训练成本约为 Qwen 2.5 32B 的 1/3（达到相近性能）；FLOPs 以 Kaplan et al. 2020 近似估算（pretrain + mid-train 阶段）。
- 性能：首个 fully-open 模型超越 GPT-3.5-Turbo 与 GPT-4o mini；逼近 Qwen 2.5 72B、Llama 3.1/3.3 70B。
- 可在单张 H100 GPU 节点上微调全部 7B/13B/32B。
- 完全开放：数据、代码、权重、细节全部公开；配套 tech report arXiv:2501.00656。
- 发布日期：2025-03-13。

## 原始链接
- 官方博客：https://allenai.org/blog/olmo2-32B
- tech report：https://arxiv.org/abs/2501.00656

## 本地落盘文件
- ../../../sources/llm/2025/ai2-olmo-2-32b-blog.md
