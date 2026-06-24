---
title: "Ling and Ring 2.6 Technical Report: Efficient and Instant Agentic Intelligence at Trillion-Parameter Scale"
org: 蚂蚁 InclusionAI / Ant Group (Ling Team)
country: China
date: 2026-06
type: paper
categories: [架构, AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2606.15079
pdf_url: https://arxiv.org/pdf/2606.15079
github_url: https://github.com/inclusionAI
downloaded: [ling-ring-2.6.pdf]
---

## 一句话定位
蚂蚁 InclusionAI 的 Ling-2.6（即时响应）与 Ring-2.6（深度推理）万亿级 MoE 模型族，通过"架构迁移预训练 + 大规模后训练"从 Ling-2.0 升级，引入 Lightning Attention + MLA 混合线性注意力。

## 摘要
Ling-2.6 与 Ring-2.6（arXiv 2026-06-13，作者 Ang Li 等 218 人）是一族面向高效可扩展 agentic 智能的模型：Ling-2.6 优化即时响应与每输出 token 的高能力密度；Ring-2.6 面向更深推理与高级 agentic 工作流。不从零训练，而是通过"架构迁移预训练（architectural migration pre-training）+ 大规模后训练"从 Ling-2.0 基座升级，由模型架构、优化目标、serving 系统、agent 训练环境的统一协同设计指导，同时提升能力与部署效率。架构层引入 hybrid linear attention——把 Lightning Attention 与 MLA 整合，提升长上下文训练与解码效率。为提升 token 效率，通过 Evolutionary Chain-of-Thought、Linguistic Unit Policy Optimization、双向（bidirectional）等手段优化每输出 token 的能力。

## 关键技术细节
- **模型族**：Ling-2.6（即时响应 / 高能力密度每 token）+ Ring-2.6（深度推理 / 高级 agentic）；trillion-parameter scale。
- **升级方式**：不从头训练；architectural migration pre-training + 大规模 post-training，从 Ling-2.0 基座升级。
- **架构-混合线性注意力**：hybrid linear attention，整合 Lightning Attention + MLA，提升长上下文训练/解码效率。
- **后训练-token 效率**：Evolutionary Chain-of-Thought（演化式 CoT）；Linguistic Unit Policy Optimization；bidirectional 等。
- **协同设计**：模型架构 + 优化目标 + serving 系统 + agent 训练环境统一 co-design。
- **目标**：低延迟响应 + 强推理，同时易于训练/serving/部署。
- **同机构相关 2026 H1**：见独立条目蚂蚁 LLaDA 扩散系列工作（LLaDA-o / LLaDA-TTS 等）。

## 原始链接
- url: https://arxiv.org/abs/2606.15079
- pdf_url: https://arxiv.org/pdf/2606.15079
- github_url: https://github.com/inclusionAI

## 本地落盘文件
- ../../../sources/llm/2026/ling-ring-2.6.pdf
