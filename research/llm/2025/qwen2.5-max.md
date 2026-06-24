---
title: "Qwen2.5-Max: Exploring the Intelligence of Large-scale MoE Model"
org: 阿里巴巴 Qwen Team
country: China
date: 2025-01
type: blog
categories: [预训练数据, 架构, 后训练]
url: https://qwenlm.github.io/blog/qwen2.5-max/
pdf_url:
github_url:
downloaded: [qwen2.5-max-blog.html]
---

## 一句话定位
阿里大规模 MoE 旗舰 Qwen2.5-Max，预训练超 20T token，对标 DeepSeek-V3 / GPT-4o / Claude-3.5-Sonnet。发布 2025-01-28。

## 摘要
官方博客介绍 Qwen2.5-Max：一个超大规模 MoE 模型，在 20T+ token 上预训练，并经过精选 SFT 与 RLHF 后训练。博客公布其在 MMLU-Pro、LiveCodeBench、LiveBench、Arena-Hard、GPQA-Diamond 等 benchmark 上与 DeepSeek-V3、GPT-4o、Claude-3.5-Sonnet 等领先模型的对比，base 模型对比开源 DeepSeek-V3 / Llama-3.1-405B / Qwen2.5-72B。通过阿里云 API 提供。

## 关键技术细节
- 架构：大规模 Mixture-of-Experts (MoE)。
- 预训练数据：超过 20 万亿（20T+）tokens。
- 后训练：精选 SFT + RLHF。
- 对标：DeepSeek-V3、GPT-4o、Claude-3.5-Sonnet（instruct）；base 对比 DeepSeek-V3、Llama-3.1-405B、Qwen2.5-72B。
- 交付：Alibaba Cloud API + Qwen Chat（未开源权重）。

## 原始链接
- url: https://qwenlm.github.io/blog/qwen2.5-max/

## 本地落盘文件
- ../../../sources/llm/2025/qwen2.5-max-blog.html
