---
title: Mamba: Linear-Time Sequence Modeling with Selective State Spaces
org: Carnegie Mellon / Princeton
country: US
date: 2023-12
type: paper
categories: [架构]
url: https://arxiv.org/abs/2312.00752
pdf_url: https://arxiv.org/pdf/2312.00752
github_url: https://github.com/state-spaces/mamba
downloaded: [mamba.pdf]
---

## 一句话定位
选择性状态空间(SSM)的 Mamba，无注意力线性扩展、推理 5x 吞吐，2023 末最重要的非 Transformer 架构。

## 摘要
多数基础模型基于 Transformer 注意力。亚二次架构(线性注意力、门控卷积、SSM)在长序列上更省算但语言上不及注意力。本文指出关键弱点是无法做 content-based 推理，提出改进：(1)让 SSM 参数随输入变化(选择机制)，可按当前 token 选择性传播/遗忘信息；(2)设计硬件感知的并行扫描算法。整合为无注意力、无 MLP 的简化架构 Mamba：推理 5x 吞吐、序列长度线性扩展，可到百万长度；语言上 Mamba-3B 超同尺寸 Transformer、匹配 2x 大模型。

## 关键技术细节
- 核心：Selective State Space Model(S6)——SSM 的 A/B/C/Δ 参数成为输入的函数，实现选择性记忆。
- 硬件感知算法：用 parallel scan（而非卷积）在 GPU SRAM 中做 recurrence，避免物化大状态。
- 架构：去掉 attention 与 MLP，统一为 Mamba block；线性时间/显存。
- 性能：推理吞吐 5x Transformer；可处理至 1M token 序列。
- 语言：Mamba-3B 超同尺寸 Transformer，匹配 6.9B Transformer（pretrain+下游）。
- 跨模态：语言、音频、基因组学均 SOTA。

## 原始链接
- url: https://arxiv.org/abs/2312.00752
- pdf_url: https://arxiv.org/pdf/2312.00752
- github_url: https://github.com/state-spaces/mamba

## 本地落盘文件
- ../../../sources/llm/2023/mamba.pdf
