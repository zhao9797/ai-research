---
title: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
org: Google Research (Brain)    country: US    date: 2022-01    type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2201.11903    pdf_url: https://arxiv.org/pdf/2201.11903    github_url:
downloaded: [chain-of-thought.pdf]
---

## 一句话定位
提出思维链（CoT）提示：在 few-shot 示例中加入中间推理步骤，显著激发大模型的复杂推理能力，且推理能力随规模"涌现"。

## 摘要
生成"思维链"——一系列中间推理步骤——能显著提升大模型完成复杂推理的能力。方法极简：在提示中给出若干带推理过程的示例（CoT exemplars）。在三个大模型上的实验表明 CoT 提示能改善算术、常识、符号推理任务，且增益惊人。例如用 8 个 CoT 示例提示 540B 模型即在 GSM8K 数学应用题上达到 SOTA，超过带验证器的微调 GPT-3。

## 关键技术细节
- 方法：few-shot 提示中每个示例从 <input, output> 改为 <input, chain-of-thought, output>。
- 关键发现：CoT 是"涌现"能力——仅在约 100B+ 参数模型上才显著起效，小模型反而可能变差。
- GSM8K（数学应用题）：PaLM 540B + 8-shot CoT 达 56.9%（论文版本），超过此前微调 + 验证器 SOTA。
- 在 SVAMP、ASDiv、AQuA、MAWPS 等算术，CSQA、StrategyQA 等常识，last-letter / coin-flip 符号推理上均有大幅提升。
- 无需微调、无需额外训练，纯提示工程；为后续 ReAct、self-consistency、self-improve 等 agentic/推理范式打下基础。

## 原始链接
- url: https://arxiv.org/abs/2201.11903
- pdf_url: https://arxiv.org/pdf/2201.11903

## 本地落盘文件
- ../../../sources/llm/2022/chain-of-thought.pdf
