---
title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
org: DeepSeek
country: China
date: 2025-01
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2501.12948
pdf_url: https://arxiv.org/pdf/2501.12948
github_url: https://github.com/deepseek-ai/DeepSeek-R1
downloaded: [deepseek-r1.pdf]
---

## 一句话定位
通过纯强化学习（无需人工标注推理轨迹）激发大模型推理能力的开创性工作，DeepSeek-R1 与 R1-Zero 系列，2025 年初引爆"RL for reasoning"浪潮。

## 摘要
论文证明 LLM 的推理能力可以通过纯 RL（pure reinforcement learning）激励出来，无需依赖大量人工标注的 chain-of-thought 演示。R1-Zero 直接在 base 模型上做 RL，自发涌现出自我反思、验证、动态策略调整等高级推理模式；R1 则在 RL 前加入少量 cold-start 数据并采用多阶段训练以提升可读性与通用性。模型在数学、编程竞赛、STEM 等可验证任务上超越传统 SFT 训练的同类模型，并可将大模型涌现的推理模式蒸馏到小模型。v1 提交 2025-01-22，v2 修订 2026-01-04。

## 关键技术细节
- 训练范式：R1-Zero = DeepSeek-V3-Base 上直接做大规模 RL，无 SFT 冷启动；R1 = 多阶段（cold-start SFT → reasoning RL → 拒绝采样 SFT → 全场景 RL）。
- RL 算法：GRPO（Group Relative Policy Optimization），去掉 critic，用同一 prompt 的一组采样输出的相对优势估计 baseline，显著降低显存与算力开销。
- 奖励设计：以 rule-based 可验证奖励为主（数学答案正确性、代码编译/单测通过、格式奖励），不依赖 process reward model 或 MCTS。
- 基座：DeepSeek-V3-Base（671B 总参 / 37B 激活的 MoE）。
- 蒸馏：用 R1 生成数据蒸馏到 Qwen / Llama 系列（1.5B–70B），小模型显著超越同尺寸 RL 模型。
- 涌现现象："aha moment"——模型在 RL 中自发增加思考长度、回溯重审。

## 原始链接
- url: https://arxiv.org/abs/2501.12948
- pdf_url: https://arxiv.org/pdf/2501.12948
- github_url: https://github.com/deepseek-ai/DeepSeek-R1

## 一手源存档（sources/）
- deepseek-r1.pdf  （PDF 不入 git，走 HF bucket）
