---
title: "ToolACE: Winning the Points of LLM Function Calling"
org: "华为诺亚方舟实验室 / 香港科技大学 等"
country: China
date: 2024-09
type: paper
categories: [后训练, agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2409.00920
pdf_url: https://arxiv.org/pdf/2409.00920
github_url: https://huggingface.co/Team-ACE
downloaded: [toolace-2409.00920.pdf]
---

## 一句话定位
华为诺亚的函数调用数据合成引擎：用自进化合成 + 多 agent 对话 + 双层校验产出准确、复杂、多样的工具调用数据，让 8B 小模型在 BFCL 上比肩 GPT-4。

## 摘要
函数调用(function calling) 能显著扩展 LLM 能力，但需要高质量训练数据。ToolACE 是一个自动 agentic 流水线，用于生成准确、复杂、多样的工具学习数据。核心三部分：① 自进化合成过程(self-evolution synthesis)——构建覆盖 26,507 种多样 API 的工具池；② 多 agent 自指交互(self-guided dialog generation)——多个 agent 扮演不同角色生成涉及这些 API 的对话，覆盖不同复杂度(单调用、并行、依赖、嵌套等)；③ 双层校验系统(dual-layer verification)——规则校验 + 模型校验确保数据正确。实验显示用 ToolACE 数据训练的 8B 模型在 Berkeley Function-Calling Leaderboard(BFCL) 上达到与 GPT-4 相当的 SOTA 函数调用能力。

## 关键技术细节
- API 池：自进化合成出 26,507 个多样 API(覆盖多领域、多复杂度)。
- 数据生成：多 agent(user/assistant/tool 角色) 自引导对话，覆盖单工具/并行/依赖/嵌套等调用模式。
- 双层校验：规则检查(语法/参数类型) + 模型检查(语义合理性)，保证调用数据准确。
- 训练模型：基于 LLaMA/Qwen 等 8B 基座微调(ToolACE-8B)。
- 结果：BFCL 上 8B 模型对标 GPT-4，超过同规模开源模型。
- 出自华为诺亚方舟实验室。

## 原始链接
- url: https://arxiv.org/abs/2409.00920
- pdf_url: https://arxiv.org/pdf/2409.00920
- github_url: https://huggingface.co/Team-ACE

## 一手源存档（sources/）
- [toolace-2409.00920.pdf](https://arxiv.org/pdf/2409.00920)  （arXiv 原文 PDF，不入 git）
