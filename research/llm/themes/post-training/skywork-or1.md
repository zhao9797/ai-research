---
title: Skywork Open Reasoner 1 Technical Report (Skywork-OR1)
org: Skywork AI / Kunlun (昆仑万维)
country: China
date: 2025-05
type: report
categories: [后训练]
url: https://arxiv.org/abs/2505.22312
pdf_url: https://arxiv.org/pdf/2505.22312
github_url: https://github.com/SkyworkAI/Skywork-OR1
downloaded: [skywork-or1.pdf]
---

## 一句话定位
Skywork-OR1：开源的可复现推理 RL 配方，提出 MAGIC（Multi-stAge, multi-Group, ...）式数据筛选与训练，并系统研究"为何 RL 训练会熵坍缩"以及缓解办法。

## 摘要（3-6 句）
Skywork-OR1 是面向数学与代码推理的开源 RL 训练方案，从 DeepSeek-R1-Distill 系列模型出发用大规模 RL 进一步提升。报告完整公开数据准备（难度分层、去重、可验证性过滤）、训练配方（GRPO 类，含多阶段课程、自适应过滤难度合适的样本）、以及对训练动态的深入研究——尤其是策略熵坍缩（entropy collapse）问题及其缓解（如调节 KL/clip、过滤过易过难样本、温度与采样策略）。Skywork-OR1-32B 在 AIME24/25 等达到开源 SOTA 区间，全部模型、数据与代码开源。

## 关键技术细节
- 起点：DeepSeek-R1-Distill-Qwen-7B/32B 等蒸馏模型，再做 RL。
- 算法：GRPO 类组相对优势 RL，去除部分约束以稳训练。
- 数据：可验证（数学有答案、代码有测试）任务，按难度分层、去污染、过滤无信号样本（全对/全错组）。
- 熵坍缩研究：系统分析 RL 中策略熵塌缩导致探索消失，提出通过 KL/裁剪/采样温度/样本过滤等缓解，延长有效训练。
- 结果：Skywork-OR1-32B 在 AIME24/AIME25、LiveCodeBench 等达到开源领先；7B 版亦强。
- 全开源：权重、训练数据、训练代码、技术细节。

## 原始链接
- url: https://arxiv.org/abs/2505.22312
- pdf_url: https://arxiv.org/pdf/2505.22312
- github_url: https://github.com/SkyworkAI/Skywork-OR1

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/skywork-or1.pdf
