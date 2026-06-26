---
title: "SGLang: Efficient Execution of Structured Language Model Programs"
org: Stanford / UC Berkeley / others (SGLang)
country: US
date: 2023-12
type: paper
categories: [AI infra, agentic训练]
url: https://arxiv.org/abs/2312.07104
pdf_url: https://arxiv.org/pdf/2312.07104
github_url: https://github.com/sgl-project/sglang
downloaded: [sglang-radixattention-2312.07104.pdf, sglang-readme.md]
---

## 一句话定位
面向“结构化 LLM 程序”（多轮、并行、工具调用、约束解码）的前端 DSL + 后端运行时，核心是 RadixAttention 自动复用 KV cache 前缀，是与 vLLM 并列的主流推理框架。

## 摘要（3-6 句）
复杂 LLM 应用（agent、思维链、并行调用、JSON 约束）常有大量共享前缀但被重复计算。SGLang 提供共置的前端语言（表达分支/并行/约束）与后端运行时；后端的 RadixAttention 用基数树（radix tree）在请求间自动复用 KV cache 前缀。配合压缩有限状态机的快速约束解码与 API 推测执行，吞吐相对当时 SOTA（vLLM、Guidance 等）提升最高 6.4×。SGLang 后被 DeepSeek、xAI 等用于大规模 serving。

## 关键技术细节
- RadixAttention：以 radix tree 索引 KV cache，跨请求自动前缀共享与 LRU 淘汰，无需手工 prefix。
- 前端 DSL：表达 gen/select/fork/join、约束解码（JSON/regex）、并行调用。
- 压缩 FSM 加速约束解码；API speculative execution。
- 吞吐最高 6.4×（vs vLLM/LMQL/Guidance）；现支持 TP/DP、MoE、PD 分离、大规模 EP serving。

## 原始链接
- url: https://arxiv.org/abs/2312.07104
- pdf_url: https://arxiv.org/pdf/2312.07104
- github_url: https://github.com/sgl-project/sglang

## 一手源存档（sources/）
- [sglang-radixattention-2312.07104.pdf](https://arxiv.org/pdf/2312.07104)  （arXiv 原文 PDF，不入 git）
- [sglang-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/sglang-readme.md)
