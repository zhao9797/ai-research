---
title: Nemotron-Cascade 2: Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation
org: NVIDIA    country: US    date: 2026-03    type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2603.19220    pdf_url: https://arxiv.org/pdf/2603.19220    github_url:
downloaded: [arxiv-2603.19220.pdf]
---

## 一句话定位
NVIDIA 2026-03 的 Nemotron-Cascade 2——基于 Nemotron-3-Nano-30B-A3B 的开放 30B MoE（3B 激活）后训练模型，用 Cascade RL + 多域在线策略蒸馏达到接近前沿的数学/代码推理与 agentic 能力，是 DeepSeek-V3.2 之后第二个在 2025 IMO/IOI/ICPC 拿金牌级表现的开放权重模型。

## 摘要
Nemotron-Cascade 2 是一个开放的 30B MoE 模型（3B 激活参数），交付一流推理与强 agentic 能力。尽管尺寸紧凑，其数学与代码推理接近前沿开放模型；它是继 DeepSeek-V3.2-Speciale-671B-A37B 之后第二个在 2025 国际数学奥赛(IMO)、国际信息学奥赛(IOI)、ICPC 全球总决赛达到金牌级表现的开放权重 LLM，以 20× 更少参数展现极高"智能密度"。相比 Nemotron-Cascade 1：在精选数据上 SFT 后，大幅扩展 Cascade RL 覆盖更广的推理与 agentic 域；并在 Cascade RL 全程引入对每个域取最强中间教师模型的多域在线策略蒸馏（multi-domain on-policy distillation），高效恢复基准回退并持续保持性能增益。开源检查点与训练数据集。

## 关键技术细节
- 提交日期：2026-03-19（v2；PDF 标注 2026-03-16）。机构：NVIDIA。第一作者 Zhuolin Yang / Zihan Liu / Yang Chen / Wei Ping 等。
- 基座：Nemotron-3-Nano-30B-A3B-Base（30B 总 / 3B 激活 MoE）。
- 后训练流程：SFT（精选数据）→ 大幅扩展的 Cascade RL（覆盖更广推理 + agentic 域）。
- 关键创新：multi-domain on-policy distillation —— 在 Cascade RL 全程，对每个域取最强中间教师做在线策略蒸馏，恢复回退、保持增益。
- 表现：2025 IMO / IOI / ICPC World Finals 金牌级（开放权重中第二个，前一个为 DeepSeek-V3.2-Speciale-671B-A37B）；以 20× 更少参数达成。
- 开源：Nemotron-Cascade-2-30B-A3B 后训练模型、Nemotron-Cascade-2-SFT-Data、Nemotron-Cascade-2-RL 数据。

## 原始链接
- url: https://arxiv.org/abs/2603.19220
- pdf_url: https://arxiv.org/pdf/2603.19220

## 本地落盘文件
- ../../../sources/llm/2026/arxiv-2603.19220.pdf
