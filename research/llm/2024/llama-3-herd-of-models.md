---
title: The Llama 3 Herd of Models
org: Meta
country: US
date: 2024-07
type: paper
categories: [预训练数据, 架构, AI infra, 后训练]
url: https://arxiv.org/abs/2407.21783
pdf_url: https://arxiv.org/pdf/2407.21783
github_url:
downloaded: [2407.21783.pdf]
---

## 一句话定位
Llama 3 全系技术报告（92 页），最大为 405B 稠密 Transformer，128K 上下文，是 2024 年最详尽的开源前沿模型训练手册。

## 摘要
本文介绍 Llama 3 基础模型族，原生支持多语言、编码、推理与工具使用。最大模型为 405B 参数稠密 Transformer，上下文窗口达 128K。报告给出大量实证评测，发现 Llama 3 质量可与 GPT-4 等领先模型相当。公开发布 405B 的预训练与后训练版本及 Llama Guard 3 安全模型。还通过组合式方法把图像、视频、语音能力集成进 Llama 3，在相应任务上有竞争力（这些多模态模型尚未广泛发布）。

## 关键技术细节
- 旗舰：405B 稠密 Transformer（非 MoE）；另有 8B、70B。128K 上下文。
- 预训练：约 15.6T token；知识截止 2023 年末；tokenizer 128K 词表（128,000 BPE + 28,000 额外）。
- 算力：405B 用 3.8×10^25 FLOPs；在最多 16K H100（700W、80GB HBM3）上训练；峰值 >400 TFLOPS/GPU。
- 并行：4D 并行 = TP + PP + CP（context parallel）+ DP（FSDP），BF16。
- 数据配比：约 50% 通用知识、25% 数学与推理、17% 代码、8% 多语言。
- 后训练：多轮 SFT + 拒绝采样 + DPO（用 DPO 而非 PPO 做偏好对齐）；reward model 训练。
- 多模态：用 cross-attention adapter 组合方式接入图像/视频/语音编码器。
- 安全：Llama Guard 3、Prompt Guard、Code Shield。

## 原始链接
- url: https://arxiv.org/abs/2407.21783
- pdf_url: https://arxiv.org/pdf/2407.21783

## 本地落盘文件
- ../../../sources/llm/2024/2407.21783.pdf
