---
title: "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills"
org: Microsoft Research India / Georgia Tech
country: US
date: 2023-08
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2308.16369
pdf_url: https://arxiv.org/pdf/2308.16369
downloaded: [sarathi-2308.16369.pdf]
---

## 一句话定位
提出 chunked-prefill（分块预填充）+ piggyback（把解码搭在预填充块上）调度，平衡每个 batch 的算力，消除流水线气泡与 prefill/decode 干扰，是后续 Sarathi-Serve 的基础。

## 摘要（3-6 句）
LLM 推理中 prefill 是计算密集、decode 是访存密集，二者混批导致 GPU 利用不均与流水线气泡。SARATHI 把长 prefill 切成固定大小 chunk，并在每个 chunk 上“搭载”若干 decode token，使每个迭代的计算量均衡（compute-bound 与 memory-bound 配平）。这显著提升解码吞吐并减少 PP 气泡。其思想（chunked prefill + stall-free batching）后来发展为 Sarathi-Serve，被 vLLM 等广泛采用为默认调度。

## 关键技术细节
- chunked-prefill：把单条长 prompt 的 prefill 拆成固定 token 预算的块，避免单步算力尖峰。
- decode-maximal piggybacking：在 prefill chunk 的算力预算内填入尽量多 decode token，配平每步算力。
- 减少 pipeline bubble、提升 decode 吞吐；在 A6000/A100 上对 LLaMA/GPT 大幅提速。
- 演进为 Sarathi-Serve（stall-free scheduling），成为主流引擎默认 continuous batching 策略之一。

## 原始链接
- url: https://arxiv.org/abs/2308.16369
- pdf_url: https://arxiv.org/pdf/2308.16369

## 一手源存档（sources/）
- [sarathi-2308.16369.pdf](https://arxiv.org/pdf/2308.16369)  （arXiv 原文 PDF，不入 git）
