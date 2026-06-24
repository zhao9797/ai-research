---
title: "DeepSpeed Ulysses: System Optimizations for Enabling Training of Extreme Long Sequence Transformer Models"
org: Microsoft (DeepSpeed)
country: US
date: 2023-09
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2309.14509
pdf_url: https://arxiv.org/pdf/2309.14509
github_url: https://github.com/deepspeedai/DeepSpeed
downloaded: [deepspeed-ulysses-2309.14509.pdf]
---

## 一句话定位
DeepSpeed 的序列并行方案，用 all-to-all 在序列维与 head 维之间转置，使注意力按 head 并行、其余层按序列并行，实现高效超长序列训练。

## 摘要（3-6 句）
Ulysses 针对超长序列训练，把激活沿序列维切到多卡；进入注意力前用 all-to-all 把切分从序列维转到 attention head 维，使每卡算完整序列的一部分 head，算完再 all-to-all 转回。相比 Ring/Megatron-SP，其通信量随序列长度线性而非平方增长，通信效率更高。论文称可训练比现有方法长 4× 的序列、吞吐高 2.5×，支持百万 token 级序列。

## 关键技术细节
- 通信原语：两次 all-to-all（序列维 ↔ head 维转置），通信量 O(N) 而非 O(N^2)。
- 与 ZeRO-3 兼容，可叠加数据/参数分片；支持 dense 与 sparse attention。
- 性能：支持 4× 更长序列、约 2.5× 吞吐；可达百万级 token 上下文训练。
- 与 Ring Attention 是序列并行两条主流路线（all-to-all vs ring）。

## 原始链接
- url: https://arxiv.org/abs/2309.14509
- pdf_url: https://arxiv.org/pdf/2309.14509
- github_url: https://github.com/deepspeedai/DeepSpeed

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/deepspeed-ulysses-2309.14509.pdf
