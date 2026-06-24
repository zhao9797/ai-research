---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
org: "Princeton University / Google Research (Brain)"
country: US
date: 2022-10
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2210.03629
pdf_url: https://arxiv.org/pdf/2210.03629
github_url: https://github.com/ysymyth/ReAct
downloaded: [react-2210.03629.pdf]
---

## 一句话定位
定义了至今主流的 agent 推理范式：交错生成"思考(Thought)—动作(Action)—观察(Observation)"轨迹，让 LLM 在推理与工具/环境交互之间形成协同闭环。

## 摘要
ReAct 让 LLM 以交错方式生成推理轨迹（reasoning traces）和任务相关动作（actions）：推理帮助模型归纳/跟踪/更新行动计划并处理异常，动作让模型与外部知识库或环境交互获取信息。在问答(HotpotQA)与事实核查(Fever)上，ReAct 通过与简单 Wikipedia API 交互，缓解了 chain-of-thought 中的幻觉与错误传播；在两个交互决策基准(ALFWorld、WebShop)上，仅用 1-2 个 in-context 示例就以绝对成功率 34%(ALFWorld)、10%(WebShop) 超过模仿学习和强化学习方法。

## 关键技术细节
- 核心机制：把语言模型的"思考"和"行动"统一为同一 token 序列里交替出现的片段（Thought / Act / Obs），few-shot 提示即可触发，无需训练。
- 实验基座主要为 PaLM-540B（及 GPT-3 对比）。
- HotpotQA / Fever：动作空间为 search[entity]、lookup[string]、finish[answer]，与 Wikipedia API 交互。
- ALFWorld(文本具身)：ReAct 相对 Act-only 提升约 34 个百分点的绝对成功率；WebShop(网购)提升约 10 个百分点。
- 关键论点：纯推理(CoT)易幻觉，纯行动缺乏高层规划；二者结合可互补、可解释、可纠错（人在回路可编辑思考来纠偏）。
- 项目页：https://react-lm.github.io

## 原始链接
- url: https://arxiv.org/abs/2210.03629
- pdf_url: https://arxiv.org/pdf/2210.03629
- github_url: https://github.com/ysymyth/ReAct

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/react-2210.03629.pdf
