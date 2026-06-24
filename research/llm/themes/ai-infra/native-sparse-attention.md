---
title: "Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention"
org: DeepSeek-AI / Peking University / University of Washington
country: China
date: 2025-02
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2502.11089
pdf_url: https://arxiv.org/pdf/2502.11089
downloaded: [native-sparse-attention-2502.11089.pdf]
---

## 一句话定位
DeepSeek 提出的可端到端训练的硬件对齐稀疏注意力 NSA，结合粗粒度 token 压缩与细粒度 token 选择，在长上下文下兼顾效率与质量。

## 摘要（3-6 句）
NSA 用动态分层稀疏策略：粗粒度 token 压缩（保全局）+ 细粒度 token 选择（保局部精度）+ 滑动窗口分支。两项关键创新：算术强度平衡的算法设计配合硬件优化实现可观加速；支持端到端原生训练（而非仅推理稀疏），从而在预训练阶段就省算力且不掉点。实验显示用 NSA 预训练的模型在通用、长上下文与指令推理基准上与 Full Attention 持平或更优，前向/反向与解码均显著提速。

## 关键技术细节
- 三分支：compressed（块级压缩 KV）、selected（动态选 top-n 块）、sliding window（局部）；门控融合。
- 硬件对齐：blockwise 选择保证 Tensor Core 友好的算术强度，定制 Triton kernel。
- 原生可训练：稀疏掩码可微/可学习，预训练即用，省 pretraining compute。
- 长上下文（如 64K）下相对 Full Attention 大幅加速且质量不降。

## 原始链接
- url: https://arxiv.org/abs/2502.11089
- pdf_url: https://arxiv.org/pdf/2502.11089

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/native-sparse-attention-2502.11089.pdf
