---
title: "MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention"
org: MiniMax (稀宇科技)
country: China
date: 2025-06
type: paper
categories: [架构, AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2506.13585
pdf_url: https://arxiv.org/pdf/2506.13585
github_url: https://github.com/MiniMax-AI/MiniMax-M1
downloaded: [minimax-m1.pdf]
---

## 一句话定位
全球首个开源大规模混合注意力推理模型，基于 MiniMax-Text-01（456B/45.9B 激活），原生 1M 上下文（DeepSeek-R1 的 8 倍），提出 CISPO RL 算法，512×H800 三周完成 RL。发布 2025-06-16。

## 摘要
MiniMax-M1 是全球首个开源、大规模 hybrid-attention 推理模型，由混合 MoE 架构 + lightning attention 驱动，基于 MiniMax-Text-01（456B 总参 / 45.9B 激活）开发，原生支持 100 万 token 上下文（DeepSeek-R1 的 8 倍）。lightning attention 使 test-time compute 可高效扩展，适合长输入、长思考任务。用大规模 RL 在 sandbox 软件工程等多样问题上训练，提出 CISPO 算法：裁剪重要性采样权重而非 token 更新，优于其他 RL 变体。混合注意力 + CISPO 使全程 RL 训练仅在 512 张 H800 上约三周完成。

## 关键技术细节
- 架构：hybrid MoE + lightning attention，456B 总参 / 45.9B 激活；提供 40K 与 80K 思考预算两个版本。
- 上下文：原生 1M tokens。
- RL 算法：CISPO（Clipped IS-weight Policy Optimization）——裁剪重要性采样权重而非裁剪 token 更新，比 GRPO/DAPO 更高效。
- RL 任务：sandbox-based 真实软件工程环境 + 可验证任务（数学/逻辑/代码）。
- 训练成本：完整 RL 仅 512×H800、约 3 周（约 53.5 万美元）。
- 开源：GitHub MiniMax-AI/MiniMax-M1，Apache 2.0。

## 原始链接
- url: https://arxiv.org/abs/2506.13585
- pdf_url: https://arxiv.org/pdf/2506.13585
- github_url: https://github.com/MiniMax-AI/MiniMax-M1

## 一手源存档（sources/）
- minimax-m1.pdf  （PDF 不入 git，走 HF bucket）
