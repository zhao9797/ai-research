---
title: ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models
org: NVIDIA
country: US
date: 2025-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2505.24864
pdf_url: https://arxiv.org/pdf/2505.24864
github_url: https://huggingface.co/nvidia/Nemotron-Research-Reasoning-Qwen-1.5B
downloaded: [prorl.pdf]
---

## 一句话定位
ProRL：用"长时程 RL"正面回应"RL 只是放大 base 已有能力"的质疑，证明足够长 + 稳定的 RL 能让模型解出 base 怎么采样都解不出的新问题。

## 摘要（3-6 句）
学界争论 RL 是否真正扩展模型推理边界、还是只放大 base 分布里已有的高奖励输出。ProRL 提出延长 RL（prolonged RL）训练方法——结合 KL 散度控制、参考策略定期重置（reference policy resetting）、以及多样化任务套件——并通过实验反驳上述质疑：RL 训练后的模型在广泛 pass@k 评测上一致超过 base，包括 base 无论采样多少次都完全失败的场景。推理边界的提升与 base 任务能力及训练时长强相关，说明 RL 能随时间探索并填充新的解空间区域。开源 Nemotron-Research-Reasoning-Qwen-1.5B 权重。

## 关键技术细节
- 核心论点：充分长、充分稳定的 RL 能让模型获得 base 完全不可达的新推理策略（pass@k 在 base 全失败任务上 >0）。
- 三项稳定化技术：(1) KL 散度控制；(2) reference policy resetting（定期把参考策略重置为当前策略，避免 KL 项过度限制长训练）；(3) 多样化任务套件（数学、代码、STEM、逻辑谜题、指令遵循）。
- 算法：GRPO 基础上加上述改造（与 DAPO 的部分技巧结合）。
- 发现：边界扩展程度与 base 模型在该任务的初始能力、以及 RL 训练时长强正相关。
- 产出：Nemotron-Research-Reasoning-Qwen-1.5B（当时同规模开源 SOTA 推理模型），权重开源。

## 原始链接
- url: https://arxiv.org/abs/2505.24864
- pdf_url: https://arxiv.org/pdf/2505.24864
- model: https://huggingface.co/nvidia/Nemotron-Research-Reasoning-Qwen-1.5B

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/prorl.pdf
