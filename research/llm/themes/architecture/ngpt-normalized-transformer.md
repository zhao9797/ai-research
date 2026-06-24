---
title: "nGPT: Normalized Transformer with Representation Learning on the Hypersphere"
org: NVIDIA
country: US
date: 2024-10
type: paper
categories: [架构]
url: https://arxiv.org/abs/2410.01131
pdf_url: https://arxiv.org/pdf/2410.01131
github_url: https://github.com/NVIDIA/ngpt
downloaded: [ngpt.pdf]
---

## 一句话定位
nGPT 把 Transformer 的所有向量（embedding、MLP、注意力矩阵、隐状态）都约束到单位超球面上，每层是球面上的一次位移，训练步数减少 4-20 倍。

## 摘要（3-6 句）
nGPT 提出在超球面上做表示学习的归一化 Transformer：embedding、MLP、注意力矩阵和隐状态的所有向量都做单位范数归一化。token 表示在超球面上「行走」，每层由注意力与 MLP 块给出一个朝目标输出的位移，这些位移分量也位于同一超球面。这种几何约束让优化更稳定，实验显示达到相同精度所需训练步数减少 4 到 20 倍（取决于序列长度）。

## 关键技术细节
- 全单位范数归一化：所有权重矩阵的行/列、embedding、隐状态都归一化到超球面。
- 层更新视为球面上向目标的可学习步长（eigen learning rate）位移，用 SLERP/线性插值近似。
- 去掉 LayerNorm/RMSNorm 和权重衰减（归一化天然约束尺度）。
- 收敛：相同精度训练步数减少约 4×–20×（序列越长收益越大）。
- 作者：Ilya Loshchilov、Cheng-Ping Hsieh、Simeng Sun、Boris Ginsburg（NVIDIA）。

## 原始链接
- url: https://arxiv.org/abs/2410.01131
- pdf_url: https://arxiv.org/pdf/2410.01131
- github_url: https://github.com/NVIDIA/ngpt

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/ngpt.pdf
