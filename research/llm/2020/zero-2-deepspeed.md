---
title: ZeRO-2 & DeepSpeed — Shattering barriers of deep learning speed & scale
org: Microsoft
country: US
date: 2020-05
type: blog
categories: [AI infra]
url: https://www.microsoft.com/en-us/research/blog/zero-2-deepspeed-shattering-barriers-of-deep-learning-speed-scale/
pdf_url:
github_url: https://github.com/microsoft/DeepSpeed
downloaded: [ms-zero2-deepspeed.html]
---

## 一句话定位
DeepSpeed 升级 ZeRO-2（叠加梯度分片 + 激活分片 + 连续内存优化等），把可训练规模提升到 2000 亿参数、训练吞吐再翻倍，是 2020 年大模型 infra 的关键迭代。

## 摘要（3-6 句）
微软 2020-05 发布 ZeRO-2，在 ZeRO stage-1（优化器状态分片）基础上加入梯度分片，并引入激活值分片/卸载、连续内存优化、更快的算子等系统优化。ZeRO-2 可训练高达 2000 亿参数的模型（约为当时最大模型的 10 倍），并在相同硬件上相比 SOTA 实现最高约 10 倍训练速度提升。该版本进一步降低了对模型并行的依赖，使更大的 batch 与更高的算子效率成为可能。

## 关键技术细节
- ZeRO-2 = 优化器状态分片 + 梯度分片（ZeRO stage-2），相对标准数据并行显存降约 8 倍。
- 可训练规模：最高 200B 参数（约为发布时最大模型的 10 倍）。
- 速度：相比当时最佳系统最高约 10 倍训练吞吐提升（结合 Megatron 模型并行）。
- 系统优化：激活值分片/CPU 卸载（activation partitioning/offload）、常驻连续内存以减少碎片、更高效的通信与算子重叠。
- 对 100B 参数级模型可在数百块 V100 上以高吞吐训练。
- 与 ZeRO-1/Megatron-LM 张量并行可灵活组合。

## 原始链接
- url: https://www.microsoft.com/en-us/research/blog/zero-2-deepspeed-shattering-barriers-of-deep-learning-speed-scale/
- github_url: https://github.com/microsoft/DeepSpeed

## 本地落盘文件
- ../../../sources/llm/2020/ms-zero2-deepspeed.html
