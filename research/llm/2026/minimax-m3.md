---
title: "MiniMax-M3（原生多模态，1M 上下文，MiniMax Sparse Attention）"
org: MiniMax (稀宇科技)
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://huggingface.co/MiniMaxAI/MiniMax-M3
pdf_url: https://arxiv.org/abs/2606.13392
github_url: https://github.com/MiniMax-AI/MSA
downloaded: [minimax-m3-readme.md, minimax-m3-config.json]
---

## 一句话定位
MiniMax-M3 —— 原生多模态、1M 上下文模型，~428B 总参 / ~23B 激活，用 **MiniMax Sparse Attention (MSA)** 把长上下文效率推到新高（晚于初版调研，增量补录；M2 与 MSA 论文已在库）。

## 摘要
M3 是 M2 之后的迭代，核心是 MSA 稀疏注意力（技术报告 arXiv 2606.13392，已收录为 minimax-sparse-attention）：相比 M2，在 1M 上下文下 **prefill 提速 9×、decode 提速 15×，per-token 算力降到 1/20**；相比 GQA 大幅降注意力算力与显存而保质量。前沿级 long-horizon agentic（coding & cowork）。三种推理模式：enabled / adaptive（自动判断是否深思）/ disabled。

## 关键技术细节
- **架构（config.json，model_type=minimax_m3_vl）**：hidden 6144；**60 层**；64 注意力头 / 4 KV（GQA），head_dim 128；vocab 200064；上下文 **1M**（max_position 1,048,576）；rope_theta 5e6；MoE 每 token 选 4 + 1 共享专家（dense_intermediate 12288，shared_intermediate 3072）。
- **MSA**：面向百万 token 的高性能稀疏注意力算子（GitHub MiniMax-AI/MSA）。
- **推理模式**：thinking = enabled/adaptive/disabled。
- 许可 minimax-community。较 M2 主打长上下文效率 + agentic coding/cowork。

## 原始链接
- url: https://huggingface.co/MiniMaxAI/MiniMax-M3 ; MSA 报告: https://arxiv.org/abs/2606.13392

## 本地落盘文件
- ../../../sources/llm/2026/minimax-m3-readme.md
- ../../../sources/llm/2026/minimax-m3-config.json
