---
title: Reducing Activation Recomputation in Large Transformer Models
org: NVIDIA    country: US    date: 2022-05    type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2205.05198    pdf_url: https://arxiv.org/pdf/2205.05198    github_url: https://github.com/NVIDIA/Megatron-LM
downloaded: [reducing-activation-recomputation.pdf]
---

## 一句话定位
NVIDIA 提出序列并行 + 选择性激活重计算，几乎消除大模型训练中的激活重算开销，是 Megatron-LM 的关键 infra 进步。

## 摘要
训练大 Transformer 是现代 AI 最重要的计算挑战之一。激活重计算（activation recomputation）常用于绕过显存限制——不保存反向所需激活而是重算，省显存但增加冗余计算。本文证明大部分冗余计算其实不必要：提出两个简单技术——序列并行（sequence parallelism）与选择性激活重计算（selective activation recomputation）。配合张量并行，几乎无需重算激活。在最大达 1 万亿参数规模的模型上验证。

## 关键技术细节
- 序列并行（SP）：在 LayerNorm、Dropout 等非张量并行区域沿序列维切分激活，与张量并行（TP）正交组合，降低每卡激活显存。
- 选择性激活重计算：只对显存占用大但重算便宜的部分（如注意力 softmax/dropout）重算，保留其余激活，平衡显存与算力。
- 效果：相比全量重计算，将激活重算开销从约 30%+ 训练时间降到约 2%；在 530B 模型上端到端训练吞吐提升约 29%。
- 在最高 1T 参数模型上验证；MFU（模型 FLOPs 利用率）显著提升。
- 已合入 Megatron-LM，成为后续超大模型训练标配。

## 原始链接
- url: https://arxiv.org/abs/2205.05198
- pdf_url: https://arxiv.org/pdf/2205.05198
- github_url: https://github.com/NVIDIA/Megatron-LM

## 本地落盘文件
- ../../../sources/llm/2022/reducing-activation-recomputation.pdf
