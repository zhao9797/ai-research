---
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
org: Northeastern / MIT / Princeton
country: US
date: 2023-03
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2303.11366
pdf_url: https://arxiv.org/pdf/2303.11366
github_url: https://github.com/noahshinn/reflexion
downloaded: [reflexion.pdf]
---

## 一句话定位
Reflexion 用“语言反思”而非梯度更新来强化智能体，HumanEval 91% 超 GPT-4，无训练的 agent 自改进范式。

## 摘要
LLM 越来越多作目标驱动 agent 与环境交互，但用传统 RL 学 trial-and-error 需大量样本与昂贵微调。Reflexion 不更新权重，而通过语言反馈强化 agent：agent 对任务反馈口头反思，把反思文本存入 episodic memory，以改进后续 trial 的决策。可吸收多种(标量/自由文本)、多源(外部/内部模拟)反馈，在序贯决策、编码、语言推理上显著超基线。如 HumanEval pass@1 达 91%，超此前 SOTA GPT-4 的 80%。

## 关键技术细节
- 范式：verbal reinforcement——不做参数更新，用自然语言反思作“梯度”。
- 组件：Actor(LLM 生成动作) + Evaluator(打分) + Self-Reflection(生成反思) + episodic memory(存反思)。
- 反馈类型：标量或自由文本；来源可为外部环境或内部自评。
- 任务：AlfWorld 决策、HotPotQA 推理、HumanEval 编码。
- 结果：HumanEval pass@1 91%（超 GPT-4 80%）；多任务显著提升。

## 原始链接
- url: https://arxiv.org/abs/2303.11366
- pdf_url: https://arxiv.org/pdf/2303.11366
- github_url: https://github.com/noahshinn/reflexion

## 本地落盘文件
- ../../../sources/llm/2023/reflexion.pdf
