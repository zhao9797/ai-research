---
title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
org: "DeepSeek-AI (深度求索)"
country: China
date: 2025-01
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2501.12948
pdf_url: https://arxiv.org/pdf/2501.12948
github_url: https://github.com/deepseek-ai/DeepSeek-R1
downloaded: [deepseek-r1-2501.12948.pdf]
---

## 一句话定位
纯 RL(无 SFT 冷启动)即可激发强推理：DeepSeek-R1-Zero 用 GRPO + 规则化可验证奖励(RLVR) 让推理能力自发涌现，奠定 2025 "agentic RL/工具 RL"浪潮的算法底座(GRPO 被 Search-R1/ReTool/ToolRL 等广泛采用)。

## 摘要
DeepSeek 推出第一代推理模型 DeepSeek-R1-Zero 与 DeepSeek-R1。R1-Zero 在基座模型上直接做大规模强化学习(不经监督微调冷启动)，展现出强大的推理行为自发涌现(自我验证、反思、长链推理)，但有可读性差、语言混杂等问题。R1 引入多阶段训练与冷启动数据再做 RL，缓解上述问题并进一步提升推理，在数学、代码、推理任务上达到与 OpenAI-o1-1217 相当的水平。作者开源 R1-Zero、R1，以及从 R1 蒸馏到 Qwen/Llama 的 1.5B-70B 系列稠密模型。

## 关键技术细节
- 基座：DeepSeek-V3-Base(671B MoE, 37B 激活)。
- RL 算法：GRPO(Group Relative Policy Optimization)——去掉 critic，用组内相对优势估计，省显存、适合大模型 RL。
- 奖励：规则化可验证奖励(RLVR)——数学答案/代码测试等可自动判定的结果奖励 + 格式奖励，而非神经奖励模型，避免 reward hacking。
- R1-Zero：跳过 SFT，直接 RL，推理能力(含"aha moment"长思考)自发涌现；AIME 2024 pass@1 从 15.6% 提到 71.0%(多数投票 86.7%)。
- R1：冷启动 SFT → 推理 RL → 拒绝采样 SFT → 全场景 RL 的多阶段管线；性能对标 o1-1217。
- 蒸馏：把 R1 推理蒸到 Qwen2.5/Llama 的 1.5B/7B/8B/14B/32B/70B。
- 对 agentic 的意义：GRPO + RLVR 成为后续工具/搜索/agent RL(Search-R1、ReTool、ToolRL、WebSailor 等)的事实标准训练方法。

## 原始链接
- url: https://arxiv.org/abs/2501.12948
- pdf_url: https://arxiv.org/pdf/2501.12948
- github_url: https://github.com/deepseek-ai/DeepSeek-R1

## 一手源存档（sources/）
- [deepseek-r1-2501.12948.pdf](https://arxiv.org/pdf/2501.12948)  （arXiv 原文 PDF，不入 git）
