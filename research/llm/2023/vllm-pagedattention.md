---
title: Efficient Memory Management for LLM Serving with PagedAttention (vLLM)
org: UC Berkeley
country: US
date: 2023-09
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2309.06180
pdf_url: https://arxiv.org/pdf/2309.06180
github_url: https://github.com/vllm-project/vllm
downloaded: [vllm-pagedattention.pdf]
---

## 一句话定位
PagedAttention 把 OS 分页搬到 KV cache，vLLM 吞吐较 SOTA 提 2-4x，成为业界事实标准推理引擎。

## 摘要
高吞吐 LLM 服务需大批量，但每请求 KV cache 巨大且动态增减，管理不善会因碎片与冗余浪费显存、限制批量。PagedAttention 借鉴 OS 虚拟内存与分页，将 KV cache 分块管理。基于它构建 vLLM：(1)KV cache 近零浪费，(2)请求内/间灵活共享 KV。较 FasterTransformer、Orca 等 SOTA 提升 2-4x 吞吐，序列越长/模型越大/解码越复杂提升越显著。

## 关键技术细节
- 核心：PagedAttention——KV cache 分成固定大小 block，非连续存储，用 block table 映射（类比 OS 页表）。
- 收益：消除内部/外部碎片，显存利用近 100%。
- 共享：beam search、parallel sampling、prefix 共享时 KV block 可 copy-on-write 共享，省显存。
- 性能：相同延迟下吞吐较 FasterTransformer/Orca 提升 2-4x。
- 工程：连续批处理(continuous batching)、PagedAttention CUDA kernel。
- 影响：vLLM 成为最广泛使用的开源推理服务框架。

## 原始链接
- url: https://arxiv.org/abs/2309.06180
- pdf_url: https://arxiv.org/pdf/2309.06180
- github_url: https://github.com/vllm-project/vllm

## 本地落盘文件
- ../../../sources/llm/2023/vllm-pagedattention.pdf
