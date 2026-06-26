---
title: Pangu Ultra - Pushing the Limits of Dense Large Language Models on Ascend NPUs
org: 华为 (Huawei) 盘古
country: China
date: 2025-04
type: paper
categories: [架构, AI infra, 预训练数据, 后训练]
url: https://arxiv.org/abs/2504.07866
pdf_url: https://arxiv.org/pdf/2504.07866
github_url:
downloaded: [pangu-ultra.pdf]
---

## 一句话定位
华为 135B / 94 层稠密 Transformer，全程在 8192 张昇腾 NPU 上训练；用 depth-scaled sandwich norm + tiny init 消除深层 loss spike，MFU >50%，超 Llama 405B / Mistral Large 2，对标稀疏的 DeepSeek-R1。arXiv 2504.07866，发布 2025-04-10。

## 摘要
Pangu Ultra 是 135B 参数稠密 Transformer，证明国产昇腾 NPU 能高效训练 >100B 稠密模型。深层模型训练易出现 loss spike，论文归因于梯度波动，提出两项技术：depth-scaled sandwich norm（按深度缩放的三明治归一化，用 1/√L 因子缩放残差层初始化）+ tiny initialization（按宽度与深度缩放权重初始化标准差），二者共同稳住梯度范数、消除 loss spike。在 13.2T 多样高质量 token 上分三阶段预训练（先建知识/语言、再装推理、最后强化主动推理），上下文从 4K 渐扩到 128K；后训练用 SFT 冷启动 + RL 增强推理。

## 关键技术细节
- 架构：135B 稠密 Transformer，整体类 Llama 3；94 层；hidden dimension 12,288；SwiGLU FFN 中间维 28,672；96 query heads + 8 KV heads（GQA）；RoPE。
- 稳定性：depth-scaled sandwich norm（DSSN，替代 pre-LN，c_attn=0.283、c_mlp=0.283 等按深度缩放）+ tiny init；94 层 1.6B proxy 模型验证有效消除 spike。
- 预训练数据：13.2T tokens，三阶段课程；统一词表。
- 上下文：4K → 128K 渐进扩展。
- Infra：8192 张昇腾 NPU；DP + TP + Sequence Parallelism + PP；细粒度调度把 PP bubble ratio 从 30.45% 降到 6.8%；NPU Fusion Attention (NFA) 算子支持长序列；MFU >50%。
- 后训练：SFT 冷启动（精选指令数据）→ RL 强化推理；整体训练稳定。
- 成绩：超 Llama 405B、Mistral Large 2 等稠密模型；与参数更多的稀疏 DeepSeek-R1 竞争（如 MBPP Pass@1 3-shot 72.6）。

## 原始链接
- url: https://arxiv.org/abs/2504.07866
- pdf_url: https://arxiv.org/pdf/2504.07866

## 一手源存档（sources/）
- pangu-ultra.pdf  （PDF 不入 git，走 HF bucket）
