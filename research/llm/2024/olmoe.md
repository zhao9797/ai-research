---
title: "OLMoE: Open Mixture-of-Experts Language Models"
org: Allen Institute for AI (AI2)
country: US
date: 2024-09
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2409.02060
pdf_url: https://arxiv.org/pdf/2409.02060
github_url: https://github.com/allenai/OLMoE
downloaded: [2409.02060.pdf]
---

## 一句话定位
OLMoE：完全开放的稀疏 MoE 语言模型，1B 激活 / 7B 总参数，开源权重、数据、代码、日志，并系统分析 MoE 路由专长。

## 摘要
OLMoE 是利用稀疏 MoE 的完全开放 SOTA 模型。OLMoE-1B-7B 总参数 7B，每 token 仅用 1B。在 5T token 上预训练并进一步适配出 OLMoE-1B-7B-Instruct。它超过所有同等激活参数的可用模型，甚至超过更大的 Llama2-13B-Chat 与 DeepSeekMoE-16B。论文给出大量 MoE 训练实验、分析模型路由（显示高度专长），并开源全部内容：权重、训练数据、代码与日志。

## 关键技术细节
- MoE 架构：64 个细粒度专家、每 token 选 top-8；1B 激活 / 7B 总参数。
- 训练：5T token 预训练；含 load balancing loss 与 router z-loss。
- 关键 MoE 发现：细粒度专家 + dropless（无 token drop）路由优于共享专家等方案；专家高度专长（领域/词汇）。
- 全开放：权重 + 数据 + 训练代码 + 日志 + 中间检查点。
- 性能：超同激活参数模型，胜 Llama2-13B-Chat、DeepSeekMoE-16B。

## 原始链接
- url: https://arxiv.org/abs/2409.02060
- pdf_url: https://arxiv.org/pdf/2409.02060
- github: https://github.com/allenai/OLMoE

## 本地落盘文件
- ../../../sources/llm/2024/2409.02060.pdf
