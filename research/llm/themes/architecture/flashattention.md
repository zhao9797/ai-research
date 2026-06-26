---
title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
org: Stanford University / SUNY Buffalo
country: US
date: 2022-05
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2205.14135
pdf_url: https://arxiv.org/pdf/2205.14135
github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [flashattention.pdf]
---

## 一句话定位
FlashAttention 用 tiling + IO 感知把精确注意力的 HBM 读写降到次二次，既快又省显存，成为现代 LLM 训练/推理的标准注意力 kernel。

## 摘要（3-6 句）
Transformer 在长序列上慢且耗显存，因为自注意力时间和显存随长度二次增长。此前近似注意力多以质量换算力，却常无法真正壁钟加速。FlashAttention 指出关键缺失原则是 IO 感知——考虑 GPU 不同层级显存（HBM vs SRAM）间的读写。它用 tiling 把 Q/K/V 分块放进片上 SRAM 计算、用 online softmax 避免实例化完整 N×N 注意力矩阵，从而减少 HBM 读写、实现精确（非近似）注意力。FlashAttention 显著加速训练（如 BERT、GPT-2）并支持更长上下文。

## 关键技术细节
- IO 感知：分析并最小化 HBM↔SRAM 读写次数，是真正的壁钟加速来源。
- tiling + online softmax：分块计算注意力，流式更新 softmax 归一化，不存完整 N×N 矩阵，显存从 O(N²) 降到 O(N)。
- recomputation：反向传播时重算注意力而非存中间结果，省显存。
- 精确：结果与标准注意力数值等价（非近似）。
- 加速：GPT-2 训练约 3× 加速；使长上下文（如 16K、64K）训练可行。
- 作者：Tri Dao 等；后续 FlashAttention-2/3 持续优化 GPU 利用率。

## 原始链接
- url: https://arxiv.org/abs/2205.14135
- pdf_url: https://arxiv.org/pdf/2205.14135
- github_url: https://github.com/Dao-AILab/flash-attention

## 一手源存档（sources/）
- flashattention.pdf  （PDF 不入 git，走 HF bucket）
