---
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
org: "Northeastern University / MIT / Princeton"
country: US
date: 2023-03
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2303.11366
pdf_url: https://arxiv.org/pdf/2303.11366
github_url: https://github.com/noahshinn/reflexion
downloaded: [reflexion-2303.11366.pdf]
---

## 一句话定位
"语言化强化学习"：不更新权重，而是把环境反馈转成自然语言的自我反思存进记忆，下一次试错时读回，从而让 agent 在多次尝试间自我改进。

## 摘要
Reflexion 通过"语言反馈"而非梯度更新来强化语言 agent。agent 在一次任务失败后，把（稀疏的）标量/文本反馈转写成一段自然语言反思（reflective text），存入情景记忆缓冲区；在后续尝试中把这段反思作为上下文，引导更好的决策。该框架兼容多种反馈信号（标量或自由文本）。在决策(ALFWorld)、推理(HotpotQA)、编程(HumanEval)上均显著提升：HumanEval 上达到 91% pass@1，超过当时 GPT-4 的 80%。

## 关键技术细节
- 三角色结构：Actor(产生动作，常基于 ReAct/CoT) + Evaluator(对轨迹打分) + Self-Reflection 模型(把失败转成语言反思)。
- 记忆：短期(本轮轨迹) + 长期(跨轮的反思文本缓冲)。
- 不做参数更新：所有"学习"发生在文本记忆层面，因此轻量、可解释。
- 结果：ALFWorld 决策成功率较强基线提升约 22%；HotpotQA 推理提升约 20%；HumanEval Python 编程 91% pass@1（>GPT-4 80%）。
- 与 RLHF 的关系：用"语言空间的反思"近似强化学习中的策略改进信号。

## 原始链接
- url: https://arxiv.org/abs/2303.11366
- pdf_url: https://arxiv.org/pdf/2303.11366
- github_url: https://github.com/noahshinn/reflexion

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/reflexion-2303.11366.pdf
