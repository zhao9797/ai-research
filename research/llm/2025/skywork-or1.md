---
title: Skywork Open Reasoner 1 Technical Report (Skywork-OR1)
org: 昆仑万维 天工 (Kunlun Skywork AI)
country: China
date: 2025-05
type: paper
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2505.22312
pdf_url: https://arxiv.org/pdf/2505.22312
github_url: https://github.com/SkyworkAI/Skywork-OR1
downloaded: [skywork-or1.pdf]
---

## 一句话定位
昆仑天工面向长 CoT 模型的可扩展 RL 实现，基于 DeepSeek-R1-Distill 系列，32B 模型 AIME/LiveCodeBench 平均准确率从 57.8% 提升到 72.8%，超 DeepSeek-R1 与 Qwen3-32B。发布 2025-05-28。

## 摘要
受 DeepSeek-R1 启发，Skywork-OR1 给出针对长链思维（long CoT）模型的高效可扩展 RL 实现。基于 DeepSeek-R1-Distill 模型系列做 RL：32B 模型在 AIME24/AIME25/LiveCodeBench 上平均准确率 57.8%→72.8%（+15.0），7B 模型 43.6%→57.5%（+13.9）。Skywork-OR1-32B 在 AIME24/AIME25 上超越 DeepSeek-R1 与 Qwen3-32B。报告还系统研究了 RL 训练中的 entropy collapse 等问题与缓解方法，并开源训练代码与数据。

## 关键技术细节
- 基座：DeepSeek-R1-Distill-Qwen 7B / 32B。
- RL 方法：可扩展长 CoT RL（GRPO 改进 + 多阶段训练 + 数据过滤）；研究并缓解 entropy collapse。
- 提升：32B 平均 57.8%→72.8%（+15.0），7B 43.6%→57.5%（+13.9）。
- 成绩：OR1-32B 在 AIME24/25 上超 DeepSeek-R1、Qwen3-32B。
- 开源：训练代码、数据、模型权重（GitHub SkyworkAI/Skywork-OR1）。

## 原始链接
- url: https://arxiv.org/abs/2505.22312
- pdf_url: https://arxiv.org/pdf/2505.22312
- github_url: https://github.com/SkyworkAI/Skywork-OR1

## 本地落盘文件
- ../../../sources/llm/2025/skywork-or1.pdf
