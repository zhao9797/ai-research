---
title: "YaRN: Efficient Context Window Extension of Large Language Models"
org: Nous Research / EleutherAI
country: US
date: 2023-09
type: paper
categories: [架构]
url: https://arxiv.org/abs/2309.00071
pdf_url: https://arxiv.org/pdf/2309.00071
github_url: https://github.com/jquesnelle/yarn
downloaded: [yarn.pdf]
---

## 一句话定位
YaRN 高效扩展 RoPE 上下文窗口，比前法省 10x token、2.5x 步数，成为开源长上下文标配方法。

## 摘要
RoPE 有效编码位置但模型无法泛化超出训练长度。YaRN(Yet another RoPE extensioN) 计算高效地扩展上下文窗口，比已有方法少 10x token、少 2.5x 训练步。用 YaRN，LLaMA 可有效利用并外推到远超原训练长度的上下文，刷新上下文扩展 SOTA，且能外推超出微调数据集长度。

## 关键技术细节
- 方法：NTK-aware + “temperature/attention scaling” 改进的 RoPE 频率插值（对不同维度频率分段处理：高频保留、低频插值）。
- 效率：仅需前法 1/10 的 token、1/2.5 的训练步即可扩窗。
- 结果：将 LLaMA 2 从 4k 扩到 64k/128k；困惑度优于 Position Interpolation/NTK。
- 外推：可超出微调时见过的长度继续泛化。
- 落地：被 Mistral、Qwen、Code Llama 等大量长上下文模型采用。

## 原始链接
- url: https://arxiv.org/abs/2309.00071
- pdf_url: https://arxiv.org/pdf/2309.00071
- github_url: https://github.com/jquesnelle/yarn

## 一手源存档（sources/）
- yarn.pdf  （PDF 不入 git，走 HF bucket）
