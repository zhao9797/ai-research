---
title: "OpenRLHF: An Easy-to-use, Scalable and High-performance RLHF Framework"
org: OpenRLHF community (含 ByteDance/NVIDIA 等贡献者)
country: China
date: 2024-05
type: paper
categories: [后训练, AI infra, agentic训练]
url: https://arxiv.org/abs/2405.11143
pdf_url: https://arxiv.org/pdf/2405.11143
github_url: https://github.com/OpenRLHF/OpenRLHF
downloaded: [openrlhf-2405.11143.pdf, openrlhf-readme.md]
---

## 一句话定位
首批开源、可扩展到 70B+ 的 RLHF 框架，基于 Ray + vLLM + ZeRO-3 解耦 actor/critic/reward/ref 四模型调度，是社区 PPO/RLHF 训练的常用基座。

## 摘要（3-6 句）
OpenRLHF 用 Ray 做分布式调度、vLLM 做高效生成、DeepSpeed ZeRO-3 做训练，把 RLHF 的四个模型（actor、critic、reward、reference）调度到不同 GPU 组并支持模型卸载，从而把 70B+ 模型的 PPO 训练做得既快又省卡。它对比 DeepSpeed-Chat 等更易用、扩展性更好，支持 PPO、DPO、KTO、拒绝采样等多种对齐算法。现已演进为支持 agentic RL（异步、多轮、VLM、REINFORCE++/DAPO 等）的框架。

## 关键技术细节
- 架构：Ray 编排 + vLLM 生成加速 + DeepSpeed ZeRO-3 训练；四模型（actor/critic/reward/ref）分组调度与 offload。
- 支持算法：PPO、DPO、KTO、Rejection Sampling、conditional SFT；后续加 REINFORCE++、GRPO、DAPO、async RL、VLM。
- 可扩展到 70B+ 模型 RLHF；相对 DeepSpeed-Chat 更快更省资源。
- 生成与训练分离，用 vLLM 显著加速 rollout（RLHF 的吞吐瓶颈）。

## 原始链接
- url: https://arxiv.org/abs/2405.11143
- pdf_url: https://arxiv.org/pdf/2405.11143
- github_url: https://github.com/OpenRLHF/OpenRLHF

## 一手源存档（sources/）
- [openrlhf-2405.11143.pdf](https://arxiv.org/pdf/2405.11143)  （arXiv 原文 PDF，不入 git）
- [openrlhf-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/openrlhf-readme.md)
