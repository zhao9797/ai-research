---
title: Llama-Nemotron: Efficient Reasoning Models
org: NVIDIA
country: US
date: 2025-05
type: report
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2505.00949
pdf_url: https://arxiv.org/pdf/2505.00949
github_url: https://huggingface.co/collections/nvidia/llama-nemotron
downloaded: [llama-nemotron.pdf]
---

## 一句话定位
NVIDIA Llama-Nemotron：开放的高效推理模型族（Nano/Super/Ultra），用"NAS 压缩 + 大规模推理 SFT 蒸馏 + 大规模 RL"，并支持运行时开关推理（reasoning on/off）。

## 摘要（3-6 句）
Llama-Nemotron 系列（LN-Nano 8B、LN-Super 49B、LN-Ultra 253B）面向企业推理，从 Llama 3 系列出发，结合神经架构搜索（Puzzle NAS）与知识蒸馏做推理加速，再以推理数据 SFT + 大规模 RL 提升推理能力。其中 LN-Ultra 用 GRPO 在科学推理等可验证任务上做大规模 RL，成为当时开放权重中最强的推理模型之一。模型支持动态推理开关——用户可在推理时切换"思考/不思考"模式。权重、训练数据与训练代码（含 NeMo / Megatron-LM 对齐栈）全部开放。

## 关键技术细节
- 模型：LN-Nano 8B / LN-Super 49B / LN-Ultra 253B，均源自 Llama 3.1/3.3。
- 高效化：Puzzle 神经架构搜索（NAS）+ 知识蒸馏 + FFN fusion，优化推理吞吐与显存。
- 五阶段后训练：NAS/蒸馏恢复 → 推理 SFT（用 DeepSeek-R1 等生成的高质量推理数据蒸馏）→ 大规模 RL（GRPO，科学/数学/代码可验证奖励）→ 偏好对齐（RLHF/指令遵循）。
- reasoning toggle：系统提示控制 "detailed thinking on/off"，同一模型可切换长 CoT 与直答。
- 开源：权重 + 后训练数据集 + 训练代码（NVIDIA NeMo / Megatron 对齐栈）。

## 原始链接
- url: https://arxiv.org/abs/2505.00949
- pdf_url: https://arxiv.org/pdf/2505.00949
- models: https://huggingface.co/collections/nvidia/llama-nemotron

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/llama-nemotron.pdf
