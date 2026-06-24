---
title: "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity"
org: Google
country: US
date: 2021-01
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2101.03961
pdf_url: https://arxiv.org/pdf/2101.03961
github_url: https://github.com/google-research/t5x
downloaded: [arxiv-2101.03961.pdf]
---

## 一句话定位
Google 的 Switch Transformer：把 MoE 路由简化为每 token 只选 1 个专家（top-1），首次在 bfloat16 下稳定训练万亿参数稀疏模型。

## 摘要（3-6 句）
Switch Transformer 简化了 MoE 路由算法（每 token 只路由到单个专家），降低通信与计算开销，并通过训练技巧缓解稀疏模型的训练不稳定，首次实现用低精度（bfloat16）训练大型稀疏模型。基于 T5-Base/T5-Large 设计的模型在相同算力下可获得最高 7 倍的预训练加速，在 101 种语言的多语种设置下也优于 mT5-Base。论文进一步把语言模型规模推进到万亿参数级别（在 C4 上预训练），相对 T5-XXL 实现 4 倍加速。

## 关键技术细节
- 路由简化：每个 token 只发送到 1 个专家（top-1 routing，区别于此前 MoE 的 top-2/top-k）。
- 引入容量因子（capacity factor）与负载均衡损失（load balancing loss）控制专家负载。
- 首次以 bfloat16 低精度稳定训练大型稀疏 MoE。
- 相对 T5-Base/Large 预训练提速最多 7×；万亿参数 Switch-C 相对 T5-XXL 提速 4×。
- 多语种 mT5-Base 对比：101 种语言全部获益。
- 数据：C4（Colossal Clean Crawled Corpus）。
- 代码与全部 checkpoint 开源（google-research/t5x，原 Mesh TensorFlow / t5x）。
- 发表于 JMLR 23 (2022)，arXiv 首版 2021-01。

## 原始链接
- url: https://arxiv.org/abs/2101.03961
- pdf_url: https://arxiv.org/pdf/2101.03961
- github_url: https://github.com/google-research/t5x

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2101.03961.pdf
