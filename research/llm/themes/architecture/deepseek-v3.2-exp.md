---
title: "DeepSeek-V3.2-Exp: Boosting Long-Context Efficiency with DeepSeek Sparse Attention"
org: DeepSeek-AI
country: China
date: 2025-09
type: report
categories: [架构, AI infra]
url: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp
pdf_url: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp/raw/main/DeepSeek_V3_2.pdf
github_url: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp
downloaded: [deepseek-v3.2-exp.pdf]
---

## 一句话定位
DeepSeek-V3.2-Exp 在 V3.1-Terminus 基础上唯一架构改动是引入 DeepSeek Sparse Attention (DSA)：用 lightning indexer + top-k 细粒度选择，把长上下文训练/推理成本大幅压低。

## 摘要（3-6 句）
DeepSeek-V3.2-Exp 是实验性稀疏注意力模型，通过继续训练给 DeepSeek-V3.1-Terminus 装上 DeepSeek Sparse Attention (DSA)。DSA 是由 lightning indexer 驱动的细粒度稀疏注意力，在长上下文场景显著提升训练与推理效率。相比 V3.1-Terminus，唯一架构修改就是引入 DSA（通过 continued training）。模型检查点已在 HuggingFace 开放。

## 关键技术细节
- DSA 两部分：① lightning indexer——用少量 indexer 头计算 query 对历史 token 的 index score（ReLU 激活、可 FP8 实现，计算极省），决定关注哪些 token；② fine-grained token selection——只对 top-k 的 KV 条目做注意力。
- index score 公式：I_{t,s} = Σ_j w_{t,j} · ReLU(q_{t,j}·k_s)，按 top-k 选 KV。
- 基础架构继承 V3.1-Terminus（即 V3 的 MLA + DeepSeekMoE + auxiliary-loss-free + MTP）。
- 仅通过 continued training 引入 DSA，沿用 V3 系列权重；显著降低长上下文 attention 复杂度。
- 是 NSA（训练侧）思路在生产模型上的工程落地，叠加 MLA 的 KV 压缩。
- 发布于 2025-09（官方 GitHub/HF，技术报告 PDF 随仓库发布）。

## 原始链接
- url: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp
- pdf_url: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp/raw/main/DeepSeek_V3_2.pdf
- github_url: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp

## 一手源存档（sources/）
- deepseek-v3.2-exp.pdf  （PDF 不入 git，走 HF bucket）
