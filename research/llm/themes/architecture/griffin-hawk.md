---
title: "Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models (Hawk & Griffin)"
org: Google DeepMind
country: US
date: 2024-02
type: paper
categories: [架构]
url: https://arxiv.org/abs/2402.19427
pdf_url: https://arxiv.org/pdf/2402.19427
downloaded: [griffin-hawk.pdf]
---

## 一句话定位
DeepMind 提出 Hawk（纯门控线性递归 RNN）和 Griffin（门控线性递归 + 局部注意力的混合），Griffin 用 6 倍更少的 token 就匹敌 Llama-2，是 RG-LRU 递归单元的代表作。

## 摘要（3-6 句）
RNN 推理快、长序列扩展好，但难训练、难 scale。论文提出 Hawk——基于新型门控线性递归单元 RG-LRU 的 RNN；以及 Griffin——把 RG-LRU 递归与局部（滑动窗口）注意力混合的模型。Hawk 在下游任务上超过 Mamba；Griffin 在仅用 1/6 训练 token 的情况下匹敌 Llama-2 的表现，并能外推到远超训练长度的序列。两者训练时达到 Transformer 的硬件效率，推理时延迟更低、吞吐显著更高。作者把 Griffin 扩展验证到 14B 参数。

## 关键技术细节
- RG-LRU：real-gated linear recurrent unit，带数据相关门控的稳定线性递归，替代 SSM/注意力。
- Hawk：纯 RG-LRU 递归模型，下游性能超过 Mamba（同规模）。
- Griffin：交替堆叠 RG-LRU 递归块与局部注意力块（local/sliding-window attention），兼顾长程记忆与精确局部回忆。
- 效率：Griffin 用约 1/6 的训练 token 匹敌 Llama-2；推理吞吐高、延迟低；可外推超训练长度。
- 规模：验证到 14B 参数；训练硬件效率与 Transformer 相当。
- 是后续 Google RecurrentGemma 的架构基础。

## 原始链接
- url: https://arxiv.org/abs/2402.19427
- pdf_url: https://arxiv.org/pdf/2402.19427

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/griffin-hawk.pdf
