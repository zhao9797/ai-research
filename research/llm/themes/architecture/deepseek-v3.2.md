---
title: "DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models"
org: DeepSeek-AI
country: China
date: 2025-12
type: paper
categories: [架构, AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2512.02556
pdf_url: https://arxiv.org/pdf/2512.02556
downloaded: [deepseek-v3.2-arxiv.pdf]
---

## 一句话定位
DeepSeek-V3.2（2025-12 正式版）把 DeepSeek Sparse Attention、可扩展 RL 框架和大规模 agentic 任务合成结合，高算力变体 V3.2-Speciale 在 2025 IMO/IOI 拿金牌、对标 GPT-5/Gemini-3.0-Pro。

## 摘要（3-6 句）
DeepSeek-V3.2 兼顾高算力效率与卓越推理/agent 性能，三大突破：(1) DeepSeek Sparse Attention (DSA)——在长上下文下大幅降低注意力复杂度且保持性能；(2) 可扩展强化学习框架——通过稳健 RL 协议 + 扩大后训练算力，使 V3.2 与 GPT-5 相当，高算力变体 V3.2-Speciale 超过 GPT-5、推理与 Gemini-3.0-Pro 相当，在 2025 IMO 和 IOI 均达金牌水平；(3) 大规模 agentic 任务合成流水线——系统化生成工具使用训练数据，实现可扩展的 agentic 后训练，显著提升复杂交互环境下的泛化与指令遵循。

## 关键技术细节
- 架构：DSA（lightning indexer + top-k 细粒度 KV 选择）叠加 V3 的 MLA + DeepSeekMoE（671B 总参 / 37B 激活级别）。
- 变体：DeepSeek-V3.2-Thinking、DeepSeek-V3.2-Speciale（高算力推理变体）。
- 强化学习：scalable RL 框架，扩大后训练算力；推理基准 AIME 2025 ~96.0、HMMT 2025、HLE、Codeforces Rating ~2700+。
- agentic：新型 agentic 任务合成 pipeline，提升 SWE-Verified、Terminal-Bench 2.0、Tool Decathlon 等工具使用/agent 基准。
- 成绩：V3.2-Speciale 在 2025 IMO、IOI 达金牌；与 GPT-5-High、Claude-4.5-Sonnet、Gemini-3.0-Pro 对标。
- 发布于 2025-12（arXiv 2512.02556）；区别于 2025-09 的实验版 DeepSeek-V3.2-Exp。

## 原始链接
- url: https://arxiv.org/abs/2512.02556
- pdf_url: https://arxiv.org/pdf/2512.02556

## 一手源存档（sources/）
- deepseek-v3.2-arxiv.pdf  （PDF 不入 git，走 HF bucket）
