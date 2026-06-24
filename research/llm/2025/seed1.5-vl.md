---
title: Seed1.5-VL Technical Report
org: 字节跳动 Seed (ByteDance Seed)
country: China
date: 2025-05
type: paper
categories: [架构, 后训练, agentic训练]
url: https://arxiv.org/abs/2505.07062
pdf_url: https://arxiv.org/pdf/2505.07062
github_url: https://github.com/ByteDance-Seed/Seed1.5-VL
downloaded: [seed1.5-vl.pdf]
---

## 一句话定位
字节 Seed 视觉语言基座：532M 视觉编码器 + 20B 激活 MoE LLM，60 个公开 benchmark 上 38 个 SOTA，GUI 控制/游戏等 agent 任务超 OpenAI CUA 与 Claude 3.7。发布 2025-05-11。

## 摘要
Seed1.5-VL 是面向通用多模态理解与推理的视觉语言基座，由 532M 视觉编码器与 20B 激活参数的 MoE LLM 组成。尽管架构相对紧凑，在大量公开 VLM benchmark 与内部评测上表现强劲：60 个公开 benchmark 中 38 个达 SOTA。在 GUI 控制、游戏等 agent 任务上超越 OpenAI CUA、Claude 3.7 等领先多模态系统。报告涵盖架构、数据与训练（含 RL）。

## 关键技术细节
- 架构：532M 视觉编码器 + MoE LLM（20B 激活参数）。
- 评测：60 个公开 benchmark，38 项 SOTA。
- Agentic：GUI 控制、游戏等 agent-centric 任务超 OpenAI CUA / Claude 3.7。
- 训练：大规模多模态预训练 + 后训练（含 RL）。
- 开源：GitHub ByteDance-Seed/Seed1.5-VL。

## 原始链接
- url: https://arxiv.org/abs/2505.07062
- pdf_url: https://arxiv.org/pdf/2505.07062
- github_url: https://github.com/ByteDance-Seed/Seed1.5-VL

## 本地落盘文件
- ../../../sources/llm/2025/seed1.5-vl.pdf
