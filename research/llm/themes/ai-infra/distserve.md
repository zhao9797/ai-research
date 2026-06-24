---
title: DistServe: Disaggregating Prefill and Decoding for Goodput-optimized LLM Serving
org: Peking University / UCSD
country: China
date: 2024-01
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2401.09670
pdf_url: https://arxiv.org/pdf/2401.09670
downloaded: [distserve-2401.09670.pdf]
---

## 一句话定位
提出把 prefill 与 decode 阶段拆到不同 GPU 池（PD 分离），分别针对 TTFT 与 TPOT 优化并独立配比资源，提升满足 SLO 的 goodput。

## 摘要（3-6 句）
LLM 推理的 prefill（计算密集、决定 TTFT）与 decode（访存密集、决定 TPOT）相互干扰，同卡共置导致互相拖慢。DistServe 把两阶段解耦到不同 GPU，按各自 SLO 与负载独立选并行策略与资源比例，并据集群带宽放置以降低 KV 传输开销。结果在满足严格延迟 SLO 下，相比共置系统可服务 7.4× 更多请求或承受 12.6× 更紧的 SLO。PD 分离自此成为高端推理系统标配（vLLM/SGLang/Mooncake 均采纳）。

## 关键技术细节
- prefill / decode 物理分离到不同 GPU 池，各自独立的 batch/并行策略。
- 按 SLO 拆分优化目标：TTFT（首 token 延迟）vs TPOT（每 token 延迟）。
- 带宽感知放置，减少 KV cache 跨节点传输代价。
- goodput 提升：满足 SLO 下 7.4× 请求量 / 容忍 12.6× 更紧 SLO。

## 原始链接
- url: https://arxiv.org/abs/2401.09670
- pdf_url: https://arxiv.org/pdf/2401.09670

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/distserve-2401.09670.pdf
