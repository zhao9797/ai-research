---
title: "Ring-1T — Every Step Evolves: Scaling Reinforcement Learning for Trillion-Scale Thinking Model"
org: 蚂蚁集团 百灵 / inclusionAI (Ant Group Ling Team)
country: China
date: 2025-10
type: paper
categories: [后训练, AI infra, agentic训练]
url: https://arxiv.org/abs/2510.18855
pdf_url: https://arxiv.org/pdf/2510.18855
github_url: https://github.com/inclusionAI/Ring-V2
downloaded: [ring-1t.pdf]
---

## 一句话定位
蚂蚁 Ring-1T：首个万亿参数开源 thinking（推理）模型，1T 总参 / 约 50B 激活，提出 IcePop / C3PO++ / ASystem 解决万亿级 RL 的训推不一致与系统瓶颈。发布 2025-10-21。

## 摘要
Ring-1T 是首个万亿参数级、开源 SOTA thinking 模型，1T 总参、每 token 激活约 50B。万亿级 RL 训练带来空前挑战：train-inference 不一致、rollout 处理低效、RL 系统瓶颈。论文提出三项相互关联的创新：(1) IcePop——通过 token 级差异 masking 与 clipping 稳定 RL，解决训推不匹配的不稳定；(2) C3PO++——改进资源利用与 rollout 效率；(3) ASystem——高性能 RL 训练系统框架。Ring-1T 在数学/代码/逻辑等推理 benchmark 上达开源 SOTA。

## 关键技术细节
- 规模：1T 总参 / 约 50B 激活 MoE（基于 Ling-1T 基座做 RL）。
- IcePop：token-level discrepancy masking + clipping，消除 train-inference mismatch 引起的 RL 不稳定。
- C3PO++：在 Ring-lite 的 C3PO 基础上升级，提升 rollout 资源利用率。
- ASystem：面向万亿级 thinking 模型的 RL 训练系统（解决 rollout / 同步瓶颈）。
- 成绩：开源万亿级 thinking 模型 SOTA（AIME、代码、逻辑）。
- 开源：GitHub inclusionAI/Ring-V2。

## 原始链接
- url: https://arxiv.org/abs/2510.18855
- pdf_url: https://arxiv.org/pdf/2510.18855
- github_url: https://github.com/inclusionAI/Ring-V2

## 本地落盘文件
- ../../../sources/llm/2025/ring-1t.pdf
