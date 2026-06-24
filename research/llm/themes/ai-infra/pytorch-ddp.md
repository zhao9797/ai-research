---
title: PyTorch Distributed: Experiences on Accelerating Data Parallel Training
org: Meta (Facebook AI)
country: US
date: 2020-06
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2006.15704
pdf_url: https://arxiv.org/pdf/2006.15704
github_url: https://github.com/pytorch/pytorch
downloaded: [pytorch-ddp-2006.15704.pdf]
---

## 一句话定位
PyTorch DistributedDataParallel（DDP）的设计与工程经验论文，gradient bucketing + 通信计算重叠成为分布式数据并行的工业标准。

## 摘要（3-6 句）
论文介绍 PyTorch v1.5 的 DDP 模块设计：把梯度分桶（bucketing），在反向计算中梯度一就绪即异步 all-reduce，使通信与反向计算重叠；并跳过不参与的梯度同步。它讨论了梯度归约的工程权衡（bucket 大小、参数顺序、no_sync 累积）。在最多 256 张 GPU 上对 ResNet/BERT 近线性扩展。DDP 是后续 FSDP、ZeRO 等数据并行优化的基线与对照。

## 关键技术细节
- gradient bucketing：把多参数梯度打包成 bucket 后 all-reduce，减少小通信开销。
- overlap：反向遍历中梯度就绪即触发异步 all-reduce，与计算重叠。
- 跳过未用参数同步、梯度累积（no_sync）。
- 扩展：最多 256 GPU 近线性；是 PyTorch 分布式训练事实标准，FSDP/DTensor 的前身基础。

## 原始链接
- url: https://arxiv.org/abs/2006.15704
- pdf_url: https://arxiv.org/pdf/2006.15704

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/pytorch-ddp-2006.15704.pdf
