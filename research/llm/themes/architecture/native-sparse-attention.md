---
title: "Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (NSA)"
org: DeepSeek-AI / Peking University / University of Washington
country: China/US
date: 2025-02
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2502.11089
pdf_url: https://arxiv.org/pdf/2502.11089
downloaded: [native-sparse-attention.pdf]
---

## 一句话定位
NSA 是 DeepSeek 提出的「原生可训练」稀疏注意力：分层（压缩 + 选择 + 滑窗）+ 硬件对齐 kernel，端到端可训练，长上下文训练/推理大幅加速且不掉点。

## 摘要（3-6 句）
长上下文建模重要但标准注意力计算昂贵。NSA 把算法创新与硬件对齐优化结合，实现高效长上下文。它用动态分层稀疏策略：粗粒度 token 压缩 + 细粒度 token 选择 + 局部滑动窗口三分支并行，兼顾全局上下文与局部精度。两大创新：(1) 算术强度平衡的算法设计 + 实现优化带来实际加速；(2) 端到端可训练（原生稀疏），降低预训练算力而不牺牲性能。在 27B（约 3B 激活）模型上，NSA 在通用基准、长上下文、指令推理上匹配或超过全注意力，且 64K 长度下前向/反向/解码均显著加速。

## 关键技术细节
- 三分支：① compression（把 token 块压成代表 token，提供全局视野）；② selection（按块重要性选 top-n 块做细粒度注意力）；③ sliding window（局部）。三分支输出门控融合。
- 原生可训练：所有分支可微，预训练即学稀疏模式，避免「先全注意力训练再稀疏化」的不一致。
- 硬件对齐：为 GQA/MLA 设计 arithmetic-intensity-balanced 的 Triton kernel，块大小匹配 Tensor Core 与内存访问。
- 验证：27B 总参（约 3B 激活）MoE，260B token 预训练；64K 上下文下相对 FlashAttention-2 大幅加速，质量不降。
- 作者含 Jingyang Yuan、Damai Dai、Wenfeng Liang 等（DeepSeek + 北大）。

## 原始链接
- url: https://arxiv.org/abs/2502.11089
- pdf_url: https://arxiv.org/pdf/2502.11089

## 一手源存档（sources/）
- native-sparse-attention.pdf  （PDF 不入 git，走 HF bucket）
