---
title: "AgentTuning: Enabling Generalized Agent Abilities for LLMs"
org: "清华大学 / 智谱 AI (THUDM / Zhipu)"
country: China
date: 2023-10
type: paper
categories: [后训练, agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2310.12823
pdf_url: https://arxiv.org/pdf/2310.12823
github_url: https://github.com/THUDM/AgentTuning
downloaded: [agenttuning-2310.12823.pdf]
---

## 一句话定位
清华/智谱提出用轻量 agent 轨迹指令微调 + 通用指令混合训练，让开源 LLM 获得泛化 agent 能力又不损通用能力，产出开源 AgentLM(7/13/70B)。

## 摘要
开源 LLM 在作为 agent 处理复杂真实任务时远逊于 ChatGPT/GPT-4。AgentTuning 提出一个简单通用的方法来增强 LLM 的 agent 能力同时保持其通用能力。作者构造 AgentInstruct——一个含高质量交互轨迹的轻量指令微调数据集，并采用混合指令微调策略，把 AgentInstruct 与通用领域开源指令数据混合训练。用该方法微调 Llama 2 系列得到 AgentLM。评测显示 AgentTuning 使 LLM 获得 agent 能力而不牺牲通用能力，其中 AgentLM-70B 在未见 agent 任务上可比 GPT-3.5-turbo，展现泛化 agent 能力。开源了 AgentInstruct 与 AgentLM-7B/13B/70B。

## 关键技术细节
- 数据集 AgentInstruct：高质量交互轨迹，覆盖多个 agent 任务环境（来自 AgentBench 等场景），用 GPT-4 等构造并过滤。
- 训练策略：混合指令微调(hybrid instruction-tuning)——agent 轨迹数据 + 通用领域开源指令，缓解专精导致的通用能力退化。
- 基座：Llama 2 (7B/13B/70B) → AgentLM。
- 结果：AgentLM-70B 在 held-out(未见) agent 任务上达到 GPT-3.5-turbo 水平，泛化到训练未覆盖的 agent 任务；通用基准(MMLU 等)基本不降。
- 与 AgentBench 同组工作，共同推动"开源可用的 agent LLM"。

## 原始链接
- url: https://arxiv.org/abs/2310.12823
- pdf_url: https://arxiv.org/pdf/2310.12823
- github_url: https://github.com/THUDM/AgentTuning

## 一手源存档（sources/）
- [agenttuning-2310.12823.pdf](https://arxiv.org/pdf/2310.12823)  （arXiv 原文 PDF，不入 git）
