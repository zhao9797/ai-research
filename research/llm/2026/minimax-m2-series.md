---
title: "The MiniMax-M2 Series: Mini Activations Unleashing Max Real-World Intelligence"
org: MiniMax (稀宇科技)
country: China
date: 2026-05
type: paper
categories: [架构, AI infra, 后训练, agentic训练, 预训练数据]
url: https://arxiv.org/abs/2605.26494
pdf_url: https://arxiv.org/pdf/2605.26494
github_url: https://huggingface.co/MiniMaxAI
downloaded: [minimax-m2.pdf]
---

## 一句话定位
MiniMax M2 系列 MoE 模型，旗舰 M2 总参 229.9B / 仅 9.8B 激活，主打"mini 激活释放最大真实世界智能"，配套 Forge agent-native RL 系统与可自我演化的 M2.7 checkpoint。

## 摘要
MiniMax-M2 系列（arXiv 2026-05-26，作者 "MiniMax"，207 人）是面向 agentic 部署端到端设计的 MoE 语言模型族，核心理念"mini activations 释放最大真实世界智能"。旗舰 M2 含 229.9B 总参、每 token 仅激活 9.8B。系列建立在三大支柱上：(i) agent 驱动的数据 pipeline，产出大规模可验证轨迹（agentic coding 与 agentic cowork），每条轨迹基于可执行工作区与 artifact 对齐奖励；(ii) Forge——可扩展的 agent-native RL 系统，适配长程 agent 轨迹，配 windowed-FIFO 调度、前缀树合并、推理优化、训练-推理-agent 清晰解耦，支持白盒/黑盒 agent；(iii) 最新 M2.7 checkpoint 迈出自我演化第一步——自主调试训练 run、修改自身 scaffold。从 M2 到 M2.7 把 mini 激活转化为前沿级 agentic coding / deep search 性能。另有姊妹论文 MiniMax Sparse Attention（MSA，arXiv 2026-06-11）。

## 关键技术细节
- **旗舰 M2 规格**：229.9B 总参 / 9.8B 激活/token（MoE）。
- **预训练数据/后训练-数据 pipeline**：agent 驱动数据 pipeline，产出大规模可验证轨迹（agentic coding + agentic cowork），基于可执行 workspace + artifact 对齐奖励。
- **AI infra-Forge**：可扩展 agent-native RL 系统；windowed-FIFO 调度、prefix-tree merging、推理优化、训练/推理/agent 三方解耦；支持白盒与黑盒 agent。
- **agentic 自我演化-M2.7**：最新 checkpoint 自主 debug 训练 run、修改自身 scaffold（自我演化雏形）。
- **性能定位**：mini-activation footprint → 前沿级 agentic coding 与 deep search。
- **姊妹工作 MiniMax Sparse Attention (MSA, arXiv 2606.13392)**：见单独条目（109B 原生多模态模型上验证的 blockwise 稀疏注意力）。

## 原始链接
- url: https://arxiv.org/abs/2605.26494
- pdf_url: https://arxiv.org/pdf/2605.26494

## 本地落盘文件
- ../../../sources/llm/2026/minimax-m2.pdf
