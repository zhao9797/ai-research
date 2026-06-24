---
title: Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed Deep Learning
org: UC Berkeley / Google / AMPLab
country: US
date: 2022-01
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2201.12023
pdf_url: https://arxiv.org/pdf/2201.12023
downloaded: [alpa-2201.12023.pdf]
---

## 一句话定位
自动化分布式训练编译器，把并行划分为 inter-operator（流水线）与 intra-operator（算子内/张量）两个层级，分别用整数规划与动态规划求最优方案。

## 摘要（3-6 句）
Alpa 把并行策略空间分层：intra-operator parallelism（数据/张量并行，用 ILP 求每个算子的最优 sharding）与 inter-operator parallelism（流水线，用 DP 切分 stage 并分配设备 mesh）。编译器自动生成跨网格的执行计划，无需人工设计 3D 并行。论文在 GPT-3/GShard-MoE/Wide-ResNet 上达到甚至超过人工调优的 Megatron/DeepSpeed 性能，在缺乏手工策略的模型上优势更大。Alpa 成为自动并行的代表作。

## 关键技术细节
- 两级并行空间：intra-op（ILP 最小化通信+计算代价）+ inter-op（DP 切 pipeline stage 与 device mesh 分配）。
- 自动跨 mesh 通信生成（resharding between meshes）。
- 与 Megatron-LM、DeepSpeed 在 GPT 上 matched，在 MoE/异构模型上更优；运行于 GPU 集群。
- 基于 XLA/Jax，开源。

## 原始链接
- url: https://arxiv.org/abs/2201.12023
- pdf_url: https://arxiv.org/pdf/2201.12023

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/alpa-2201.12023.pdf
