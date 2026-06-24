---
title: "Gated Delta Networks: Improving Mamba2 with Delta Rule"
org: NVIDIA / MIT CSAIL
country: US
date: 2024-12
type: paper
categories: [架构]
url: https://arxiv.org/abs/2412.06464
pdf_url: https://arxiv.org/pdf/2412.06464
github_url: https://github.com/NVlabs/GatedDeltaNet
downloaded: [gated-deltanet.pdf]
---

## 一句话定位
Gated DeltaNet 把「门控」（自适应记忆擦除）与「delta 更新规则」（精确记忆修改）结合，超过 Mamba2 和 DeltaNet，是 Qwen3-Next 等混合线性架构采用的递归单元。

## 摘要（3-6 句）
线性 Transformer 是高效替代品，但在检索与长上下文上受限。近期两种机制各有所长：gating（自适应记忆控制，可快速擦除）与 delta update rule（精确定向记忆修改）。作者发现两者互补，提出 gated delta rule，并给出面向现代硬件的并行训练算法。所得架构 Gated DeltaNet 在语言建模、常识推理、in-context 检索、长度外推、长上下文理解等多个基准上一致超过 Mamba2 与 DeltaNet。进一步把 Gated DeltaNet 层与滑动窗口注意力/Mamba2 混合得到更强的混合模型。

## 关键技术细节
- gated delta rule：状态更新同时含门控衰减项（α_t，控制遗忘）与 delta 规则项（β_t·(v_t − S k_t)k_t^T，定向纠正记忆）。
- 并行训练算法：chunkwise（基于 WY 表示 / flash-linear-attention 后端）高效训练。
- 超过 Mamba2、DeltaNet：语言建模困惑度、检索（MQAR）、长度外推、长上下文均更优。
- 混合变体：Gated DeltaNet + 滑动窗口注意力（H-类）进一步提升回忆能力。
- 作者：Songlin Yang、Jan Kautz、Ali Hatamizadeh（NVIDIA + MIT）；ICLR 2025。
- 该递归单元被 Qwen3-Next 等后续混合架构采用。

## 原始链接
- url: https://arxiv.org/abs/2412.06464
- pdf_url: https://arxiv.org/pdf/2412.06464
- github_url: https://github.com/NVlabs/GatedDeltaNet

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/gated-deltanet.pdf
