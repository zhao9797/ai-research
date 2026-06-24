---
title: ToolRL: Reward is All Tool Learning Needs
org: University of Illinois Urbana-Champaign
country: US
date: 2025-04
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2504.13958
pdf_url: https://arxiv.org/pdf/2504.13958
github_url: https://github.com/qiancheng0/ToolRL
downloaded: [toolrl.pdf]
---

## 一句话定位
ToolRL：首个系统研究"工具使用 RL 的奖励设计"的工作，提出面向工具选择与调用的细粒度奖励 + GRPO 训练，显著超过 SFT 的工具泛化能力。

## 摘要（3-6 句）
SFT 习得的工具使用难以泛化到陌生/复杂场景，而 R1 式 RL 展现出更好的推理与泛化。但工具使用的奖励设计有独特挑战：可能调用多个工具、参数各异，"答案匹配"这类粗粒度奖励无法提供有效细粒度反馈。ToolRL 首次全面研究工具任务的奖励设计，系统分析奖励的类型、尺度、粒度与时间动态，提出一套有原则的工具使用奖励，并用 GRPO 训练。在多个基准上，该方法比 base 模型提升 17%、比 SFT 提升 15%，训练稳健可扩展，全部代码开源。

## 关键技术细节
- 问题：工具使用奖励需兼顾工具是否选对、参数是否正确、调用结构是否合法等多维度，粗粒度答案匹配不够。
- 奖励设计：分解为格式奖励（结构/可解析）+ 正确性奖励（工具名匹配、参数匹配等细粒度），系统消融奖励 scale/granularity/temporal dynamics。
- 算法：GRPO（组相对优势，无 critic）。
- 结果：相对 base +17%、相对 SFT +15%；在域外工具场景泛化更好，训练稳定。
- 意义：把"R1 式可验证奖励 RL"扩展到 agentic 工具调用，强调奖励工程是关键。

## 原始链接
- url: https://arxiv.org/abs/2504.13958
- pdf_url: https://arxiv.org/pdf/2504.13958
- github_url: https://github.com/qiancheng0/ToolRL

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/toolrl.pdf
