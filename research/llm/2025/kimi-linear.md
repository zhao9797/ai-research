---
title: Kimi Linear: An Expressive, Efficient Attention Architecture
org: 月之暗面 Moonshot AI
country: China
date: 2025-10
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2510.26692
pdf_url: https://arxiv.org/pdf/2510.26692
github_url: https://github.com/MoonshotAI/Kimi-Linear
downloaded: [kimi-linear.pdf]
---

## 一句话定位
首个在短上下文、长上下文与 RL scaling 等场景下都公平超过 full attention 的混合线性注意力架构，核心是 Kimi Delta Attention (KDA)。发布 2025-10-30。

## 摘要
Kimi Linear 是混合线性注意力架构，首次在公平对比下于短上下文、长上下文、RL scaling 多场景超越 full attention。核心是 Kimi Delta Attention (KDA)——一种表达力强的线性注意力模块，扩展 Gated DeltaNet 引入更细粒度的门控，更有效利用有限的有限状态 RNN 记忆。配套 chunkwise 算法通过 DPLR（Diagonal-Plus-Low-Rank）转移矩阵的专门变体实现高硬件效率，大幅降低计算。相比 full attention 可减少 KV cache 并提升长上下文吞吐。

## 关键技术细节
- KDA：扩展 Gated DeltaNet 的细粒度门控线性注意力，提升有限状态记忆利用。
- 混合架构：KDA 线性层与少量 full attention 层混合（hybrid）。
- 硬件高效算法：基于 DPLR 转移矩阵的 chunkwise 算法，显著降低计算量。
- 收益：减少 KV cache，提升长上下文解码吞吐；短/长上下文与 RL scaling 全面优于 full attention。
- 开源：模型与 kernel 代码于 GitHub MoonshotAI/Kimi-Linear。

## 原始链接
- url: https://arxiv.org/abs/2510.26692
- pdf_url: https://arxiv.org/pdf/2510.26692
- github_url: https://github.com/MoonshotAI/Kimi-Linear

## 本地落盘文件
- ../../../sources/llm/2025/kimi-linear.pdf
