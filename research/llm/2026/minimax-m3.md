---
title: "MiniMax-M3（原生多模态，1M 上下文，MiniMax Sparse Attention）"
org: MiniMax (稀宇科技)
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练, 预训练数据]
url: https://huggingface.co/MiniMaxAI/MiniMax-M3
pdf_url: https://arxiv.org/abs/2606.13392
github_url: https://github.com/MiniMax-AI/MiniMax-M3
downloaded: [minimax-m3-readme.md, minimax-m3-config.json]
---

## 一句话定位
原生多模态、1M 上下文模型，~428B 总参 / ~23B 激活，用 **MiniMax Sparse Attention (MSA)** 把长上下文效率推到新高（M2 之后迭代；MSA 论文 2606.13392 已在库）。

## 架构（config.json，model_type=minimax_m3_vl）
- hidden 6144；**60 层**；64 注意力头 / 4 KV（GQA），head_dim 128；vocab 200064；上下文 **1M**（1,048,576）；rope_theta 5e6。
- **MoE**：每 token 选 4 专家 + 1 共享（dense_intermediate 12288，shared_intermediate 3072）。

## 预训练数据 / 训练
- **原生多模态**：从第一步起就做 mixed-modality 训练（text/image/video 深度语义融合），而非后接视觉。
- 具体 token 量/算力 card 未披露；方法细节见 MSA 技术报告 arXiv 2606.13392（已落盘 minimax-sparse-attention）。

## 架构创新 / AI infra：MSA
- **MiniMax Sparse Attention (MSA)**：面向百万 token 的高性能稀疏注意力算子（GitHub MiniMax-AI/MSA）。
- vs M2 @1M 上下文：**prefill 提速 9×、decode 提速 15×，per-token 算力降到 1/20**；相比 GQA 大幅降注意力算力与显存而保质量。

## RL / 推理模式
- 三种 thinking 模式：`enabled` / `adaptive`（自动判断是否深思）/ `disabled`（最低延迟）。

## agentic
- 前沿级 long-horizon agentic（coding & cowork 双强）；配套 MiniMax Agent（agent.minimax.io）。

## Benchmark
- 官方仅以图表披露（figures/benchmark.jpeg），无文本表；定位 frontier-level long-horizon agentic。

## AI infra / 部署
- SGLang / vLLM / Transformers（`minimax_m3_vl`）/ KTransformers / unsloth；推理参数 temp 1.0 / top_p 0.95 / top_k 40；许可 minimax-community。

## 原始链接
- url: https://huggingface.co/MiniMaxAI/MiniMax-M3 · MSA 报告: https://arxiv.org/abs/2606.13392 · github: https://github.com/MiniMax-AI/MSA

## 本地落盘文件
- ../../../sources/llm/2026/minimax-m3-readme.md
- ../../../sources/llm/2026/minimax-m3-config.json
