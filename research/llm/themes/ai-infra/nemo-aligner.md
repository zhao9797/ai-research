---
title: "NeMo-Aligner: Scalable Toolkit for Efficient Model Alignment"
org: NVIDIA
country: US
date: 2024-05
type: paper
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2405.01481
pdf_url: https://arxiv.org/pdf/2405.01481
github_url: https://github.com/NVIDIA/NeMo-Aligner
downloaded: [nemo-aligner-2405.01481.pdf, nemo-aligner-readme.md]
---

## 一句话定位
NVIDIA 基于 NeMo 框架的可扩展对齐工具包，支持 SFT/RM/PPO-RLHF/DPO/SteerLM/SPIN，用 TP/PP/DP 跨数千 GPU 高效训练，并用 TRT-LLM 加速 RLHF 生成。

## 摘要（3-6 句）
NeMo-Aligner 把主流对齐算法（RLHF-PPO、DPO、SteerLM、SPIN、奖励模型训练）整合进 NeMo 框架，利用张量/流水/数据并行支持从小到 70B/340B 规模的对齐，并支持上千 GPU 扩展。RLHF 生成阶段用 TensorRT-LLM 加速 rollout。它用于训练 Nemotron-4-340B Instruct/Reward、Llama3-70B 各对齐变体等。2025-05 起官方建议迁移到 NeMo-RL（基于 Ray + Megatron Core）。是 NVIDIA 一手对齐 infra。

## 关键技术细节
- 支持算法：SFT、Reward Model、RLHF（PPO）、REINFORCE、DPO、SteerLM（属性条件 SFT）、SPIN。
- 并行：基于 NeMo 的 TP/PP/DP，跨数千 GPU；checkpoint 与 NeMo 生态互通。
- RLHF 生成用 TensorRT-LLM 加速（rollout 是 RLHF 吞吐瓶颈）。
- 产出：Nemotron-4-340B Instruct/Reward、Llama-3.1-Nemotron-70B-Instruct（REINFORCE）等；后继 NeMo-RL（Ray + Megatron Core + HF 集成）。

## 原始链接
- url: https://arxiv.org/abs/2405.01481
- pdf_url: https://arxiv.org/pdf/2405.01481
- github_url: https://github.com/NVIDIA/NeMo-Aligner

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/nemo-aligner-2405.01481.pdf
- ../../../../sources/llm/themes/ai-infra/nemo-aligner-readme.md
