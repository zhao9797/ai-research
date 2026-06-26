---
title: "AgentGym: Evolving Large Language Model-based Agents across Diverse Environments"
org: "复旦大学 (Fudan NLP)"
country: China
date: 2024-06
type: paper
categories: [后训练, agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2406.04151
pdf_url: https://arxiv.org/pdf/2406.04151
github_url: https://github.com/WooooDyy/AgentGym
downloaded: [agentgym-2406.04151.pdf]
---

## 一句话定位
复旦提出"通用自进化 agent"的训练框架与平台：14 个环境、多任务交互轨迹数据 AgentTraj + 自进化方法 AgentEvol，让一个 agent 跨多环境探索学习并泛化。

## 摘要
构建能处理多样任务、跨环境自我进化的通用 agent 是 AI 长期目标。现有方法要么让 LLM agent 逐步模仿专家轨迹(需人类监督、难扩展、限制探索)，要么让 agent 在孤立环境探索(得到泛化差的专才)。AgentGym 迈出构建通用、可自进化 LLM agent 的第一步，识别出三要素三位一体：① 供 agent 探索学习的多样环境；② 配备基础 agent 能力与知识的轨迹数据集；③ 有效且可扩展的自进化方法。AgentGym 是一个含 14 个环境、多任务、支持实时交互的框架/平台，并提供扩展指令数据集 AgentTraj，以及 AgentEvol——让 agent 跨环境自我进化的算法。实验显示进化后的 agent 可达甚至超过 SOTA。

## 关键技术细节
- 平台：14 个交互环境(覆盖网页、具身、工具、游戏、编码等)，统一接口，支持并发实时交互。
- 数据：AgentTraj / AgentTraj-L——跨环境的高质量交互轨迹指令数据，用于 SFT 基础 agent(AgentEvol-Base)。
- 自进化算法 AgentEvol：agent 在多环境中探索、用成功轨迹自我训练，跨环境泛化而非过拟合单一任务。
- 结果：自进化 agent 在多个环境达到/超过 SOTA，验证"跨环境自进化"路线。
- 出自复旦 NLP(《The Rise and Potential of LLM-based Agents》综述同团队)。

## 原始链接
- url: https://arxiv.org/abs/2406.04151
- pdf_url: https://arxiv.org/pdf/2406.04151
- github_url: https://github.com/WooooDyy/AgentGym

## 一手源存档（sources/）
- [agentgym-2406.04151.pdf](https://arxiv.org/pdf/2406.04151)  （arXiv 原文 PDF，不入 git）
