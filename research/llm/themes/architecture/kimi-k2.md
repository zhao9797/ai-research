---
title: "Kimi K2: Open Agentic Intelligence (Technical Report)"
org: Moonshot AI (Kimi Team)
country: China
date: 2025-07
type: report
categories: [架构, AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2507.20534
pdf_url: https://arxiv.org/pdf/2507.20534
github_url: https://github.com/MoonshotAI/Kimi-K2
downloaded: [kimi-k2.pdf, kimi-k2-techreport.pdf]
---

## 一句话定位
Kimi K2 是 Moonshot 的 1T 总参/32B 激活 MoE 大模型，提出 MuonClip 优化器（Muon + QK-clip）实现 15.5T token 零 loss spike 预训练，强在 agentic 与 coding。

## 摘要（3-6 句）
Kimi K2 是 32B 激活、1T 总参的 MoE 大模型。作者提出 MuonClip 优化器——在 Muon 基础上加 QK-clip 技术解决训练不稳，同时保留 Muon 的高 token 效率；基于 MuonClip，K2 在 15.5T token 上零 loss spike 完成预训练。后训练为多阶段，亮点是大规模 agentic 数据合成流水线和联合强化学习阶段（与真实/合成环境交互）。K2 在开源 non-thinking 模型中 SOTA，尤其 agentic 能力：Tau2-Bench 66.1、ACEBench(En) 76.5、SWE-Bench Verified 65.8、SWE-Bench Multilingual 47.3，并在 coding/数学/推理上强（LiveCodeBench v6 53.7、AIME 2025 49.5、GPQA-Diamond 75.1）。

## 关键技术细节
- 规模：1T 总参 / 32B 激活 MoE；细粒度专家（沿 DeepSeek 风格 MoE 设计）。
- MuonClip：Muon 优化器 + QK-clip（对 attention logits 的 Q/K 做 clip 防 attention logit 爆炸），解决大规模训练 loss spike。
- 预训练：15.5T token，零 loss spike。
- 后训练：大规模 agentic 数据合成 pipeline（工具使用轨迹）+ 联合 RL（真实 + 合成环境交互）。
- 强项：agentic/工具使用与软件工程；SWE-Bench Verified 65.8（non-thinking）。
- 开源 base + 指令模型权重。

## 原始链接
- url: https://arxiv.org/abs/2507.20534
- pdf_url: https://arxiv.org/pdf/2507.20534
- github_url: https://github.com/MoonshotAI/Kimi-K2

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/kimi-k2.pdf
- ../../../../sources/llm/themes/architecture/kimi-k2-techreport.pdf
