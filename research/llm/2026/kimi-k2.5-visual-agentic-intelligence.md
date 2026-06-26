---
title: "Kimi K2.5: Visual Agentic Intelligence"
org: 月之暗面 Moonshot AI (Kimi Team)
country: China
date: 2026-02
type: paper
categories: [架构, 后训练, agentic训练, 预训练数据]
url: https://arxiv.org/abs/2602.02276
pdf_url: https://arxiv.org/pdf/2602.02276
github_url: https://huggingface.co/moonshotai/Kimi-K2.5
downloaded: [kimi-k2.5.pdf]
---

## 一句话定位
月之暗面 Kimi K2.5，开源多模态 agentic 大模型，主打"文本-视觉联合优化"与 Agent Swarm 自主并行智能体编排框架。

## 摘要
Kimi K2.5（arXiv 2026-02-02，作者 "Kimi Team"）是一款开源多模态 agentic 模型，强调文本与视觉两种模态的联合优化使彼此互相增强。技术组合包括 joint text-vision pre-training、zero-vision SFT、joint text-vision RL。在多模态基座之上引入 Agent Swarm——一个自主并行的智能体编排框架，可动态把复杂任务分解为异构子问题并并发执行，相比单 agent baseline 把延迟降低最多 4.5×。在编码、视觉、推理、agentic 任务上达到 SOTA，开源 post-trained checkpoint。其后继模型 Kimi K2.6（HF createdAt 2026-04-14）为 1T 总参 / 32B 激活 MoE（384 专家、top-8、1 共享专家、64 注意力头），Agent Swarm 扩展到 300 子智能体 / 4000 协同步骤。

## 关键技术细节
- **定位**：开源多模态 agentic 模型；文本+视觉联合优化（两模态互增强）。
- **预训练**：joint text-vision pre-training（文本-视觉联合预训练）。
- **后训练**：zero-vision SFT + joint text-vision reinforcement learning（文本-视觉联合 RL）。
- **agentic-Agent Swarm**：自主并行智能体编排框架，动态把复杂任务分解为异构子问题并发执行；相比单 agent 延迟降低最多 4.5×。
- **评测**：编码 / 视觉 / 推理 / agentic 多域 SOTA（开源模型）。
- **后继 Kimi K2.6（model card，2026-04）**：MoE 1T 总参 / 32B 激活；注意力隐藏维 7168；MoE 每专家隐藏维 2048；64 注意力头；384 专家、top-8、1 shared expert；Agent Swarm 横向扩展到 300 子智能体执行 4000 协同步骤；Tech Blog: kimi.com/blog/kimi-k2-6.html。
- **开源**：HF moonshotai 官方组织发布权重；K2.6 为 Modified MIT 许可。

## 原始链接
- url: https://arxiv.org/abs/2602.02276
- pdf_url: https://arxiv.org/pdf/2602.02276
- model card: https://huggingface.co/moonshotai/Kimi-K2.5 ; https://huggingface.co/moonshotai/Kimi-K2.6

## 一手源存档（sources/）
- kimi-k2.5.pdf  （PDF 不入 git，走 HF bucket）
