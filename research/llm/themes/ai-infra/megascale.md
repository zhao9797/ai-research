---
title: "MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs"
org: ByteDance / Peking University
country: China
date: 2024-02
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2402.15627
pdf_url: https://arxiv.org/pdf/2402.15627
downloaded: [megascale-2402.15627.pdf]
---

## 一句话定位
字节跳动生产级万卡 LLM 训练系统，全栈协同设计（算法+系统+网络+可观测性），在 12288 张 GPU 上训练 175B 模型达到 55.2% MFU。

## 摘要（3-6 句）
MegaScale 面向 >10000 GPU 规模的生产训练，强调效率与稳定性（长时训练的容错与 straggler 抑制）。它在 model block/optimizer 设计、计算通信重叠、算子优化、数据流水线、网络调优上做全栈协同。训练 175B 模型于 12288 GPU 时 MFU 达 55.2%，比 Megatron-LM 提升 1.34×。论文重点分享了大规模才暴露的稳定性问题及深度可观测/诊断工具（定位 root cause、容错、抑制慢节点）。

## 关键技术细节
- 规模：>10000 GPU；175B 模型在 12288 GPU 上 55.2% MFU（1.34× over Megatron-LM）。
- 算法-系统协同：parallel transformer block、sliding window attention、LAMB、混合精度通信重叠。
- 通信重叠：把 TP/PP/DP 的集合通信与计算重叠；定制算子（如 fused kernel）。
- 数据流水线与网络调优；强可观测性栈用于诊断 stability 问题、容错、straggler mitigation。
- 生产经验：长训练 job 的故障恢复与稳定性是核心贡献。

## 原始链接
- url: https://arxiv.org/abs/2402.15627
- pdf_url: https://arxiv.org/pdf/2402.15627

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/megascale-2402.15627.pdf
