---
title: Orca 2: Teaching Small Language Models How to Reason
org: Microsoft Research
country: US
date: 2023-11
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2311.11045
pdf_url: https://arxiv.org/pdf/2311.11045
github_url: https://aka.ms/orca-2
downloaded: [orca-2.pdf]
---

## 一句话定位
Orca 2 教小模型“按任务选推理策略”而非单纯模仿，Cautious Reasoning 让 7B/13B 媲美 5-10x 大模型。

## 摘要
Orca 1 从解释轨迹等丰富信号学习，超过常规指令微调模型。Orca 2 继续探索更好训练信号提升小模型推理：反对过度模仿，主张教小模型对不同任务用不同解法策略(可不同于大模型)。教模型多种推理技巧(逐步、recall-then-generate、recall-reason-generate、直接作答等)，并学会为每个任务选最有效策略(Cautious Reasoning)。用 15 个基准(约 100 任务、36K+ 提示)评测，Orca 2 显著超同尺寸模型，在测高级推理的复杂任务零样本上达 5-10x 大模型水平。

## 关键技术细节
- 参数：7B 与 13B（基于 Llama 2）。
- 核心 Cautious Reasoning：训练数据里把“该用哪种解法策略”的元决策也教给模型，并在训练时抹去原始 system prompt(prompt erasing)，迫使模型内化策略选择。
- 教师：GPT-4 生成多策略解答轨迹。
- 评测：15 基准/~100 任务；BBH、GSM8K、AGIEval、MMLU 等零样本接近/超 5-10x 大模型。
- 论点：过度模仿限制小模型潜力，应教其推理过程与策略选择。

## 原始链接
- url: https://arxiv.org/abs/2311.11045
- pdf_url: https://arxiv.org/pdf/2311.11045
- github_url: https://aka.ms/orca-2

## 本地落盘文件
- ../../../sources/llm/2023/orca-2.pdf
