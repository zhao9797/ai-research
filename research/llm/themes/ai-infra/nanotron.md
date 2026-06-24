---
title: nanotron — Minimalistic Large Language Model 3D-parallelism Training
org: Hugging Face
country: US
date: 2023-09
type: github
categories: [AI infra]
url: https://github.com/huggingface/nanotron
github_url: https://github.com/huggingface/nanotron
downloaded: [nanotron-readme.md]
---

## 一句话定位
Hugging Face 开源的极简 3D 并行预训练库，用易读代码实现 TP/PP/DP（含 ZeRO-1）+ FP8/序列并行，用于 SmolLM、FineWeb 等 HF 自训项目。

## 摘要（3-6 句）
nanotron 是 HF 面向研究者的轻量大模型预训练框架，目标是用尽量少且可读的代码实现 3D 并行（张量、流水、数据并行）与各种训练优化（ZeRO-1、序列并行、FP8、激活重计算、专家并行）。相对 Megatron-LM 更易改写与实验。它是 HF SmolLM 系列、FineWeb 数据消融、Ultrascale Playbook 等工作的训练代码基础，是社区学习分布式训练的优质参考实现。

## 关键技术细节
- 3D 并行：Tensor Parallel + Pipeline Parallel（1F1B/interleaved）+ Data Parallel（ZeRO-1 优化器分片）。
- 优化：序列并行、激活重计算、FP8（配合 TE）、专家并行（MoE）、分布式 checkpoint。
- 设计：minimalistic、可读、易 hack，定位研究/教学与 HF 内部预训练。
- 用于 SmolLM/SmolLM2、FineWeb 消融、HF "Ultrascale Playbook"。

## 原始链接
- url: https://github.com/huggingface/nanotron
- github_url: https://github.com/huggingface/nanotron

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/nanotron-readme.md
