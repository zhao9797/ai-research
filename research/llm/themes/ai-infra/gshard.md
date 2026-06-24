---
title: GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding
org: Google
country: US
date: 2020-06
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2006.16668
pdf_url: https://arxiv.org/pdf/2006.16668
downloaded: [gshard-2006.16668.pdf]
---

## 一句话定位
首个把 MoE（条件计算）与自动分片（automatic sharding）结合、训练 6000 亿参数稀疏多语言翻译模型的系统性工作，奠定大规模 MoE 工程范式。

## 摘要（3-6 句）
GShard 用一组轻量级 sharding API（注解张量切分）让编译器自动把模型并行到上千加速器。作者用它训练了 600B 参数的稀疏门控 MoE Transformer 翻译模型，在 2048 TPU v3 上 4 天完成，覆盖 100 种语言到英语的翻译，质量全面超过双语基线。论文提出 expert 容量因子、辅助负载均衡损失、随机路由等 MoE 稳定化技巧，成为后续所有 MoE 系统的基础。

## 关键技术细节
- MoE 层：每个 token 经门控选 top-2 expert；expert 沿设备分片（expert parallelism）。
- 负载均衡：auxiliary load-balancing loss、expert capacity（含溢出丢弃）、random dispatch。
- 规模：600B 参数 MoE，2048×TPU v3 训练 4 天；对比 96 层 dense 模型质量更优而成本更低。
- sharding API（split/replicate）+ XLA SPMD partitioner 自动生成通信，是 GSPMD 的前身。

## 原始链接
- url: https://arxiv.org/abs/2006.16668
- pdf_url: https://arxiv.org/pdf/2006.16668

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/gshard-2006.16668.pdf
