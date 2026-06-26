---
title: FlashMLA — Efficient Multi-head Latent Attention Kernels
org: DeepSeek-AI
country: China
date: 2025-02
type: github
categories: [AI infra]
url: https://github.com/deepseek-ai/FlashMLA
github_url: https://github.com/deepseek-ai/FlashMLA
downloaded: [flashmla-readme.md]
---

## 一句话定位
DeepSeek 开源周首日放出的 MLA 高性能注意力 kernel，针对 Hopper 优化变长序列解码，支撑 DeepSeek-V3/R1 推理；后续加入 FP8 稀疏注意力。

## 摘要（3-6 句）
FlashMLA 是面向 MLA（Multi-head Latent Attention）的优化 CUDA kernel 库，为 DeepSeek-V3/R1 等模型推理服务。它针对 Hopper（SM90）做了变长序列、分页 KV cache 的高效解码实现，2025-04 更新对 compute-bound 工作负载提升 5-15%。2025-09 随 DeepSeek-V3.2 发布 token 级稀疏注意力 kernel（DSA），并加入 SM100（Blackwell）支持。是 DeepSeek 2025 开源周（open-source week）第 1 天发布的项目。

## 关键技术细节
- dense MLA decoding kernel：H800 SXM5 / CUDA 12.8 上达 3000 GB/s（访存受限）与 660 TFLOPS（算力受限）。
- token 级 sparse MLA decoding（FP8 KV cache、BF16 matmul）：H800 上 410 TFLOPS；B200 约 350 TFLOPS。
- sparse MLA prefill：H800 640 TFLOPS，B200 最高 1450 TFLOPS。
- 支持 SM90/SM100，CUDA 12.8+（SM100 需 12.9+），PyTorch 2.0+；分页 KV cache、变长序列。

## 原始链接
- url: https://github.com/deepseek-ai/FlashMLA
- github_url: https://github.com/deepseek-ai/FlashMLA

## 一手源存档（sources/）
- [flashmla-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/flashmla-readme.md)
