---
title: "Intern-S2-Preview（上海 AILab：35B 科学多模态，task scaling）"
org: 上海人工智能实验室 Shanghai AI Lab (InternLM)
country: China
date: 2026-06
type: model-card
categories: [架构, 后训练, 预训练数据, agentic训练]
url: https://huggingface.co/internlm/Intern-S2-Preview-FP8
downloaded: [intern-s2-preview-readme.md, intern-s2-preview-config.json]
---

## 一句话定位
Intern-S2-Preview —— 35B 科学多模态基础模型，提出 **task scaling**（提升科学任务的难度/多样性/覆盖面）：仅 35B 即在多项核心专业科学任务上**比肩万亿级 Intern-S1-Pro**（晚于初版调研、Intern-S1-Pro 已在库，增量补录）。

## 摘要
在参数/数据 scaling 之外探索**任务 scaling**：把数百个专业科学任务从预训练贯通到 RL 的全链训练。从 **Qwen3.5 续训**；强化小分子结构的空间建模 + 实值预测模块，成为**首个兼具材料晶体结构生成与强通用能力的开源模型**；保持通用推理、多模态理解与 agent 能力。RL 用 **shared-weight MTP + KL loss** 降低训练/推理行为失配、提 MTP accept 率与生成速度；并用 **CoT 压缩**在保推理的前提下缩短响应。

## 关键技术细节
- **架构（config.json，model_type=intern_s2_preview / qwen3_5_moe_text）**：hidden 2048；**40 层**；16 注意力头 / 2 KV，head_dim 256；**256 专家，每 token 选 8**，moe_intermediate 512；MTP 1 层；vocab 251392；上下文 256K（262144）；rope 1e7；FP8 权重。
- **方法**：task scaling 全链（pretrain→RL）；shared-weight MTP+KL；CoT 压缩。
- **效率**：35B 在复杂数学等基准上以更短响应超越万亿级 S1-Pro。
- 许可 Apache-2.0。

## 原始链接
- url: https://huggingface.co/internlm/Intern-S2-Preview-FP8

## 本地落盘文件
- ../../../sources/llm/2026/intern-s2-preview-readme.md
- ../../../sources/llm/2026/intern-s2-preview-config.json
