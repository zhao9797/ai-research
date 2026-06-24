---
title: "QwQ-32B: Embracing the Power of Reinforcement Learning"
org: Qwen Team, Alibaba
country: China
date: 2025-03
type: blog
categories: [后训练, agentic训练]
url: https://qwenlm.github.io/blog/qwq-32b/
github_url: https://huggingface.co/Qwen/QwQ-32B
downloaded: [qwq-32b-blog.html]
---

## 一句话定位
QwQ-32B 官方博客：用大规模 RL（含可验证奖励 + 多阶段 + agent/工具 RL）让 32B 稠密模型达到与 671B DeepSeek-R1 相当的推理水平，开源权重。

## 摘要（3-6 句）
Qwen 团队发布 QwQ-32B（2025 年 3 月 6 日），探索 RL 在强基座上的可扩展性。仅 320 亿参数的 QwQ-32B 在多项推理基准上达到与 6710 亿参数（370 亿激活）的 DeepSeek-R1 相当的表现，凸显 RL 应用于在海量世界知识上预训练的稳健基座的有效性。训练分阶段：先针对数学/代码做基于结果验证器（answer verifier / 代码执行）的 RL，再做面向通用能力与对齐的第二阶段 RL；并集成了 agent 相关能力——模型能边思考边调用工具、根据环境反馈调整推理。模型以 Apache 2.0 在 Hugging Face / ModelScope 开源。

## 关键技术细节
- 基座：Qwen2.5-32B（稠密，32B）。
- 阶段一 RL（推理）：数学用答案正确性验证器、代码用代码执行服务器（通过测试用例判对错）给奖励，无传统 RM；随训练轮次性能持续上升。
- 阶段二 RL（通用）：用通用奖励模型 + 规则验证器，提升指令遵循、对齐、人类偏好，且不损推理。
- agent 能力：集成工具使用与环境反馈下的推理（think-with-tools）。
- 结果：AIME24、LiveCodeBench、LiveBench、IFEval、BFCL 等与 DeepSeek-R1 相当，远超 o1-mini 与同规模蒸馏模型。
- 开源：QwQ-32B 权重 Apache 2.0（HuggingFace / ModelScope）；官方博客原发于 qwenlm.github.io（后迁 qwen.ai）。

## 原始链接
- url: https://qwenlm.github.io/blog/qwq-32b/
- model: https://huggingface.co/Qwen/QwQ-32B

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/qwq-32b-blog.html
