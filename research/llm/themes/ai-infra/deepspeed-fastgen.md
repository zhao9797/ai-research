---
title: DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference
org: Microsoft (DeepSpeed)
country: US
date: 2024-01
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2401.08671
pdf_url: https://arxiv.org/pdf/2401.08671
github_url: https://github.com/deepspeedai/DeepSpeed-MII
downloaded: [deepspeed-fastgen-2401.08671.pdf]
---

## 一句话定位
DeepSpeed 的高吞吐推理系统，核心调度技术 Dynamic SplitFuse 把 prompt 拆分并与生成 token 融合成均匀 batch，提升吞吐并降低尾延迟。

## 摘要（3-6 句）
DeepSpeed-FastGen 基于 DeepSpeed-MII 与 DeepSpeed-Inference，提出 Dynamic SplitFuse 调度：把长 prompt 动态切片，并把这些切片与正在生成的 decode token 组合成大小一致的连续批，从而稳定每步算力、提升 token/s 并改善延迟一致性。相比 vLLM，论文报告吞吐最高约 2.3× 提升、平均延迟降低、尾延迟显著改善。支持张量并行与多副本扩展。

## 关键技术细节
- Dynamic SplitFuse：prompt 动态分块 + 与 generation token 组合成 uniform-size forward，配平算力。
- 基于 DeepSpeed-Inference kernel（高性能 fused kernel）+ MII serving 层。
- 性能：相对 vLLM 最高约 2.3× 吞吐、更低平均/尾延迟（P95/P99）。
- 支持 tensor parallelism、replica scaling、continuous batching。

## 原始链接
- url: https://arxiv.org/abs/2401.08671
- pdf_url: https://arxiv.org/pdf/2401.08671
- github_url: https://github.com/deepspeedai/DeepSpeed-MII

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/deepspeed-fastgen-2401.08671.pdf
