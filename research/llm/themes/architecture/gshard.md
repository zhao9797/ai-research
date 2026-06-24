---
title: "GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding"
org: Google
country: US
date: 2020-06
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2006.16668
pdf_url: https://arxiv.org/pdf/2006.16668
downloaded: [gshard.pdf]
---

## 一句话定位
GShard 把稀疏门控 MoE 引入 Transformer 并配合自动分片，训练出 600B 参数的多语言翻译模型，是现代大规模 MoE 训练基建的奠基作。

## 摘要（3-6 句）
GShard 用条件计算（Mixture-of-Experts）和自动分片把 Transformer 扩展到 6000 亿参数。它在 Transformer 的 FFN 层插入稀疏门控 MoE 层，每个 token 只路由到 top-2 专家。通过 GShard 注解 + XLA SPMD 编译器实现专家在数千加速器上的自动并行（expert parallelism），通信与计算高效重叠。在 100 种语言到英语的翻译上，600B MoE 模型用 4 天、2048 个 TPU v3 完成训练，质量与效率都远超稠密基线。

## 关键技术细节
- 规模：最大 600B 参数 MoE Transformer；2048 TPU v3 训练约 4 天。
- 路由：每层 MoE 用 top-2 gating，每个 token 选 2 个专家；引入 expert capacity、辅助 load balancing loss、random routing。
- 并行：专家并行（expert parallelism）+ 自动分片，通过 GShard API 给张量加 sharding 注解，XLA SPMD 自动生成分布式程序。
- 任务：覆盖 100 语言→英语的大规模多语种翻译，质量随专家数扩展持续提升。
- 是 Switch Transformer、GLaM、DeepSeekMoE 等后续 MoE 工作的直接前身。

## 原始链接
- url: https://arxiv.org/abs/2006.16668
- pdf_url: https://arxiv.org/pdf/2006.16668

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/gshard.pdf
