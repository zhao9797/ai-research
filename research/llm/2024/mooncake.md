---
title: "Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving"
org: 月之暗面 Moonshot AI / 清华大学
country: 中国
date: 2024-06
type: arxiv
categories: [AI infra]
url: https://arxiv.org/abs/2407.00079
pdf_url: https://arxiv.org/pdf/2407.00079
github_url: https://github.com/kvcache-ai/Mooncake
downloaded: [files/mooncake.pdf]
---

## 一句话定位
Kimi（月之暗面）背后的推理服务平台，以 KVCache 为中心的 prefill/decode 分离（disaggregated）架构，过载时用早拒绝（early rejection）调度，端到端吞吐显著提升。

## 摘要
Mooncake 是 Moonshot AI 旗下 Kimi 的服务平台，采用以 KVCache 为中心的分离式架构：把 prefill 集群与 decoding 集群分开，并利用 GPU 集群中被闲置的 CPU/DRAM/SSD 资源实现分离式 KVCache 缓存池。核心是 KVCache-centric 调度器，在满足时延 SLO 的同时最大化整体有效吞吐。针对长上下文与过载场景，提出基于预测的 early rejection 策略。真实负载下相比基线吞吐大幅提升、可处理更多请求。

## 关键技术细节（带数字）
- 架构：prefill 与 decoding 集群解耦（disaggregated），KVCache 为中心。
- 缓存池：复用 GPU 集群闲置 CPU/DRAM/SSD，构建分布式 KVCache 池（远端缓存命中复用）。
- 调度：KVCache-centric scheduler，在 TTFT/TBT 等 SLO 约束下最大化有效吞吐。
- 过载处理：基于预测的 early rejection（提前拒绝注定违约的请求）。
- 效果：在长上下文真实工作负载下相比基线显著提升吞吐、提升请求处理量（论文报告在某些模拟场景多处理 75% 请求）。
- 生产价值：Kimi 线上系统的真实经验，已开源 transfer engine。

## 原始链接
- arXiv: https://arxiv.org/abs/2407.00079
- PDF: https://arxiv.org/pdf/2407.00079
- GitHub: https://github.com/kvcache-ai/Mooncake

## 本地落盘文件
- ../../../sources/llm/2024/mooncake.pdf
