---
title: Flash-Decoding for long-context inference
org: Dao-AILab / Meta (PyTorch Blog)
country: US
date: 2023-10
type: blog
categories: [AI infra]
url: https://pytorch.org/blog/flash-decoding/
pdf_url:
github_url: https://github.com/Dao-AILab/flash-attention
downloaded: [flash-decoding-pytorch-blog.md]
---

## 一句话定位
为推理解码阶段（query 长度=1、batch 小、context 长）重写注意力：在 FlashAttention 基础上新增「KV 序列长度」并行维，把长上下文解码注意力加速最高 8×（注意力本身最高快 50×）。

## 摘要（3-6 句）
训练用的 FlashAttention v1/v2 只在 batch 和 query 长度维并行；而解码时 query 长度通常为 1，若 batch 小于 GPU 的 SM 数（A100 有 108 个），就只用到极小部分 GPU——batch=1 时 FlashAttention 利用率不足 1%。Flash-Decoding 增加沿 keys/values 序列长度的并行维：先把 KV 切成小块，对每块用 FlashAttention 并行算局部注意力并记录每行每块的 log-sum-exp，最后用 log-sum-exp 做跨块归约合并。它兼具 FlashAttention（几乎不写中间结果到显存）与矩阵乘法（占满 GPU）两者优点。在 CodeLlama-34B 上对 512~64k 序列解码吞吐最高提升 8×，且序列变长时解码速度几乎不变。已并入 FlashAttention 包（≥2.2）与 xFormers（≥0.0.22）。

## 关键技术细节
- 三步算法：(1) 把 keys/values 切成小 chunk（仅为视图，无 GPU 开销）；(2) 对每个 split 用 FlashAttention 并行算注意力，额外写出每行每 split 一个标量 log-sum-exp；(3) 用 log-sum-exp 跨 split 归约得最终输出。注意力/softmax 可迭代计算，故能两级（split 内 + split 间）合并。
- 端到端：CodeLlama-34B（同 Llama 2 架构）batch=1 下，序列 512→64k 解码吞吐最高 8× 加速，长序列下序列变长几乎不影响生成速度。
- 微基准（A100，f16，batch=1，16 个 query head dim=128、2 个 KV head 即 GQA，对应 CodeLlama-34B 跑在 4 卡）：注意力本身最高比 FlashAttention v2 快约 50×；到 32k 长度前注意力耗时近似常数。例如 seqlen=131072 时 PyTorch Eager 2664us / FA v2.0.9 4592us / Flash-Decoding 仅 106.6us。
- 可用性：FlashAttention 包 ≥2.2；xFormers ≥0.0.22 经 xformers.ops.memory_efficient_attention 自动按问题规模分发到 Flash-Decoding / FlashAttention / triton 内核。
- 作者：Tri Dao、Daniel Haziza、Francisco Massa、Grigory Sizov（2023-10-13 发布）。

## 原始链接
- url: https://pytorch.org/blog/flash-decoding/
- github_url: https://github.com/Dao-AILab/flash-attention

## 一手源存档（sources/）
- [flash-decoding-pytorch-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/flash-decoding-pytorch-blog.md)
