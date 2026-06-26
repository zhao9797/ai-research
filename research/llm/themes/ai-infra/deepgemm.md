---
title: DeepGEMM — Clean and Efficient FP8 GEMM Kernels with Fine-grained Scaling
org: DeepSeek-AI
country: China
date: 2025-02
type: github
categories: [AI infra]
url: https://github.com/deepseek-ai/DeepGEMM
github_url: https://github.com/deepseek-ai/DeepGEMM
downloaded: [deepgemm-readme.md]
---

## 一句话定位
DeepSeek 开源的 FP8/FP4/BF16 高性能 tensor core GEMM 库，含细粒度缩放与 fused MoE，代码简洁、全 JIT，是 DeepSeek-V3 FP8 训练/推理的矩阵乘底座。

## 摘要（3-6 句）
DeepGEMM 把现代 LLM 的核心计算原语（FP8/FP4/BF16 GEMM、带通信重叠的 fused MoE「Mega MoE」、lightning indexer 的 MQA scoring、HyperConnection 等）统一进一个简洁 CUDA 代码库。它借鉴 CUTLASS/CuTe 概念但不重度依赖其模板，核函数少、易读，适合学习 GPU kernel 优化。全部 kernel 运行时 JIT 编译，安装无需 CUDA 编译。在 H800 上 FP8 GEMM 最高达 1550 TFLOPS，性能匹配或超过专家调优库。

## 关键技术细节
- 支持 FP8 / FP4 / BF16 GEMM + 细粒度（fine-grained tile/block-wise）缩放，匹配 DeepSeek-V3 FP8 训练精度方案。
- fused MoE（Mega MoE）含通信重叠；MQA scoring（weighted ReLU logits）供 V3.2 的 lightning indexer。
- 性能：H800 FP8 GEMM 最高 1550 TFLOPS；支持 SM90/SM100。
- 全 JIT、低 CPU 开销的 JIT C++ 模块；要求 SM90/SM100、CUDA 12.3+（推荐 12.9+）、PyTorch 2.1+、CUTLASS 4.0+。

## 原始链接
- url: https://github.com/deepseek-ai/DeepGEMM
- github_url: https://github.com/deepseek-ai/DeepGEMM

## 一手源存档（sources/）
- [deepgemm-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/deepgemm-readme.md)
