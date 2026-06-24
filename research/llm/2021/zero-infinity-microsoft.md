---
title: "ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning"
org: Microsoft
country: US
date: 2021-04
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2104.07857
pdf_url: https://arxiv.org/pdf/2104.07857
github_url: https://github.com/microsoft/DeepSpeed
downloaded: [arxiv-2104.07857.pdf]
---

## 一句话定位
微软 DeepSpeed 团队的 ZeRO-Infinity：把模型状态卸载到 CPU 内存与 NVMe，突破 GPU 显存墙，让单个 DGX-2 节点也能训练数十万亿参数模型。

## 摘要（3-6 句）
近三年最大稠密模型增长超 1000 倍达千亿级，而 GPU 显存只增长 5 倍（16GB→80GB），逼近"GPU 显存墙"。ZeRO-Infinity 提出异构系统技术：同时利用 GPU、CPU 内存和 NVMe，配合新的内存访问与数据流优化，可在有限 GPU 上训练极大模型。它在 32 个 DGX-2 节点（512 V100）上训练 32 万亿参数模型，单节点也能跑万亿级模型，且对用户几乎无需重构代码。

## 关键技术细节
- 异构内存：GPU 显存 + CPU DRAM + NVMe SSD 三级卸载（offload）模型参数/梯度/优化器状态。
- infinity offload engine + memory-centric tiling + bandwidth-centric partitioning 等技术。
- 规模：512 张 V100（32 个 DGX-2）上可训 32T 参数；单 DGX-2 节点可训 ~1T 参数。
- 易用性：基于 ZeRO 的自动化卸载，几乎不需改模型代码（DeepSpeed 集成）。
- 对照：此前需 800 张 V100 才能"装下"1T 参数模型。
- 是 MT-NLG 530B 等大模型训练的关键 infra 基础；代码 microsoft/DeepSpeed。

## 原始链接
- url: https://arxiv.org/abs/2104.07857
- pdf_url: https://arxiv.org/pdf/2104.07857
- github_url: https://github.com/microsoft/DeepSpeed

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2104.07857.pdf
