---
title: "Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving"
org: Moonshot AI / Tsinghua University
country: China
date: 2024-06
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2407.00079
pdf_url: https://arxiv.org/pdf/2407.00079
github_url: https://github.com/kvcache-ai/Mooncake
downloaded: [mooncake-2407.00079.pdf]
---

## 一句话定位
Moonshot AI 旗下 Kimi 的生产服务平台，以 KVCache 为中心做 prefill/decode 分离，并利用集群空闲 CPU/DRAM/SSD 构建分布式 KV 缓存池，配 SLO 感知调度与过载早拒策略。

## 摘要（3-6 句）
Mooncake 是 Kimi 的 serving 平台，采用 KVCache 中心的分离架构（prefill 与 decode 集群分开），并把 GPU 集群里闲置的 CPU、DRAM、SSD 组织成分布式 KVCache 池以增大缓存容量。核心是 KVCache-centric scheduler，在满足延迟 SLO 的前提下最大化有效吞吐；针对高过载场景提出基于预测的早期拒绝策略。模拟场景下吞吐最高提升 525%，真实负载下使 Kimi 多处理 75% 请求。配套开源 Mooncake Store / Transfer Engine。

## 关键技术细节
- KVCache-centric 分离：prefill cluster 与 decode cluster 分开，KV cache 作为一等公民跨节点传输与复用。
- 分布式缓存池：聚合 GPU 集群闲置 CPU/DRAM/SSD 作为 KV 二级缓存（容量 >> HBM）。
- 调度器：最大化 effective throughput 同时满足 TTFT/TPOT SLO；prediction-based early rejection 应对过载。
- 效果：模拟最高 +525% 吞吐；真实负载 Kimi +75% 请求处理量。开源 Transfer Engine 已被 vLLM/SGLang 集成。

## 原始链接
- url: https://arxiv.org/abs/2407.00079
- pdf_url: https://arxiv.org/pdf/2407.00079
- github_url: https://github.com/kvcache-ai/Mooncake

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/mooncake-2407.00079.pdf
