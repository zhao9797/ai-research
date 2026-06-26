---
title: "GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding"
org: Google
country: US
date: 2020-06
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2006.16668
pdf_url: https://arxiv.org/pdf/2006.16668
github_url:
downloaded: [arxiv-2006.16668.pdf]
---

## 一句话定位
Google 用稀疏 MoE（Mixture-of-Experts）+ 自动分片把多语言翻译 Transformer 扩到 6000 亿参数，是工业级 MoE 大模型与自动并行的开创性工作。

## 摘要（3-6 句）
GShard 由一套轻量级的并行计算标注 API 和支持 SPMD 编译器（XLA）组成，让开发者只需对张量加少量分片注解即可自动把模型切分到上千个加速器上。论文用 GShard 训练了基于稀疏门控 MoE 的多语言机器翻译 Transformer，最大模型 6000 亿参数，在 100 种语言到英语的翻译上同时大幅超越双语基线，且训练成本（算力/时间）远低于稠密扩展。MoE 使得参数量增长但每个 token 的计算量基本不变（条件计算）。

## 关键技术细节
- 架构：Transformer encoder-decoder，将每隔一层的 FFN 替换为稀疏门控 MoE 层（Sparsely-Gated Mixture-of-Experts）。
- 最大模型：600B 参数，每个 MoE 层最多 2048 个专家，模型共 36 层（encoder/decoder 各若干 MoE 层）。
- 路由：top-2 gating（每个 token 路由到 2 个专家），带专家容量（capacity factor）和负载均衡辅助损失。
- 条件计算：尽管 600B 参数，每个 token 实际只激活 2 个专家，计算量与远小的稠密模型相当。
- 训练规模：在 2048 个 TPU v3 核心上训练，600B 模型约 4 天训练完成（约 22 TPU v3 core-years）。
- 并行：专家并行（每个专家放在不同设备）+ 数据并行；通过 XLA SPMD 自动分片，注解式 API（split/replicate/shard）。
- 数据：覆盖 100 种语言到英语的网络规模平行语料（总计约 250 亿训练样本对）。

## 原始链接
- url: https://arxiv.org/abs/2006.16668
- pdf_url: https://arxiv.org/pdf/2006.16668

## 一手源存档（sources/）
- [arxiv-2006.16668.pdf](https://arxiv.org/pdf/2006.16668)  （arXiv 原文 PDF，不入 git）
