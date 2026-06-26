---
title: Megatron-Core — GPU-optimized Library for Training Transformers at Scale
org: NVIDIA
country: US
date: 2023-08
type: github
categories: [AI infra]
url: https://github.com/NVIDIA/Megatron-LM
github_url: https://github.com/NVIDIA/Megatron-LM
downloaded: [megatron-lm-readme.md]
---

## 一句话定位
NVIDIA 把 Megatron-LM 沉淀为可组合库 Megatron Core，提供 GPU 优化的 Transformer building block 与全套并行（TP/PP/DP/EP/CP）+ 混合精度（含 FP8/FP4），是工业级大模型训练框架的底座。

## 摘要（3-6 句）
该仓库含两部分：Megatron-LM（带预配训练脚本的参考样例）与 Megatron Core（可组合的核心库）。Megatron Core 提供高度优化的算子、五维并行（张量 TP、流水 PP、数据 DP、专家 EP、上下文 CP）、混合精度（FP16/BF16/FP8/FP4）、各类模型结构与分布式 checkpoint，供框架开发者搭自定义训练管线。它被 NeMo、Megatron-LM、众多厂商训练栈集成，并提供 Megatron Bridge 做 HF ↔ Megatron checkpoint 互转。是 Megatron 系列从研究代码到产品库的演进形态。

## 关键技术细节
- 五维并行：Tensor / Pipeline（含 interleaved 1F1B）/ Data / Expert（MoE）/ Context 并行可任意组合。
- 混合精度：FP16、BF16、FP8（配 Transformer Engine）、FP4（Blackwell）。
- 优化：fused kernel、激活重计算、序列并行、分布式优化器、分布式/异步 checkpoint。
- 生态：pip 安装 megatron-core；被 NeMo、NeMo-RL、Megatron-Bridge（HF 互转）集成。

## 原始链接
- url: https://github.com/NVIDIA/Megatron-LM
- github_url: https://github.com/NVIDIA/Megatron-LM

## 一手源存档（sources/）
- [megatron-lm-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/megatron-lm-readme.md)
