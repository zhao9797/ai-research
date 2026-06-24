---
title: Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM
org: NVIDIA / Stanford / Microsoft
country: US
date: 2021-04
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2104.04473
pdf_url: https://arxiv.org/pdf/2104.04473
github_url: https://github.com/NVIDIA/Megatron-LM
downloaded: [megatron-gpu-clusters-2104.04473.pdf]
---

## 一句话定位
提出 3D 并行（张量 + 流水线 + 数据并行）的组合与交错式（interleaved）流水线调度，把 Megatron 从单纯 TP 升级为可在数千卡上训练万亿级模型的系统。

## 摘要（3-6 句）
论文系统研究了如何把张量并行、流水线并行、数据并行组合（PTD-P），并给出在 GPU 集群上的最优划分原则。提出 interleaved 1F1B 流水线调度以减小 pipeline bubble。实验在 3072 张 A100 上训练万亿参数模型，达到每卡 502 TeraFLOPs（理论峰值 52% 的 aggregate throughput），整体 502 PetaFLOPs。论文给出了 TP 应限制在单节点内（NVLink）、PP 跨节点、DP 在最外层的工程经验法则。

## 关键技术细节
- 三维并行 PTD-P：tensor(TP) × pipeline(PP) × data(DP)；TP 控制在 8（单 DGX 节点内 NVLink），PP 跨节点。
- Interleaved 1F1B 调度：每设备承载多个非连续 model chunk，将 bubble 比例从 (p-1)/m 降到 (p-1)/(v·m)（v 为每卡 chunk 数）。
- 规模：1T 参数模型，3072×A100（80GB）；端到端 502 PFLOPs，每卡约 163 TFLOPs（52% MFU 量级）。
- 给出 scatter/gather 通信优化、激活重计算与并行度的联合调优指南。

## 原始链接
- url: https://arxiv.org/abs/2104.04473
- pdf_url: https://arxiv.org/pdf/2104.04473
- github_url: https://github.com/NVIDIA/Megatron-LM

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/megatron-gpu-clusters-2104.04473.pdf
