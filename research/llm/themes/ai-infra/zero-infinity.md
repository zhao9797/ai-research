---
title: "ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning"
org: Microsoft (DeepSpeed)
country: US
date: 2021-04
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2104.07857
pdf_url: https://arxiv.org/pdf/2104.07857
github_url: https://github.com/deepspeedai/DeepSpeed
downloaded: [zero-infinity-2104.07857.pdf]
---

## 一句话定位
ZeRO 的卸载（offload）扩展，把参数/梯度/优化器状态卸到 CPU 内存与 NVMe SSD，使单节点也能训练数十万亿参数模型。

## 摘要（3-6 句）
ZeRO-Infinity 在 ZeRO-3 基础上引入异构内存层级（GPU、CPU、NVMe）卸载，并提出 infinity offload engine、memory-centric tiling、带宽中心的通信调度与 overlap。论文称单 DGX-2 节点可微调万亿参数模型，512 张 V100 上可训练 32 万亿参数模型，并在 512 GPU 上对 20 万亿参数模型达到 49 TFLOPs/GPU。它消除了人工重写模型代码的需求，对用户近乎透明。

## 关键技术细节
- 三级内存卸载：GPU HBM ← CPU DRAM ← NVMe SSD，按需 prefetch / 异步写回。
- memory-centric tiling：把大算子切成可放入 GPU 的小块，避免单层超显存。
- bandwidth-centric partitioning + overlap-centric design：把通信与 NVMe/CPU↔GPU 传输与计算重叠。
- 规模断言：32T 参数可训于 512×V100；20T 模型 49 TFLOPs/GPU；单节点可 fine-tune 1T 模型。

## 原始链接
- url: https://arxiv.org/abs/2104.07857
- pdf_url: https://arxiv.org/pdf/2104.07857
- github_url: https://github.com/deepspeedai/DeepSpeed

## 一手源存档（sources/）
- [zero-infinity-2104.07857.pdf](https://arxiv.org/pdf/2104.07857)  （arXiv 原文 PDF，不入 git）
