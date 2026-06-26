---
title: "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"
org: Carnegie Mellon University / Princeton University
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
Mamba 给 SSM 加入「选择性」（参数随输入变化）和硬件感知并行扫描，无注意力、无 MLP，线性复杂度，3B 模型匹敌两倍大的 Transformer，推理吞吐高 5 倍。

## 摘要（3-6 句）
此前的次二次架构（线性注意力、门控卷积、SSM）在语言上始终不及注意力，根因是无法做基于内容的推理。Mamba 让 SSM 参数（B、C、Δ）成为输入的函数（selective SSM），从而能按当前 token 选择性地传播或遗忘信息。由于这破坏了卷积形式，作者设计了硬件感知的并行扫描算法（在 recurrent 模式下高效）。Mamba 去掉注意力和 MLP，推理吞吐为 Transformer 的 5 倍、随序列线性扩展，可处理百万长度序列；Mamba-3B 在语言建模上超过同规模 Transformer，匹敌两倍大的模型。

## 关键技术细节
- 选择性 SSM (S6)：Δ、B、C 由输入投影得到，赋予 SSM 内容感知的选择能力（选择性遗忘/传播）。
- 硬件感知并行扫描：用 kernel fusion + 重计算在 SRAM 中做 selective scan，避免实例化大状态张量，GPU 高效。
- 架构：把 SSM 融入单一 Mamba block（结合门控 MLP），堆叠成无 attention、无独立 MLP 的网络。
- 性能：推理吞吐 ×5（vs Transformer），序列线性扩展，达百万长度；Mamba-3B 超同规模、匹敌 2× Transformer。
- 跨模态：语言、音频、基因组均 SOTA 级。
- 作者：Albert Gu、Tri Dao。

## 原始链接
- url: https://arxiv.org/abs/2312.00752
- pdf_url: https://arxiv.org/pdf/2312.00752
- github_url: https://github.com/state-spaces/mamba

## 一手源存档（sources/）
- mamba.pdf  （PDF 不入 git，走 HF bucket）
