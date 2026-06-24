---
title: DeepSeek-V3.2 (含 V3.2-Exp / DeepSeek Sparse Attention)
org: DeepSeek
country: China
date: 2025-12
type: paper
categories: [架构, AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2512.02556
pdf_url: https://arxiv.org/pdf/2512.02556
github_url: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp
downloaded: [deepseek-v3.2.pdf, deepseek-v3.2-exp.html]
---

## 一句话定位
DeepSeek-V3.2 引入 DeepSeek Sparse Attention（DSA）细粒度稀疏注意力，大幅降低长上下文训练/推理成本，配合可扩展 RL 框架性能对标 GPT-5。V3.2-Exp 2025-09-29 先行实验版，V3.2 正式版 2025-12-02 论文。

## 摘要
DeepSeek-V3.2 兼顾极高计算效率与顶级推理/agent 性能。两大技术突破：(1) DeepSeek Sparse Attention (DSA)——高效注意力机制，在长上下文场景下大幅降低计算复杂度而几乎不损性能；(2) 可扩展 RL 框架——通过稳健 RL 协议并扩大后训练算力，使 V3.2 表现可与 GPT-5 比肩。V3.2-Exp 基于 V3.1-Terminus，是首次落地 DSA 的实验版，API 价格因此下调 50%+。

## 关键技术细节
- 架构：DeepSeek Sparse Attention (DSA)，细粒度 sparse attention（lightning indexer + top-k token 选择），长上下文推理质量基本无损。
- 效率：长上下文训练与推理算力显著下降；API 价格下调 50%+。
- 后训练：scalable RL 框架，扩大后训练 compute，性能对标 GPT-5；强化推理与 agent。
- 基座：V3.2-Exp 基于 V3.1-Terminus（V3 家族 671B MoE / 37B 激活）。
- 开源：V3.2-Exp 与 V3.2 权重发布于 HuggingFace；GitHub deepseek-ai/DeepSeek-V3.2-Exp。

## 原始链接
- url: https://arxiv.org/abs/2512.02556
- pdf_url: https://arxiv.org/pdf/2512.02556
- github_url: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp
- 发布说明: https://api-docs.deepseek.com/news/news250929

## 本地落盘文件
- ../../../sources/llm/2025/deepseek-v3.2.pdf
- ../../../sources/llm/2025/deepseek-v3.2-exp.html
