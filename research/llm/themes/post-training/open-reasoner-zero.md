---
title: Open-Reasoner-Zero: An Open Source Approach to Scaling Up Reinforcement Learning on the Base Model
org: StepFun / Tsinghua
country: China
date: 2025-03
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2503.24290
pdf_url: https://arxiv.org/pdf/2503.24290
github_url: https://github.com/Open-Reasoner-Zero/Open-Reasoner-Zero
downloaded: [open-reasoner-zero.pdf]
---

## 一句话定位
Open-Reasoner-Zero：首个完全开源的"base 模型上大规模 reasoning RL"实现，证明极简的 vanilla PPO + 规则奖励、无 KL 正则即可复现 R1-Zero 的 scaling，且只需 1/10 训练步。

## 摘要（3-6 句）
ORZ 是第一个开源的、面向 base 模型的大规模 reasoning RL 实现，主打可扩展、简单、可及。实验表明：极简方法——vanilla PPO + GAE（λ=1, γ=1）+ 直接的规则化奖励、不加任何 KL 正则——就足以同时扩大基准性能与回答长度，复现 DeepSeek-R1-Zero 的 scaling 现象。用与 DeepSeek-R1-Zero-Qwen-32B 相同的 Qwen2.5-32B base，ORZ 在 AIME2024、MATH500、GPQA Diamond 上表现更优，且只需约 1/10 的训练步数。论文还分析训练动态与关键设计消融，并完整开源代码、数据与多个模型权重。

## 关键技术细节
- 极简配方：vanilla PPO + GAE（λ=1, γ=1），规则化（rule-based）正确性奖励，无 KL 正则、无奖励模型。
- 反直觉发现：去掉 KL 正则反而稳定且高效；学到的 critic 能识别并贬低重复模式，提供更稳健的优势估计。
- 效率：相同 base（Qwen2.5-32B）下，达到/超过 R1-Zero-Qwen-32B 仅需约 1/10 训练步。
- 结果：AIME2024、MATH500、GPQA Diamond 全面超过 DeepSeek-R1-Zero-Qwen-32B。
- 全开源：源码、训练数据、不同规模模型权重（0.5B–32B 系列）。

## 原始链接
- url: https://arxiv.org/abs/2503.24290
- pdf_url: https://arxiv.org/pdf/2503.24290
- github_url: https://github.com/Open-Reasoner-Zero/Open-Reasoner-Zero

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/open-reasoner-zero.pdf
