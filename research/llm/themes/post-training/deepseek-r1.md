---
title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
org: DeepSeek-AI
country: China
date: 2025-01
type: paper
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2501.12948
pdf_url: https://arxiv.org/pdf/2501.12948
github_url: https://github.com/deepseek-ai/DeepSeek-R1
downloaded: [deepseek-r1.pdf]
---

## 一句话定位
DeepSeek-R1：证明纯 RL（无 SFT 冷启动）即可让模型自发涌现长 CoT 与"顿悟时刻"（R1-Zero），并用多阶段 RL + 冷启动得到对标 o1 的 R1，是 RLVR/reasoning RL 路线的标志性开源工作。

## 摘要（3-6 句）
论文给出两个模型。DeepSeek-R1-Zero：直接在 DeepSeek-V3-Base 上用纯 RL（GRPO + 规则化可验证奖励，无任何 SFT）训练，模型自发涌现自我验证、反思、长 CoT，AIME 2024 pass@1 从 15.6% 升到 71.0%（多数投票 86.7%），出现"aha moment"；但有可读性差、语言混杂问题。DeepSeek-R1：引入少量冷启动 CoT 数据 + 多阶段（推理 RL → 拒绝采样 SFT → 全场景 RL）流程，性能对标 OpenAI o1-1217。还把 R1 的推理能力蒸馏到 Qwen/Llama 系列（1.5B–70B），1.5B 蒸馏模型即超过 GPT-4o/Claude-3.5 的数学表现。模型与蒸馏权重全部开源。

## 关键技术细节
- 基座：DeepSeek-V3-Base（671B MoE，37B 激活）。
- RL 算法：GRPO（组相对策略优化，无 critic）。
- 奖励：规则化可验证奖励（RLVR）——准确率奖励（数学答案/代码编译+用例）+ 格式奖励（强制 <think>...</think>），R1-Zero 不用 RM、不用过程奖励/MCTS（作者称其难规模化）。
- R1-Zero 结果：AIME 2024 pass@1 15.6%→71.0%，cons@16 86.7%；自发涌现长思维链与反思。
- R1 多阶段：冷启动数千条长 CoT SFT → 推理导向 RL（加语言一致性奖励）→ 拒绝采样生成约 60 万推理 + 20 万通用 SFT 数据 → 覆盖全场景的二次 RL（含 helpfulness/harmlessness）。
- 蒸馏：用 R1 生成的 80 万样本 SFT Qwen2.5/Llama（1.5B/7B/8B/14B/32B/70B），蒸馏 > 直接对小模型做 RL。
- 开源：R1-Zero、R1、6 个蒸馏模型权重（MIT）。

## 原始链接
- url: https://arxiv.org/abs/2501.12948
- pdf_url: https://arxiv.org/pdf/2501.12948
- github_url: https://github.com/deepseek-ai/DeepSeek-R1

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/deepseek-r1.pdf
