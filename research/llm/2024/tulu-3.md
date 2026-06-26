---
title: "Tulu 3: Pushing Frontiers in Open Language Model Post-Training"
org: Allen Institute for AI (AI2)
country: US
date: 2024-11
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2411.15124
pdf_url: https://arxiv.org/pdf/2411.15124
github_url: https://github.com/allenai/open-instruct
downloaded: [2411.15124.pdf]
---

## 一句话定位
Tulu 3：完全开放的 SOTA 后训练模型族与配方，首次提出 RLVR（可验证奖励强化学习），公开数据/代码/recipe 全栈。

## 摘要
后训练用于精炼行为、解锁新技能，但开放配方落后于闭源。Tulu 3 是基于 Llama 3.1 base 的完全开放后训练模型族，连同数据、代码、训练配方一起发布，作为现代后训练技术的完整指南。其结果超过 Llama 3.1 的 instruct 版以及 Qwen 2.5、Mistral，甚至闭源的 GPT-4o-mini 与 Claude 3.5-Haiku。训练算法包括 SFT、DPO，以及新方法 RLVR（Reinforcement Learning with Verifiable Rewards）。还引入多任务评测方案（含 unseen 评测）、标准基准实现与对开放数据的去污染。

## 关键技术细节
- 四阶段配方：数据 curation → SFT → 偏好微调（DPO）→ RLVR。
- RLVR：对有可验证答案的任务（数学 GSM8K/MATH、精确指令遵循 IFEval），仅当答案/格式可被程序验证为正确才给奖励（用 PPO/GRPO 风格 RL），避免 reward hacking。
- 基座：Llama 3.1 8B / 70B base；后续有 405B。
- 全开放：SFT/偏好/RLVR 数据集、训练代码（open-instruct）、评测工具（含去污染）、详细复现报告。
- 评测：开发集 + unseen 评测；超 Llama 3.1-Instruct、Qwen 2.5、GPT-4o-mini、Claude 3.5-Haiku。

## 原始链接
- url: https://arxiv.org/abs/2411.15124
- pdf_url: https://arxiv.org/pdf/2411.15124
- github: https://github.com/allenai/open-instruct

## 一手源存档（sources/）
- [2411.15124.pdf](https://arxiv.org/pdf/2411.15124)  （arXiv 原文 PDF，不入 git）
