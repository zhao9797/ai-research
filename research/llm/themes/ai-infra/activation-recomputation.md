---
title: Reducing Activation Recomputation in Large Transformer Models
org: NVIDIA
country: US
date: 2022-05
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2205.05198
pdf_url: https://arxiv.org/pdf/2205.05198
github_url: https://github.com/NVIDIA/Megatron-LM
downloaded: [activation-recomputation-2205.05198.pdf]
---

## 一句话定位
提出序列并行（sequence parallelism）与选择性激活重计算（selective activation recomputation），大幅降低 Transformer 训练激活显存，几乎免去全量重计算的算力开销。

## 摘要（3-6 句）
大模型训练常用全量激活重计算来省显存，但带来约 30-40% 额外算力。本文提出两项技术：序列并行把 LayerNorm/dropout 等沿序列维切分以与张量并行协同减少激活显存；选择性重计算只重算占显存大而算力小的注意力部分。组合后将激活显存降低约 5×，把重计算开销从全量的 ~36% 降到 ~2%。在 530B 参数 MT-NLG 量级模型上把训练吞吐提升明显。

## 关键技术细节
- Sequence Parallelism（SP）：在张量并行的非 TP 区域沿序列维分片 LayerNorm、dropout、残差，用 all-gather/reduce-scatter 替代部分 all-reduce，激活显存随 TP 度下降。
- Selective recompute：只重算 attention 中 softmax/dropout/QK^T 等 memory-heavy 但 FLOP-light 的部分。
- 效果：激活显存约降 5×；重计算算力开销从约 36% 降至约 2%；22B/175B/530B/1T 模型上验证。
- 已合入 Megatron-LM，是后续大模型训练的标配。

## 原始链接
- url: https://arxiv.org/abs/2205.05198
- pdf_url: https://arxiv.org/pdf/2205.05198
- github_url: https://github.com/NVIDIA/Megatron-LM

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/activation-recomputation-2205.05198.pdf
