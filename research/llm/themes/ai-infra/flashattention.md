---
title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
org: Stanford / Dao-AILab
country: US
date: 2022-05
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2205.14135
pdf_url: https://arxiv.org/pdf/2205.14135
github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [flashattention-2205.14135.pdf]
---

## 一句话定位
IO 感知的精确注意力算法，通过分块（tiling）+ kernel fusion 避免把 N×N 注意力矩阵写回 HBM，使注意力又快又省显存，是现代 LLM 训练/推理的基础 kernel。

## 摘要（3-6 句）
标准注意力把巨大的 N×N 中间矩阵反复读写 HBM，受显存带宽瓶颈。FlashAttention 用 tiling 把 Q/K/V 分块加载到 SRAM，在片上完成 softmax 与累加（online softmax），并用重计算在反向避免存中间矩阵，从而减少 HBM 访问、得到精确（非近似）结果。相对 PyTorch 实现，GPT-2 训练提速约 3×，BERT-large 比 MLPerf 记录快 15%，并把可行上下文从数千扩到 16K/64K。FlashAttention 已成为事实标准 kernel。

## 关键技术细节
- 核心：block-wise tiling + online softmax（运行时维护 running max/sum）+ kernel fusion，HBM 访问从 O(N^2) 降到 O(N^2/M)（M 为 SRAM 大小）。
- 反向用重计算（不存 attention 矩阵），显存随序列长度线性。
- 加速：GPT-2 端到端约 3× 训练加速；长序列上 Long-Range Arena 提速 2.4×。
- 精确注意力（exact），非稀疏/低秩近似。

## 原始链接
- url: https://arxiv.org/abs/2205.14135
- pdf_url: https://arxiv.org/pdf/2205.14135
- github_url: https://github.com/Dao-AILab/flash-attention

## 一手源存档（sources/）
- [flashattention-2205.14135.pdf](https://arxiv.org/pdf/2205.14135)  （arXiv 原文 PDF，不入 git）
