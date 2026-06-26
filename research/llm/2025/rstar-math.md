---
title: rStar-Math - Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking
org: Microsoft Research Asia
country: US
date: 2025-01
type: technical-report
categories: [后训练]
url: https://arxiv.org/abs/2501.04519
pdf_url: https://arxiv.org/pdf/2501.04519
github_url:
downloaded: [files/rstar-math.pdf]
---

## 一句话定位
Microsoft Research Asia 2025-01 的 rStar-Math：证明小模型（SLM）无需从更强模型蒸馏，靠 MCTS 深度思考 + 过程奖励模型 + 自演化，即可在数学推理上媲美甚至超越 OpenAI o1。

## 摘要
rStar-Math 让 SLM 通过 MCTS（蒙特卡洛树搜索）做 test-time 搜索，由一个 SLM 过程奖励模型（PPM）引导。三大创新：(1) code-augmented CoT 数据合成——大量 MCTS rollout 生成逐步验证的推理轨迹训练 policy SLM；(2) 新过程奖励模型训练法，避免朴素 step-level 标注，得到更有效的 process preference model (PPM)；(3) 自演化配方——policy SLM 与 PPM 从零开始迭代共同进化。经 4 轮自演化、对 747k 数学题合成数百万解，把 SLM 数学推理推到 SOTA。

## 关键技术细节（带数字）
- 方法：MCTS 深度思考 + SLM-based 过程奖励模型（PPM）引导 test-time 搜索；无需从更强模型蒸馏。
- 数据：code-augmented CoT 合成，747k 数学问题，数百万合成解；4 轮 self-evolution。
- MATH 基准：Qwen2.5-Math-7B 从 58.8% → 90.0%；Phi3-mini-3.8B 从 41.4% → 86.4%；分别超 o1-preview +4.5% / +0.9%。
- AIME（USAMO）：显著提升（详见原文）。
- 创新点：避免朴素 step-level 标注的 PPM 训练法；policy SLM 与 PPM 从零自演化。
- 发布日期：2025-01（arXiv:2501.04519）。

## 原始链接
- arXiv：https://arxiv.org/abs/2501.04519
- PDF：https://arxiv.org/pdf/2501.04519

## 一手源存档（sources/）
- rstar-math.pdf  （PDF 不入 git，走 HF bucket）
