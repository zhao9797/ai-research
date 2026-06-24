---
title: "RAFT: Reward rAnked FineTuning for Generative Foundation Model Alignment"
org: HKUST / LMFlow
country: China
date: 2023-04
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2304.06767
pdf_url: https://arxiv.org/pdf/2304.06767
downloaded: [raft.pdf]
---

## 一句话定位
RAFT：用奖励模型对采样输出排序、只保留高分样本做监督微调的"拒绝采样微调"（reward-ranked / rejection sampling fine-tuning），作为 PPO 的简单稳定替代。

## 摘要（3-6 句）
RAFT 提出用奖励排序微调对齐生成模型：每轮从当前模型采样一批候选，用奖励模型打分，只取每个提示下分数最高的样本组成新的微调集，再做监督微调，迭代进行。相比 PPO，RAFT 实现简单、内存占用低、训练更稳定，无需价值网络与复杂超参。论文在 LLM 与扩散模型上验证其对齐效果，是后来 Llama-2 "rejection sampling" 与 best-of-n 微调路线的代表性方法之一。

## 关键技术细节
- 核心循环：采样 k 个候选 → RM 打分 → 取 top-1（或 top-k%）→ SFT，迭代。
- 与 PPO 对比：无需 critic/优势估计，显存与实现成本低；本质是 on-policy 的拒绝采样 + 模仿。
- 适用范围：LLM 文本对齐与文生图扩散模型；对奖励模型质量敏感。
- 优点：稳定、可解释、易调；缺点：样本利用率低于 PPO（丢弃低分样本）。

## 原始链接
- url: https://arxiv.org/abs/2304.06767
- pdf_url: https://arxiv.org/pdf/2304.06767

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/raft.pdf
