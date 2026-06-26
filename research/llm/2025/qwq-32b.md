---
title: "QwQ-32B: Embracing the Power of Reinforcement Learning"
org: 阿里巴巴 Qwen Team
country: China
date: 2025-03
type: blog
categories: [后训练, agentic训练]
url: https://qwenlm.github.io/blog/qwq-32b/
pdf_url:
github_url: https://huggingface.co/Qwen/QwQ-32B
downloaded: [qwq-32b-blog.html]
---

## 一句话定位
仅 32B 参数、靠大规模 RL 达到对标 DeepSeek-R1（671B/37B 激活）推理性能的开源推理模型，集成 agent 能力。发布 2025-03-06。

## 摘要
官方博客介绍 QwQ-32B：320 亿参数模型，通过扩展强化学习（RL）使其推理性能可与 6710 亿参数（激活 370 亿）的 DeepSeek-R1 相媲美，验证了在强基座上 scale RL 的有效性。采用两阶段 RL：先针对数学与编程做基于结果验证器（accuracy verifier / code execution）的 RL，再做通用能力 RL。模型还集成了 agent 相关能力，可在使用工具时进行批判性思考并根据反馈调整推理。Apache 2.0 开源。

## 关键技术细节
- 规模：32B dense（对标 DeepSeek-R1 671B/37B 激活）。
- RL 两阶段：(1) 数学/编程 outcome-based RL（数学答案校验器 + 代码执行服务器验证）；(2) 通用能力 RL（通用 reward model + rule-based verifier）。
- Agent：集成工具调用能力，可在使用工具时批判性思考、按环境反馈调整推理。
- 上下文：131K。
- 开源协议：Apache 2.0（HuggingFace / ModelScope）。

## 原始链接
- url: https://qwenlm.github.io/blog/qwq-32b/
- github_url: https://huggingface.co/Qwen/QwQ-32B

## 一手源存档（sources/）
- [qwq-32b-blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/qwq-32b-blog.html)
