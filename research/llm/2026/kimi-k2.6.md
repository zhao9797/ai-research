---
title: "Kimi K2.6（月之暗面：原生多模态 agentic，1T MoE，agent swarm）"
org: 月之暗面 Moonshot AI
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://huggingface.co/moonshotai/Kimi-K2.6
github_url: https://github.com/MoonshotAI/Kimi-K2
downloaded: [kimi-k2.6-readme.md, kimi-k2.6-config.json]
---

## 一句话定位
Kimi K2.6 —— 开源原生多模态 agentic 模型，主打 long-horizon coding、coding-driven design、自主执行与 **agent swarm 群体编排**（晚于初版调研，增量补录）；同代另有 K2.7-Code（代码 agent）。

## 摘要
K2.6 是 K2.5 之后的迭代（1T MoE 谱系延续）。强调：把简单 prompt/视觉输入转成生产级界面与轻量全栈工作流；**横向扩展到 300 个 sub-agents、4000 步协同**，动态分解为并行的领域专精子任务，一次自主运行产出文档/网站/表格；可驱动 7×24 常驻后台 agent 自主管日程、跑代码、跨平台编排。

## 关键技术细节
- **架构（config.json，model_type=kimi_k2/k25）**：MoE，**总参 1T / 激活 32B**；attention hidden 7168；**384 专家，每 token 选 8，1 共享专家**，moe_intermediate 2048；64 注意力头；**MLA**（qk_nope 128 + rope 64）；**61 层**；上下文 **256K**。
- **agentic**：原生多模态 + 群体 agent 编排（300 sub-agents / 4000 steps）；coding-driven design 生成结构化布局/交互/动画。
- 许可 modified-MIT。较 K2.5 提升长程编码与自主执行。

## 原始链接
- url: https://huggingface.co/moonshotai/Kimi-K2.6 （另：Kimi-K2.7-Code、Kimi-Linear-48B-A3B）

## 本地落盘文件
- ../../../sources/llm/2026/kimi-k2.6-readme.md
- ../../../sources/llm/2026/kimi-k2.6-config.json
