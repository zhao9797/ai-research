---
title: "ToolRL: Reward is All Tool Learning Needs"
org: "UIUC / 亚马逊"
country: US
date: 2025-04
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2504.13958
pdf_url: https://arxiv.org/pdf/2504.13958
github_url: https://github.com/qiancheng0/ToolRL
downloaded: [toolrl-2504.13958.pdf]
---

## 一句话定位
首个系统研究"工具使用 RL 奖励设计"的工作：分析奖励的类型/尺度/粒度/时序动态，给出面向工具选择与调用的原则化奖励 + GRPO 训练，显著超 SFT 与 base。

## 摘要
当前 LLM 多用 SFT 获取工具使用能力，但难泛化到陌生/复杂场景；R1 式 RL 展现了推理与泛化潜力，但工具使用的奖励设计有独特挑战：可能调用多个工具、参数多样，粗粒度奖励(如答案匹配)无法提供有效的细粒度反馈。ToolRL 首次系统研究 RL 范式下工具选择与调用任务的奖励设计：系统探索奖励的类型、尺度、粒度、时序动态；据此提出面向工具使用的原则化奖励，并用 Group Relative Policy Optimization(GRPO) 训练 LLM。多基准评测显示该方法训练鲁棒、可扩展、稳定，较 base 模型提升 17%、较 SFT 模型提升 15%。

## 关键技术细节
- 研究对象：工具选择(选哪个工具)与工具应用(传什么参数)两类任务的 RL 奖励设计。
- 奖励维度：类型(格式正确性 vs 结果正确性)、尺度(scale)、粒度(coarse vs fine，是否对每个参数/每步给反馈)、时序动态(随训练调整)。
- 提出的奖励：结合格式奖励 + 细粒度正确性奖励(工具名匹配、参数匹配等)。
- RL 算法：GRPO(Group Relative Policy Optimization)。
- 结果：较 base +17%，较 SFT +15%；在分布外工具使用上泛化更好。
- 结论：精心的奖励设计是工具学习 RL 的关键("Reward is all tool learning needs")。

## 原始链接
- url: https://arxiv.org/abs/2504.13958
- pdf_url: https://arxiv.org/pdf/2504.13958
- github_url: https://github.com/qiancheng0/ToolRL

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/toolrl-2504.13958.pdf
