---
title: "MiniMax-01: Scaling Foundation Models with Lightning Attention"
org: MiniMax (稀宇科技)
country: China
date: 2025-01
type: paper
categories: [架构, AI infra, 预训练数据]
url: https://arxiv.org/abs/2501.08313
pdf_url: https://arxiv.org/pdf/2501.08313
github_url: https://github.com/MiniMax-AI/MiniMax-01
downloaded: [minimax-01.pdf]
---

## 一句话定位
MiniMax-01 系列（Text-01 / VL-01），用 lightning attention（线性注意力）+ MoE 把上下文推到 100 万–400 万 token，456B 总参 / 45.9B 激活。发布 2025-01-14。

## 摘要
MiniMax-01 系列含 MiniMax-Text-01 与 MiniMax-VL-01，性能对标顶级模型且长上下文能力突出。核心是 lightning attention 及其高效扩展，结合 MoE（32 专家、456B 总参、每 token 激活 45.9B）。开发了优化并行策略与高效的计算-通信重叠技术（针对 MoE 与 lightning attention），可在数百亿参数、百万 token 上下文上高效训练推理。Text-01 训练时上下文可达 100 万 token，推理可外推到 400 万 token。VL-01 经 5120 亿视觉语言 token 继续训练。性能匹敌 GPT-4o / Claude-3.5-Sonnet，上下文窗口长 20–32 倍。

## 关键技术细节
- 注意力：lightning attention（线性注意力）+ 每 8 层插入 1 层 softmax attention 的混合方案。
- 架构：MoE，32 专家，456B 总参 / 45.9B 激活；80 层。
- 上下文：训练 1M，推理外推 4M tokens（业界最长之一）。
- Infra：MoE all-to-all 优化 + lightning attention 的计算-通信重叠；定制并行（专家并行 + 序列并行）。
- 预训练：高质量语料；VL-01 续训 512B 视觉语言 token。
- 对标：GPT-4o / Claude-3.5-Sonnet，上下文长 20–32×。
- 开源：GitHub MiniMax-AI/MiniMax-01。

## 原始链接
- url: https://arxiv.org/abs/2501.08313
- pdf_url: https://arxiv.org/pdf/2501.08313
- github_url: https://github.com/MiniMax-AI/MiniMax-01

## 一手源存档（sources/）
- minimax-01.pdf  （PDF 不入 git，走 HF bucket）
