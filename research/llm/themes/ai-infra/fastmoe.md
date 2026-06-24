---
title: "FastMoE: A Fast Mixture-of-Expert Training System"
org: Tsinghua University / others
country: China
date: 2021-03
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2103.13262
pdf_url: https://arxiv.org/pdf/2103.13262
github_url: https://github.com/laekov/fastmoe
downloaded: [fastmoe-2103.13262.pdf]
---

## 一句话定位
首个开源的 PyTorch MoE 训练系统，提供分布式专家并行与高性能 kernel，使开源社区能训练 GShard/Switch 式万亿级 MoE。

## 摘要（3-6 句）
当时 MoE 训练系统（GShard/Switch）依赖 Google 专有 TPU 栈。FastMoE 基于 PyTorch 实现，支持把专家分布到多 GPU/多节点（expert parallelism）并提供优化的门控与 all-to-all 通信 kernel，灵活适配各种模型。它让研究者在通用 GPU 集群上训练大规模 MoE，并支持把数据并行与专家并行组合。FastMoE 是中文社区（如 GLM/悟道）早期 MoE 工作的基础设施。

## 关键技术细节
- PyTorch 原生 MoE 层 + 自定义 CUDA kernel；支持单机多卡与多机专家并行。
- expert parallelism + data parallelism 组合，all-to-all dispatch/combine。
- 灵活 gate 接口（可插自定义路由）；可训练 SOTA 规模 MoE（论文示范 GPT-MoE）。
- 开源，奠定中文社区 MoE 训练栈基础。

## 原始链接
- url: https://arxiv.org/abs/2103.13262
- pdf_url: https://arxiv.org/pdf/2103.13262
- github_url: https://github.com/laekov/fastmoe

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/fastmoe-2103.13262.pdf
