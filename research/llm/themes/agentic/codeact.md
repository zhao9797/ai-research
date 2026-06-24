---
title: "Executable Code Actions Elicit Better LLM Agents (CodeAct)"
org: "UIUC / Apple / Google 等"
country: US
date: 2024-02
type: paper
categories: [架构, 后训练, agentic训练]
url: https://arxiv.org/abs/2402.01030
pdf_url: https://arxiv.org/pdf/2402.01030
github_url: https://github.com/xingyaoww/code-act
downloaded: [codeact-2402.01030.pdf]
---

## 一句话定位
主张用"可执行 Python 代码"作为 agent 的统一动作空间(CodeAct)，取代 JSON/文本格式调用；并开源指令数据 CodeActInstruct 与 CodeActAgent，深刻影响后续 OpenHands/SWE-agent 等。

## 摘要
LLM agent 通常被提示以预定义格式(JSON 或文本)输出动作，受限于固定动作空间与组合灵活性差。CodeAct 提出用可执行 Python 代码把 agent 动作统一为单一动作空间：配 Python 解释器，CodeAct 可执行代码动作，并在多轮交互中根据新观察动态修订先前动作或发出新动作。在 API-Bank 及新构建基准上对 17 个 LLM 的分析显示，CodeAct 优于常用替代方案(成功率最高高出 20%)。受此鼓舞，作者构造含 7k 多轮交互的指令微调数据 CodeActInstruct，并训练出 CodeActAgent(基于 Llama2 与 Mistral)——集成 Python 解释器，能用现有库执行复杂任务(如模型训练)并自主自我调试，且不损通用能力。

## 关键技术细节
- 核心思想：code-as-action——动作=可执行 Python 代码，天然支持控制流、循环、组合多工具，比 JSON/text 调用更灵活、动作空间更大。
- 多轮交互：执行代码 → 观察(stdout/报错) → 动态改写或新增动作，支持自我调试。
- 数据集 CodeActInstruct：7k 多轮交互轨迹，用于指令微调。
- 模型 CodeActAgent：基于 Llama2、Mistral 微调，配 Python 解释器。
- 实验：17 个 LLM 在 API-Bank 与自建基准上，CodeAct 相对 JSON/text 动作格式成功率最多高 20%。
- 影响：CodeAct 范式被 OpenHands 等开源 agent 框架直接采用为核心执行机制。

## 原始链接
- url: https://arxiv.org/abs/2402.01030
- pdf_url: https://arxiv.org/pdf/2402.01030
- github_url: https://github.com/xingyaoww/code-act

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/codeact-2402.01030.pdf
