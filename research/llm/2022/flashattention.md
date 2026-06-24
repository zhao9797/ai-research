---
title: FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
org: Stanford    country: US    date: 2022-05    type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2205.14135    pdf_url: https://arxiv.org/pdf/2205.14135    github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [flashattention.pdf]
---

## 一句话定位
IO-aware 的精确注意力算法：用 tiling 减少 HBM↔SRAM 读写，使注意力既快又省显存，成为长上下文与大模型训练的基础设施。

## 摘要
Transformer 在长序列上慢且耗显存，因自注意力的时间/显存复杂度对序列长度是二次的。近似注意力虽降复杂度却常牺牲质量且无壁钟加速。本文指出关键缺失原则是让注意力算法"IO-aware"——考虑 GPU 各级显存间的读写。提出 FlashAttention：用 tiling 减少 GPU HBM 与片上 SRAM 之间的读写次数，是精确（非近似）注意力。分析其 IO 复杂度，证明所需 HBM 访问更少，并对一定 SRAM 大小最优。还扩展出 block-sparse FlashAttention。

## 关键技术细节
- 核心思想：kernel fusion + tiling + recomputation，避免在 HBM 上物化 N×N 注意力矩阵；softmax 用 online/streaming 方式分块计算。
- 显存：从 O(N^2) 降到 O(N) 线性显存。
- 速度：BERT-large 端到端训练比 MLPerf 1.1 记录快 15%；GPT-2 训练快 3 倍；长序列注意力本身最高快 7.6 倍。
- 使更长上下文可行（论文展示在 Path-X 16K、Path-256 64K 序列上首次取得高于随机的结果）。
- block-sparse 版进一步加速近似注意力。
- 后续成为 PyTorch、几乎所有大模型训练/推理栈的默认注意力实现（FlashAttention-2/3 续作）。

## 原始链接
- url: https://arxiv.org/abs/2205.14135
- pdf_url: https://arxiv.org/pdf/2205.14135
- github_url: https://github.com/Dao-AILab/flash-attention

## 本地落盘文件
- ../../../sources/llm/2022/flashattention.pdf
