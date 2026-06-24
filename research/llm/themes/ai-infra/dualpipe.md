---
title: DualPipe — Bidirectional Pipeline Parallelism for Computation-Communication Overlap
org: DeepSeek-AI
country: China
date: 2025-02
type: github
categories: [AI infra]
url: https://github.com/deepseek-ai/DualPipe
github_url: https://github.com/deepseek-ai/DualPipe
downloaded: [dualpipe-readme.md]
---

## 一句话定位
DeepSeek-V3 提出并开源的双向流水线并行算法，让前向与反向的计算-通信完全重叠并减小流水线气泡，是 V3/R1 训练的关键调度。

## 摘要（3-6 句）
DualPipe 在 DeepSeek-V3 技术报告中提出，从流水线两端同时注入 micro-batch（双向），使前向块与反向块的计算-通信互相重叠，从而几乎完全隐藏跨节点 all-to-all 通信并减少 bubble。代价是每设备需保留 2× 参数副本与略多激活。仓库还包含 Sea AI Lab 提出的 DualPipeV（V 形 cut-in-half 调度，设备数减半）。它是大规模 MoE 训练把 EP 通信藏进计算的代表方案。

## 关键技术细节
- 双向调度：正/反两个方向对称注入 micro-batch，成对的前向块与反向块共享边界、计算通信互相重叠。
- bubble 对比（同 PP stage 数）：DualPipe ≈ (PP/2−1)(F&B+B−3W)，优于 1F1B 的 (PP−1)(F+B) 与 ZB1P。
- 代价：参数 2×/设备、激活 PP+1；DualPipeV 把设备数降到 PP/2。
- 由 Jiashi Li、Chengqi Deng、Wenfeng Liang 开发；需 PyTorch 2.0+；profile 数据见 deepseek-ai/profile-data。

## 原始链接
- url: https://github.com/deepseek-ai/DualPipe
- github_url: https://github.com/deepseek-ai/DualPipe

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/dualpipe-readme.md
