---
title: "Seed1.5-Thinking: Advancing Superb Reasoning Models with Reinforcement Learning"
org: ByteDance Seed
country: China
date: 2025-04
type: report
categories: [后训练, AI infra, 架构]
url: https://arxiv.org/abs/2504.13914
pdf_url: https://arxiv.org/pdf/2504.13914
github_url: https://github.com/ByteDance-Seed/Seed-Thinking-v1.5
downloaded: [seed-thinking-v1.5.pdf]
---

## 一句话定位
字节 Seed1.5-Thinking：MoE 推理模型（200B 总参 / 20B 激活），用大规模可验证 + 不可验证奖励 RL，提出 VAPO/DAPO 系列稳定化技术与定制 RL 基础设施。

## 摘要（3-6 句）
Seed1.5-Thinking 是字节跳动的推理模型，采用 MoE 架构（约 200B 总参数、20B 激活），通过强化学习激发"先思考再回答"。报告在数据（可验证的 STEM/代码 + 不可验证的开放任务两类奖励）、RL 算法（针对训练不稳定提出的改进，与同团队 VAPO、DAPO 相关）、以及 RL 基础设施（高效 rollout、异步训练）三方面给出工程细节。它在 AIME 2024、Codeforces、GPQA 等达到顶尖水平，并在 BeyondAIME 等更难基准上保持优势，整体可比 o3-mini / R1 级别。

## 关键技术细节
- 架构：MoE，约 200B 总参数 / 20B 激活参数。
- 数据：两类奖励——可验证任务（数学、代码，用 verifier/沙箱）+ 不可验证任务（用奖励模型评判开放式回答）。
- RL 稳定化：针对长 CoT RL 的训练崩溃问题，采用 value-based（VAPO）与 DAPO 系列技术（如 token-level loss、dynamic sampling、value pretraining、length-adaptive GAE 等）提升稳定性。
- infra：自研 RL 训练系统，强调高效 rollout（流式生成）、异步/解耦的 actor-learner、奖励服务（代码沙箱、数学验证）。
- 评测：AIME 2024 高分、Codeforces、GPQA Diamond 领先；提出 BeyondAIME 更难数学基准。

## 原始链接
- url: https://arxiv.org/abs/2504.13914
- pdf_url: https://arxiv.org/pdf/2504.13914
- github_url: https://github.com/ByteDance-Seed/Seed-Thinking-v1.5

## 一手源存档（sources/）
- seed-thinking-v1.5.pdf  （PDF 不入 git，走 HF bucket）
