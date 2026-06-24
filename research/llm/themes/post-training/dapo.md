---
title: "DAPO: An Open-Source LLM Reinforcement Learning System at Scale"
org: ByteDance Seed / Tsinghua AIR
country: China
date: 2025-03
type: paper
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2503.14476
pdf_url: https://arxiv.org/pdf/2503.14476
github_url: https://github.com/BytedTsinghua-SIA/DAPO
downloaded: [dapo.pdf]
---

## 一句话定位
DAPO：完全开源的大规模 RL 系统（算法+代码+数据），用四项关键技术修复 GRPO，在 Qwen2.5-32B 上仅用 50% 步数即达 AIME 2024 50 分，超过 DeepSeek-R1-Zero-Qwen-32B。

## 摘要（3-6 句）
针对 o1/R1 隐藏关键 RL 细节、社区难复现的问题，DAPO 提出 Decoupled Clip and Dynamic sAmpling Policy Optimization 算法，并完整开源基于 verl 框架的大规模 RL 系统与精心处理的数据集。DAPO 用 Qwen2.5-32B base 在 AIME 2024 上达到 50 分，且训练步数仅为 DeepSeek-R1-Zero-Qwen-32B 的一半。论文公开四项让大规模 RL 成功的关键技术，强调可复现性。

## 关键技术细节
- 四项关键技术：(1) Clip-Higher——解耦上下裁剪边界、放宽上界，缓解熵坍缩、保探索；(2) Dynamic Sampling——过滤掉组内全对或全错（优势为 0）的 prompt，提升梯度有效性与训练效率；(3) Token-Level Policy Gradient Loss——按 token 而非按样本平均，避免长样本被稀释；(4) Overlong Reward Shaping——对超长截断回答做软惩罚，降低奖励噪声。
- 算法基础：GRPO（无 critic 组相对优势），针对其稳定性问题改造。
- 系统：基于字节 verl RL 框架，全开源训练代码 + 处理好的数学数据集（DAPO-Math-17K）。
- 结果：Qwen2.5-32B base → AIME 2024 50 分（超过 DeepSeek-R1-Zero-Qwen-32B 的 47），训练步数减半。
- 意义：把"大规模可验证奖励 RL"的工程细节彻底开源，成为后续 RL 系统的参考实现。

## 原始链接
- url: https://arxiv.org/abs/2503.14476
- pdf_url: https://arxiv.org/pdf/2503.14476
- github_url: https://github.com/BytedTsinghua-SIA/DAPO

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/dapo.pdf
