---
title: "Hymba: A Hybrid-head Architecture for Small Language Models"
org: NVIDIA
country: US
date: 2024-11
type: paper
categories: [架构]
url: https://arxiv.org/abs/2411.13676
pdf_url: https://arxiv.org/pdf/2411.13676
github_url: https://huggingface.co/nvidia/Hymba-1.5B-Base
downloaded: [hymba.pdf]
---

## 一句话定位
Hymba 是 NVIDIA 的小模型混合架构：在同一层并行放注意力头（高分辨率回忆）与 SSM 头（高效上下文摘要），加可学习 meta token，Hymba-1.5B 超过所有 2B 以下公开模型。

## 摘要（3-6 句）
Hymba 是面向小语言模型的混合头并行架构，把 Transformer 注意力机制与状态空间模型 (SSM) 在同一层融合：注意力头提供高分辨率回忆，SSM 头做高效上下文摘要。论文还引入可学习的 meta token，预置到 prompt 前存储关键信息，缓解注意力「被迫关注」负担。再结合跨层 KV 共享与部分滑动窗口注意力，缩小 cache。开发中作者在相同设置下做了受控架构对比，发现该架构显著占优。Hymba-1.5B-Base 超过所有 sub-2B 公开模型，甚至超过 Llama-3.2-3B（更小且 cache 更省、吞吐更高）。

## 关键技术细节
- 混合头并行（hybrid-head parallel）：每层内注意力头与 Mamba SSM 头并行处理同一输入后融合，而非层间交替。
- meta tokens：可学习的前置 token（如 128 个），充当「注册表/记忆」，提升回忆并稳定注意力分布。
- 缓存优化：cross-layer KV sharing + 大部分层用 sliding window attention，仅少数层全局 → 小 KV cache。
- 结果：Hymba-1.5B-Base 在 sub-2B 公开模型中 SOTA；相比 Llama-3.2-3B，cache 约 1/11、吞吐约 3.5×。
- 作者：Xin Dong、Yonggan Fu、Pavlo Molchanov、Jan Kautz 等（NVIDIA）。

## 原始链接
- url: https://arxiv.org/abs/2411.13676
- pdf_url: https://arxiv.org/pdf/2411.13676
- github_url: https://huggingface.co/nvidia/Hymba-1.5B-Base

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/hymba.pdf
