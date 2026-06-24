---
title: "MegaBlocks: Efficient Sparse Training with Mixture-of-Experts"
org: Stanford / Microsoft / Google
country: US
date: 2022-11
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2211.15841
pdf_url: https://arxiv.org/pdf/2211.15841
github_url: https://github.com/databricks/megablocks
downloaded: [megablocks-2211.15841.pdf, ]
---

## 一句话定位
把 MoE 计算重构为块稀疏（block-sparse）矩阵乘，用定制 GPU kernel 避免 token 丢弃与填充，使 MoE 训练既不掉 token 又高效。

## 摘要（3-6 句）
传统 MoE 因 expert capacity 限制要么丢弃 token、要么 padding 浪费算力，二者都损害质量或效率。MegaBlocks 把 MoE 的可变规模专家计算表达为 block-sparse 运算，并实现高性能 block-sparse GEMM kernel（基于其 dropless-MoE 公式），无需丢 token 或填充。相比 Tutel 端到端训练快最高 40%、相比 Megatron-LM dense 快约 2.4×，且因不丢 token 质量更好。被 Databricks（DBRX）等用于生产 MoE 训练。

## 关键技术细节
- dropless-MoE（dMoE）：把每个 expert 的变长输入组织为 block-sparse 矩阵，无 capacity 丢弃/padding。
- 定制 block-sparse GEMM kernel（基于 blocked-CSR），高效处理不规则专家负载。
- 性能：vs Tutel 最高 +40% 端到端训练加速；vs Megatron dense 约 2.4×。
- 开源（现归 databricks/megablocks），支撑 DBRX 等 MoE 模型训练。

## 原始链接
- url: https://arxiv.org/abs/2211.15841
- pdf_url: https://arxiv.org/pdf/2211.15841
- github_url: https://github.com/databricks/megablocks

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/megablocks-2211.15841.pdf
