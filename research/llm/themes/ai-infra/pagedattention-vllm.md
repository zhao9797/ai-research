---
title: Efficient Memory Management for Large Language Model Serving with PagedAttention
org: UC Berkeley / Stanford / UCSD (vLLM)
country: US
date: 2023-09
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2309.06180
pdf_url: https://arxiv.org/pdf/2309.06180
github_url: https://github.com/vllm-project/vllm
downloaded: [pagedattention-vllm-2309.06180.pdf, vllm-readme.md]
---

## 一句话定位
提出 PagedAttention（把 KV cache 像操作系统虚拟内存分页管理），消除 KV 显存碎片、支持 cache 共享，催生 vLLM 这一主流开源推理引擎。

## 摘要（3-6 句）
LLM 服务受 KV cache 显存管理低效拖累：预留连续显存导致内/外碎片、无法共享。PagedAttention 借鉴 OS 分页，把每序列 KV 切成固定大小 block 非连续存储，用 block table 映射，几乎零浪费并支持前缀/beam 间共享。基于此构建的 vLLM 把吞吐相对 HF Transformers / FasterTransformer 提升 2-4×，长序列与大模型收益更大。vLLM 现已成为社区事实标准推理引擎。

## 关键技术细节
- PagedAttention：KV cache 分块（block，如 16 token）非连续存储 + block table 映射；显存浪费 <4%。
- copy-on-write 共享：parallel sampling、beam search、prefix 复用零冗余拷贝。
- 连续批处理（continuous batching）+ 高效调度，吞吐 2-4× over HF/FT，相同延迟下服务更多请求。
- 开源 vLLM 引擎，后续支持 tensor/pipeline 并行、量化、speculative decode、PD 分离等。

## 原始链接
- url: https://arxiv.org/abs/2309.06180
- pdf_url: https://arxiv.org/pdf/2309.06180
- github_url: https://github.com/vllm-project/vllm

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/pagedattention-vllm-2309.06180.pdf
- ../../../../sources/llm/themes/ai-infra/vllm-readme.md
