---
title: "DeepResearcher: Scaling Deep Research via Reinforcement Learning in Real-world Environments"
org: "上海交通大学 / SII / GAIR"
country: CN
date: 2025-04
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2504.03160
pdf_url: https://arxiv.org/pdf/2504.03160
github_url: https://github.com/GAIR-NLP/DeepResearcher
downloaded: [deepresearcher-2504.03160.pdf]
---

## 一句话定位
首个在"真实开放网络"环境（真实搜索引擎 + 网页爬取）端到端 RL 训练 deep research agent 的工作：跳出本地静态 RAG 语料的"消毒沙盒"，直面噪声、动态、无结构的真实网页。

## 摘要
DeepResearcher 指出现有方法两类局限：prompt-engineering 型（脆弱）与"受控 RAG 环境内 RL"型（无法刻画真实网络交互的复杂性）。它是首个在真实环境、用真实网络搜索交互对 LLM deep research agent 做端到端 RL 训练的框架。与"假设所有所需信息都在固定语料库中"的 RAG 方法不同，DeepResearcher 训练 agent 去应对真实开放网的噪声、无结构与动态特性，并实现专门的多 agent 架构（browsing agent 从各类网页结构中抽取相关信息）。实验上比 prompt-engineering 基线最高高 28.9 分，比 RAG-based RL agent 最高高 7.2 分；并涌现出制定计划、跨源交叉验证、自我反思重定向、找不到答案时保持诚实等认知行为。

## 关键技术细节
- 基座：Qwen2.5-7B-Instruct；训练框架用 verl。
- RL 算法：GRPO（用一组 rollout 估计基线、免训练独立 critic），含 KL 正则项；仅用 outcome reward（结果奖励），无过程奖励、无 SFT。
- 采样配置：每步采样 256 个 prompt，每 prompt 16 个 rollout；mini-batch 4096；每条 rollout 最多 10 次 tool call 后接最终答案步。
- 真实环境工程：GRPO 大量采样导致海量搜索/爬取请求（如 4096 并发），为此自建 50 节点分布式 CPU 服务器集群处理 RL rollout 中的工具请求（搜索 + 按 URL 爬网页）；并处理网页爬取与 API 限额等真实挑战。多 agent 架构中 browsing agent 负责从网页中增量抽取相关信息。
- 训练数据配比：NQ:TQ:HotpotQA:2Wiki = 1:1:3:3，刻意强调多跳场景（75% 为多跳）。
- 评测：NQ/TQ/HotpotQA/2Wiki/Musique/Bamboogle/PopQA 共 7 个数据集，指标含 F1 与 MBE（model-based evaluation）；全部 7 个数据集上最优。
- 对比定位：相对 Search-R1、R1-Searcher、ReSearch（均在静态本地语料上做 RAG RL）强调"真实网络环境训练"是开发鲁棒研究能力的根本要求。

## 原始链接
- url: https://arxiv.org/abs/2504.03160
- pdf_url: https://arxiv.org/pdf/2504.03160
- github_url: https://github.com/GAIR-NLP/DeepResearcher

## 一手源存档（sources/）
- [deepresearcher-2504.03160.pdf](https://arxiv.org/pdf/2504.03160)  （arXiv 原文 PDF，不入 git）
