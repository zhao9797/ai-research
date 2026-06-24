---
title: Llama-Nemotron - Efficient Reasoning Models
org: NVIDIA
country: US
date: 2025-05
type: technical-report
categories: [架构, 后训练, AI infra]
url: https://arxiv.org/abs/2505.00949
pdf_url: https://arxiv.org/pdf/2505.00949
github_url:
downloaded: [files/llama-nemotron.pdf]
---

## 一句话定位
NVIDIA 2025-05 的 Llama-Nemotron 系列技术报告：从 Llama 3 经神经架构搜索改造的异构推理模型家族（Nano 8B / Super 49B / Ultra 253B），首批支持"推理开关"动态切换的开源模型，性能对标 DeepSeek-R1。

## 摘要
Llama-Nemotron（LN-Nano/Super/Ultra）以 Llama 3 为基，通过神经架构搜索（NAS）加速推理、知识蒸馏、继续预训练，再做以推理为核心的后训练（SFT + 大规模 RL）。它们是首批支持动态 reasoning toggle（在标准聊天与推理模式间切换）的开源模型，性能媲美 DeepSeek-R1 而吞吐与显存效率更优。完整后训练数据集、训练代码（NeMo/NeMo-Aligner/Megatron-LM）均开源。

## 关键技术细节（带数字）
- 三档：LN-Nano 8B、LN-Super 49B、LN-Ultra 253B（基于 Llama-3.1/3.3）。
- 改造流程：从 Llama 3 做 neural architecture search（NAS）加速推理 + 知识蒸馏 + 继续预训练（CPT）。
- 后训练：reasoning-focused SFT + 大规模强化学习（RL）。
- 特性：首批支持动态 reasoning toggle（chat ↔ reasoning）的开源模型。
- 性能：对标 DeepSeek-R1，吞吐与内存效率更优（截至 2025-04 旗舰领先）。
- 开源：完整 post-training 数据集、训练代码库（NeMo、NeMo-Aligner、Megatron-LM）；NVIDIA Open Model License。
- 发布日期：2025-05（arXiv:2505.00949）。

## 原始链接
- arXiv：https://arxiv.org/abs/2505.00949
- PDF：https://arxiv.org/pdf/2505.00949

## 本地落盘文件
- ../../../sources/llm/2025/llama-nemotron.pdf
