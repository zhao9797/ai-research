---
title: "MiniMax Sparse Attention"
org: MiniMax (稀宇科技)
country: China
date: 2026-06
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2606.13392
pdf_url: https://arxiv.org/pdf/2606.13392
github_url: ""
downloaded: [minimax-sparse-attention.pdf]
---

## 一句话定位
MiniMax 提出的 blockwise 稀疏注意力 MSA，建立在 GQA 之上，用轻量 Index Branch 为每个 GQA 组独立选 Top-k KV 块，配合 GPU 执行路径把稀疏性转成真实加速，用于超长上下文。

## 摘要
MiniMax Sparse Attention（MSA，arXiv 2026-06-11，作者 Xunhao Lai 等 17 人）针对前沿 LLM 不可或缺的超长上下文能力（agentic workflow、仓库级代码推理、持久记忆都需要对几十万到上百万 token 联合注意）而设计，以解决 softmax 注意力的二次成本。MSA 是建立在 Grouped Query Attention（GQA）之上的 blockwise 稀疏注意力：轻量 Index Branch 对 KV 块打分并为每个 GQA 组独立选 Top-k 子集（组特定稀疏检索 + 块级高效执行）；Main Branch 仅对选中块做精确 block-sparse attention。强调简洁与可扩展，便于在多种 GPU 上高效部署。MSA 与 GPU 执行路径协同设计——exp-free Top-k 选择 + KV-outer sparse attention 提升 tensor-core 利用率。在 109B 参数、原生多模态训练模型上验证。

## 关键技术细节
- **基座**：建立在 Grouped Query Attention (GQA) 之上的 blockwise sparse attention。
- **Index Branch**：轻量分支为 KV 块打分，为每个 GQA group 独立选 Top-k 块（group-specific 稀疏检索）。
- **Main Branch**：仅对选中块做精确 block-sparse attention。
- **AI infra-GPU 协同**：exp-free Top-k 选择 + KV-outer sparse attention，提升 tensor-core 利用率（block 粒度访问下）。
- **验证规模**：109B 参数、native multimodal training 的模型上验证（性能与全注意力持平的前提下加速）。
- **目标场景**：数十万至百万 token 的 agentic / 代码 / 长记忆推理。

## 原始链接
- url: https://arxiv.org/abs/2606.13392
- pdf_url: https://arxiv.org/pdf/2606.13392

## 本地落盘文件
- ../../../sources/llm/2026/minimax-sparse-attention.pdf
