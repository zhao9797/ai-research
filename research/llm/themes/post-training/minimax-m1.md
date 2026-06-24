---
title: MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention
org: MiniMax (稀宇科技)
country: China
date: 2025-06
type: report
categories: [架构, 后训练, AI infra]
url: https://arxiv.org/abs/2506.13585
pdf_url: https://arxiv.org/pdf/2506.13585
github_url: https://github.com/MiniMax-AI/MiniMax-M1
downloaded: [minimax-m1.pdf]
---

## 一句话定位
MiniMax-M1：首个开源大规模混合注意力（Lightning Attention）+ MoE 推理模型，提出 CISPO RL 算法，用极低算力（约 53 万美元 RL 成本）训练出 100 万上下文的推理模型。

## 摘要（3-6 句）
MiniMax-M1 是世界首个开源的大规模混合注意力推理模型：4560 亿总参数（每 token 激活约 459 亿）的 MoE，结合 Lightning Attention（线性注意力）混合架构，原生支持 100 万 token 上下文，生成 10 万 token 时 FLOPs 仅为 DeepSeek-R1 的约 25%，极利于长 CoT 推理与 test-time scaling。RL 阶段提出 CISPO（Clipped IS-weight Policy Optimization），用裁剪重要性采样权重而非裁剪 token 更新，比 DAPO 收敛快约 2 倍。整个 RL 训练仅用 512 张 H800 约三周、成本约 53.5 万美元。开源 40K / 80K 思考预算两个版本。

## 关键技术细节
- 架构：MoE 4560 亿总参 / 约 459 亿激活；Lightning Attention 与 softmax 注意力混合（每 7 层 lightning + 1 层 softmax）；原生 1M token 上下文。
- 效率：生成 10 万 token 时算力约为 DeepSeek-R1 的 25%，适合长生成 RL。
- RL 算法 CISPO：裁剪重要性采样权重（importance sampling weight）而非裁剪 token 概率比，保留所有 token 梯度、稳定长序列 RL；据报告比 DAPO 快约 2×。
- 训练成本：RL 用 512×H800 约 3 周，约 53.5 万美元（强调低成本可复现）。
- 训练栈：基于自研 + 可验证奖励（数学/代码沙箱）+ 通用奖励模型。
- 发布：MiniMax-M1-40k 与 MiniMax-M1-80k（思考预算），开源权重。

## 原始链接
- url: https://arxiv.org/abs/2506.13585
- pdf_url: https://arxiv.org/pdf/2506.13585
- github_url: https://github.com/MiniMax-AI/MiniMax-M1

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/minimax-m1.pdf
