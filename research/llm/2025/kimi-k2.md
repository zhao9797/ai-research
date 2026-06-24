---
title: "Kimi K2: Open Agentic Intelligence"
org: 月之暗面 Moonshot AI
country: China
date: 2025-07
type: paper
categories: [架构, AI infra, 预训练数据, 后训练, agentic训练]
url: https://arxiv.org/abs/2507.20534
pdf_url: https://arxiv.org/pdf/2507.20534
github_url: https://github.com/MoonshotAI/Kimi-K2
downloaded: [kimi-k2.pdf]
---

## 一句话定位
1T 总参 / 32B 激活的开源 MoE，提出 MuonClip 优化器（Muon + QK-clip）在 15.5T token 上零 loss spike 预训练，主打 agentic 能力（非 thinking 模式开源 SOTA）。发布 2025-07-28。

## 摘要
Kimi K2 是 1 万亿总参、激活 320 亿的 MoE 模型。提出 MuonClip 优化器：在 Muon 基础上引入 QK-clip 技术解决训练不稳定，同时保留 Muon 的高 token 效率，K2 在 15.5T token 上预训练全程零 loss spike。后训练为多阶段流程，亮点是大规模 agentic 数据合成 pipeline 与联合 RL 阶段（模型通过与真实/合成环境交互提升能力）。K2 在开源 non-thinking 模型中 SOTA，agentic 能力突出：Tau2-Bench 66.1、ACEBench(En) 76.5、SWE-Bench Verified 65.8、SWE-Bench Multilingual 47.3、LiveCodeBench v6 53.7、AIME 2025 49.5、GPQA-Diamond 75.1。

## 关键技术细节
- 架构：1T 总参 / 32B 激活 MoE（DeepSeek-V3 类架构，384 专家选 8，MLA 注意力，1 个共享专家）。
- 优化器：MuonClip = Muon + QK-clip（裁剪 query/key 的最大 logit 控制 attention 爆炸），15.5T token 零 loss spike。
- 预训练数据：15.5T tokens；强调 token 效率（rephrasing 提高数据利用）。
- 后训练：大规模 agentic 数据合成 pipeline（合成工具使用轨迹）+ SFT + 联合 RL（真实/合成环境交互，verifiable + self-critique reward）。
- 定位：non-thinking（不含显式 long CoT）即达 agentic SOTA。
- 开源：base + instruct 权重，MIT-like 协议。

## 原始链接
- url: https://arxiv.org/abs/2507.20534
- pdf_url: https://arxiv.org/pdf/2507.20534
- github_url: https://github.com/MoonshotAI/Kimi-K2

## 本地落盘文件
- ../../../sources/llm/2025/kimi-k2.pdf
