---
title: "GSPMD: General and Scalable Parallelization for ML Computation Graphs"
org: Google
country: US
date: 2021-05
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2105.04663
pdf_url: https://arxiv.org/pdf/2105.04663
downloaded: [gspmd-2105.04663.pdf]
---

## 一句话定位
基于 XLA 的自动并行编译器，用户只需给少量张量标注 sharding，GSPMD 自动推断整图分片并生成 SPMD 程序，是 GShard 思想的通用化。

## 摘要（3-6 句）
GSPMD 把并行抽象为对张量维度的 sharding 标注，编译器据此自动补全整张计算图的分片方案并插入通信。它统一表达数据并行、算子内并行、流水线并行与它们的嵌套组合，且生成单一 SPMD 程序（无论多少设备代码量恒定）。论文在多种模型上验证，可对 50B–1T 参数模型在 2048 TPU v3 上达到 50%+ 的 FLOPs 利用率。GSPMD 是 GShard 编译能力的开源/通用化版本，被 JAX 的 pjit/Flax 等沿用。

## 关键技术细节
- 抽象：mesh + per-tensor sharding annotation（replicated / tiled / partially-tiled）；编译器做 sharding propagation。
- 支持嵌套并行：data + within-op + pipeline 任意组合，单 SPMD 程序。
- 通信由编译器自动插入（all-reduce / all-gather / collective-permute 等）。
- 规模验证：dense Transformer 与 MoE，50B 到 1T 参数，2048×TPU v3，54%–62% FLOPs 利用。

## 原始链接
- url: https://arxiv.org/abs/2105.04663
- pdf_url: https://arxiv.org/pdf/2105.04663

## 一手源存档（sources/）
- [gspmd-2105.04663.pdf](https://arxiv.org/pdf/2105.04663)  （arXiv 原文 PDF，不入 git）
