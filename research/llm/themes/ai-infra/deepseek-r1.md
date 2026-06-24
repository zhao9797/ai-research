---
title: DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
org: DeepSeek-AI
country: China
date: 2025-01
type: report
categories: [后训练, agentic训练, AI infra]
url: https://arxiv.org/abs/2501.12948
pdf_url: https://arxiv.org/pdf/2501.12948
github_url: https://github.com/deepseek-ai/DeepSeek-R1
downloaded: [deepseek-r1-2501.12948.pdf]
---

## 一句话定位
用纯 RL（GRPO + 规则化可验证奖励 RLVR）在 DeepSeek-V3-Base 上激发推理能力的旗舰报告：R1-Zero 完全无 SFT、R1 加冷启动，开源并蒸馏到小模型。

## 摘要（3-6 句）
DeepSeek-R1-Zero 直接在 base 模型上做大规模 RL（GRPO，奖励来自规则化的答案正确性与格式，即 RLVR），无任何 SFT 即涌现长链推理、自我验证、反思（"aha moment"），但有可读性/语言混杂问题。DeepSeek-R1 加入少量冷启动 CoT 数据 + 多阶段 RL 解决之，推理性能比肩 OpenAI o1。论文还把 R1 的推理蒸馏到 Qwen/Llama 系列 1.5B–70B dense 模型，开源全部权重，是推理型后训练的里程碑一手报告。

## 关键技术细节
- R1-Zero：DeepSeek-V3-Base 上纯 RL（GRPO），rule-based reward（accuracy + format），无 SFT；涌现 self-verification、reflection、长 CoT。
- R1：cold-start CoT 数据 → reasoning RL → 拒绝采样 SFT → 全场景 RL，四阶段；性能对标 o1-1217。
- RLVR：可验证奖励（数学有标准答案、代码可执行），避免奖励模型 hacking。
- 蒸馏：把 R1 输出 SFT 到 Qwen2.5/Llama3 的 1.5B/7B/8B/14B/32B/70B，小模型推理大幅提升；全开源。

## 原始链接
- url: https://arxiv.org/abs/2501.12948
- pdf_url: https://arxiv.org/pdf/2501.12948
- github_url: https://github.com/deepseek-ai/DeepSeek-R1

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/deepseek-r1-2501.12948.pdf
