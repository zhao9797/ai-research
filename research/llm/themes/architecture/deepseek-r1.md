---
title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
org: DeepSeek-AI
country: China
date: 2025-01
type: report
categories: [后训练, 架构, agentic训练]
url: https://arxiv.org/abs/2501.12948
pdf_url: https://arxiv.org/pdf/2501.12948
github_url: https://github.com/deepseek-ai/DeepSeek-R1
downloaded: [deepseek-r1.pdf]
---

## 一句话定位
DeepSeek-R1 证明纯强化学习（无需人工标注推理轨迹）就能激发 LLM 的复杂推理能力，并把这种能力蒸馏进小模型，是 RLVR / 推理模型范式的里程碑。

## 摘要（3-6 句）
通用推理是 AI 长期难题，且以往依赖大量人工标注示范。DeepSeek-R1 展示：通过纯强化学习即可激励 LLM 的推理能力，无需人工标注的推理轨迹。其 RL 框架让自我反思、验证、动态策略调整等高级推理模式自发涌现，使模型在数学、编程竞赛、STEM 等可验证任务上超过用人工示范监督训练的同类模型。涌现的推理模式还能系统性地蒸馏到更小模型以提升其推理能力。

## 关键技术细节
- DeepSeek-R1-Zero：在 DeepSeek-V3-Base 上直接做大规模 RL（无 SFT 冷启动），用 GRPO + 规则化可验证奖励（RLVR：答案正确性 + 格式奖励），推理能力自发涌现（含 "aha moment"、长 CoT）。
- DeepSeek-R1：加入少量冷启动 CoT 数据 + 多阶段 RL（推理 RL → 拒绝采样 SFT → 全场景 RL）以提升可读性与通用性。
- 算法：GRPO（Group Relative Policy Optimization），无需价值网络，用组内相对优势估计。
- 蒸馏：把 R1 的推理轨迹蒸馏进 Qwen/Llama 系 1.5B–70B 小模型，显著提升其推理；32B 蒸馏模型超过 o1-mini。
- 在 AIME、MATH-500、Codeforces、GPQA 等可验证任务上对标 OpenAI o1。

## 原始链接
- url: https://arxiv.org/abs/2501.12948
- pdf_url: https://arxiv.org/pdf/2501.12948
- github_url: https://github.com/deepseek-ai/DeepSeek-R1

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/deepseek-r1.pdf
