---
title: "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models"
org: DeepSeek-AI
country: 中国
date: 2024-02
type: arxiv
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2402.03300
pdf_url: https://arxiv.org/pdf/2402.03300
github_url: https://github.com/deepseek-ai/DeepSeek-Math
downloaded: [files/deepseekmath-grpo.pdf]
---

## 一句话定位
首次提出 GRPO（Group Relative Policy Optimization）强化学习算法的论文；7B 数学模型 MATH 51.7%，逼近 Gemini-Ultra / GPT-4。GRPO 后来成为 DeepSeek-R1 的核心。

## 摘要
DeepSeekMath 7B 在 DeepSeek-Coder-Base-v1.5 7B 基础上继续预训练 120B 数学相关 token（来自 Common Crawl 的数据选择流水线 + 自然语言 + 代码）。无外部工具与投票时 MATH 达 51.7%；64 样本 self-consistency 达 60.9%。两大关键：(1) 通过精心设计的数据选择流水线挖掘公开网络数据；(2) 提出 GRPO——PPO 的变体，在提升数学推理的同时优化显存占用（去掉 critic 网络，用组内相对优势估计 baseline）。

## 关键技术细节（带数字）
- 模型：DeepSeekMath 7B（基于 DeepSeek-Coder-Base-v1.5 7B 继续预训练）。
- 数学语料：120B math-related tokens（自建 Common Crawl 数据选择流水线）。
- 性能：MATH 51.7%（无工具、无投票）；self-consistency@64 达 60.9%。
- RL 算法：GRPO（Group Relative Policy Optimization）—— PPO 变体，去 critic、用同一 prompt 的一组采样的相对奖励估 baseline，显著省显存。
- 后续影响：GRPO 成为 DeepSeek-R1 / DeepSeek-V3 RL 阶段核心算法。

## 原始链接
- arXiv: https://arxiv.org/abs/2402.03300
- PDF: https://arxiv.org/pdf/2402.03300
- GitHub: https://github.com/deepseek-ai/DeepSeek-Math

## 本地落盘文件
- ../../../sources/llm/2024/deepseekmath-grpo.pdf
