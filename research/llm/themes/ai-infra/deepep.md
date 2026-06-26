---
title: DeepEP — Efficient Expert-Parallel Communication Library
org: DeepSeek-AI
country: China
date: 2025-02
type: github
categories: [AI infra]
url: https://github.com/deepseek-ai/DeepEP
github_url: https://github.com/deepseek-ai/DeepEP
downloaded: [deepep-readme.md]
---

## 一句话定位
DeepSeek 开源的 MoE 专家并行（EP）通信库，提供高吞吐低延迟的 all-to-all dispatch/combine kernel（含 FP8、低 SM 占用），是大规模 MoE 训练/推理的核心通信基础设施。

## 摘要（3-6 句）
DeepEP（DeepEveryParallel）专注专家并行，提供 MoE dispatch/combine 的高性能 all-to-all GPU kernel，支持 FP8 低精度，并以零/极小 SM 占用为目标。V2 完全重构：从 NVSHMEM 后端切到更轻量的 NCCL Gin 后端，统一高吞吐与低延迟 API，支持到 EP2048 的超大规模，且 V3 风格训练的 SM 占用从 24 降到 4-6。它配合 NVLink（节点内）与 RDMA（跨节点），是 DeepSeek-V3 高效 MoE 的关键。

## 关键技术细节
- 性能（V3 配置：8K token/batch、hidden 7168、top-8、FP8 dispatch、BF16 combine）：SM100 NVLink EP8 达 726 GB/s（dispatch）/740 GB/s（combine，64 SM）；RDMA EP8x2 约 90 GB/s。
- V2 vs V1：最高 1.3× 峰值性能、最多省 4× SM 数量；支持 EP2048 大规模 scale-up/scale-out。
- 后端：NCCL Gin（header-only，可复用现有 NCCL communicator）；全 JIT 编译，安装无需 CUDA 编译。
- 0-SM Engram（RDMA）、0-SM PP（RDMA）、0-SM CP（Copy Engine）等实验特性；要求 Hopper SM90+、CUDA 12.3+、NVLink + RDMA。

## 原始链接
- url: https://github.com/deepseek-ai/DeepEP
- github_url: https://github.com/deepseek-ai/DeepEP

## 一手源存档（sources/）
- [deepep-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/deepep-readme.md)
