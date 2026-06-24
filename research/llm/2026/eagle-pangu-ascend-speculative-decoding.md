---
title: "EAGLE-Pangu: Accelerator-Safe Tree Speculative Decoding on Ascend NPUs"
org: 华为盘古 Huawei Pangu (昇腾 Ascend)
country: China
date: 2026-03
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2603.08088
pdf_url: https://arxiv.org/pdf/2603.08088
github_url: ""
downloaded: [eagle-pangu.pdf]
---

## 一句话定位
华为把 EAGLE-3 风格的树状投机解码移植到昇腾 NPU + Pangu teacher backend，解决异构后端下注意力掩码/KV-cache 布局/索引语义不互通导致的脆弱性。

## 摘要
EAGLE-Pangu（arXiv 2026-03-09，作者 Chang Han、Yijie Hu、Jingling Liu）是一个可复现系统，把 EAGLE-3 风格的树状投机解码（tree speculative decoding）移植到 Ascend NPU 上的 Pangu teacher backend。自回归解码仍是 LLM serving 的主要瓶颈，投机解码通过每步验证多个候选 token 来减少昂贵的 teacher 模型调用，树状投机进一步提升并行度，但跨异构后端/加速器栈移植时往往脆弱——注意力掩码、KV-cache 布局、索引语义并不互通。EAGLE-Pangu 聚焦"accelerator-safe"（加速器安全）的移植，针对昇腾栈解决这些不兼容问题。

## 关键技术细节
- **定位**：把 EAGLE-3 风格 tree speculative decoding 移植到 Ascend NPU 的 Pangu teacher backend。
- **问题**：树状投机解码跨异构后端脆弱——attention masking / KV-cache layout / indexing semantics 不互通。
- **目标-accelerator-safe**：在昇腾加速器栈上可复现、稳健的树状投机解码。
- **收益**：减少 teacher 模型调用、提升 LLM serving 解码并行度。
- **生态**：Huawei Ascend NPU 推理加速基础设施（与 openPangu 系列配套）。

## 原始链接
- url: https://arxiv.org/abs/2603.08088
- pdf_url: https://arxiv.org/pdf/2603.08088

## 本地落盘文件
- ../../../sources/llm/2026/eagle-pangu.pdf
