---
title: DeepSeek-V3.1 Release
org: DeepSeek
country: China
date: 2025-08
type: blog
categories: [后训练, agentic训练, 架构]
url: https://api-docs.deepseek.com/news/news250821
pdf_url:
github_url: https://huggingface.co/deepseek-ai/DeepSeek-V3.1
downloaded: [deepseek-v3.1.html]
---

## 一句话定位
DeepSeek 迈向 agent 时代的第一步：首个混合推理（Think / Non-Think 一个模型两种模式）模型，强化工具使用与多步 agent 任务。发布于 2025-08-21。

## 摘要
官方发布说明：V3.1 引入 hybrid inference——同一模型支持思考（Think）与非思考（Non-Think）两种模式，通过 DeepThink 按钮切换。相比 R1-0528，V3.1-Think 用更少时间得到答案；后训练显著提升工具使用与多步 agent 任务能力。后续 2025-09-22 有 V3.1 Update。

## 关键技术细节
- 混合推理：单模型双模式（Think / Non-Think），通过 chat template / 按钮切换，免去 chat 模型与推理模型切换。
- 推理效率：V3.1-Think 比 R1-0528 更快达到答案（更短思考链）。
- Agent 后训练：post-training 强化 tool use 与多步 agentic 任务表现。
- 基座：延续 V3 系列 671B MoE / 37B 激活架构，开源权重于 HuggingFace。

## 原始链接
- url: https://api-docs.deepseek.com/news/news250821
- github_url: https://huggingface.co/deepseek-ai/DeepSeek-V3.1

## 一手源存档（sources/）
- [deepseek-v3.1.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/deepseek-v3.1.html)
