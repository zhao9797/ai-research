---
title: "Kimi k1.5: Scaling Reinforcement Learning with LLMs"
org: Moonshot AI (月之暗面)
country: China
date: 2025-01
type: report
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2501.12599
pdf_url: https://arxiv.org/pdf/2501.12599
github_url: https://github.com/MoonshotAI/Kimi-k1.5
downloaded: [kimi-k1.5.pdf]
---

## 一句话定位
Kimi k1.5：与 R1 同期的多模态推理 RL 报告，主张"长上下文 RL（long context scaling）+ 改进策略优化"，并提出把长 CoT 蒸馏成高效短 CoT（long2short）。

## 摘要（3-6 句）
Kimi k1.5 用强化学习把推理能力作为"continued scaling"的新轴，关键发现是把 RL 的上下文窗口扩到很长（最高 128K）能持续提升性能，且不必依赖 MCTS、价值函数或过程奖励等复杂方法——简单的策略优化 + 长上下文即可。它给出 long-CoT 与 short-CoT 两套配方，并提出 long2short 技术把长思维链模型的推理能力蒸馏/合并进短 CoT 模型，在有限 token 预算下仍强。long-CoT 版在 AIME、MATH-500、Codeforces、MathVista 等达到 o1 级别；short-CoT 版大幅超过 GPT-4o、Claude 3.5 Sonnet。

## 关键技术细节
- 多模态：文本 + 视觉联合 RL 训练。
- 长上下文 RL：RL 训练上下文扩到 128K，发现"context length scaling"是性能提升关键；用 partial rollouts 提高长序列 RL 效率。
- 策略优化：用在线镜像下降（online mirror descent）变体的策略优化 + 长度惩罚，刻意避免 MCTS/value function/PRM 等复杂组件（认为简单方法 + 长上下文已足够）。
- 奖励：以可验证正确性为主（数学/代码），加采样与课程、优先采样策略。
- long2short：用模型合并、最短拒绝采样、DPO、long2short RL 把长 CoT 能力压进短 CoT，提升 token 效率。
- 结果：long-CoT k1.5 在 AIME 77.5、MATH-500 96.2、Codeforces 94 百分位、MathVista 74.9（达 o1 级）；short-CoT 在多基准超 GPT-4o / Claude 3.5 Sonnet（如 AIME 60.8、MATH-500 94.6）。

## 原始链接
- url: https://arxiv.org/abs/2501.12599
- pdf_url: https://arxiv.org/pdf/2501.12599
- github_url: https://github.com/MoonshotAI/Kimi-k1.5

## 一手源存档（sources/）
- kimi-k1.5.pdf  （PDF 不入 git，走 HF bucket）
