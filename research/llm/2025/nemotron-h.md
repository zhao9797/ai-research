---
title: Nemotron-H - Hybrid Mamba-Transformer Models
org: NVIDIA
country: US
date: 2025-04
type: technical-report
categories: [架构, AI infra]
url: https://arxiv.org/abs/2504.03624
pdf_url: https://arxiv.org/pdf/2504.03624
github_url:
downloaded: [files/nemotron-h.pdf]
---

## 一句话定位
NVIDIA 2025-04 的 Nemotron-H 技术报告：8B 与 56B/47B 的混合 Mamba-Transformer 模型，用 Mamba 层替换大多数自注意力层以恒定算力/显存生成 token，推理最高快 3x。

## 摘要
为降低 inference-time scaling 下的推理成本，Nemotron-H 把常规 Transformer 中大多数 self-attention 层替换为 Mamba 层（每生成 token 恒定计算与显存）。8B/56B 在同尺寸下精度与 Qwen-2.5、Llama-3.1 持平或更好，推理最高快 3x。还用 MiniPuzzle 剪枝蒸馏把 56B 压成 47B（精度相近、再快 20%），并给出 FP8 训练配方（与 BF16 持平，用于训练 56B）。

## 关键技术细节（带数字）
- 规模：8B 与 56B；以及由 56B 压缩得到的 47B。
- 架构：hybrid Mamba-Transformer——大多数 self-attention 层替换为 Mamba 层（恒定计算/显存 per token）。
- 速度：相对同尺寸 Transformer（Qwen-2.5-7B/72B、Llama-3.1-8B/70B）精度持平或更好，推理最高 3x 快。
- 压缩：MiniPuzzle（剪枝 + 蒸馏）将 56B → 47B，精度相近且再快 20%。
- 精度：FP8 训练配方（与 BF16 持平），用于训练 56B。
- 开源：base 检查点（Hugging Face + NeMo 支持）。
- 发布日期：2025-04（arXiv:2504.03624）。

## 原始链接
- arXiv：https://arxiv.org/abs/2504.03624
- PDF：https://arxiv.org/pdf/2504.03624

## 本地落盘文件
- ../../../sources/llm/2025/nemotron-h.pdf
