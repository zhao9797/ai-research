---
title: "Nemotron-4 340B Technical Report"
org: NVIDIA
country: US
date: 2024-06
type: report
categories: [架构, 后训练]
url: https://arxiv.org/abs/2406.11704
pdf_url: https://arxiv.org/pdf/2406.11704
github_url:
downloaded: [2406.11704.pdf]
---

## 一句话定位
NVIDIA Nemotron-4 340B（Base/Instruct/Reward），定位"合成数据生成引擎"：对齐过程 >98% 数据为合成生成，开源整套合成数据 pipeline；340B 稠密 Transformer，96 层 / hidden 18432 / GQA，9T token、6144 H100、FP8 可单机部署。

## 摘要
发布 Nemotron-4 340B 模型族（Base、Instruct、Reward），采用 NVIDIA Open Model License（允许分发/修改/商用含输出）。模型在多项基准上与开放模型竞争，设计上可在单台 8×H100 DGX 以 FP8 精度部署。对齐过程中 >98% 数据是合成生成的，展示这些模型可用于生成合成数据来训练更小模型；同时开源对齐所用的合成数据生成 pipeline。Nemotron-4-340B-Reward 在发布时居 RewardBench 榜首，超过 GPT-4o-0513 与 Gemini 1.5 Pro-0514。

## 关键技术细节
- 架构：标准 decoder-only Transformer；340B 稠密（非 MoE）；96 层；hidden 18432；96 attention heads + 8 KV heads（GQA）；context 4096；RoPE；SentencePiece tokenizer，词表 256,000；squared ReLU 激活、无 bias、dropout=0、untied input-output embeddings。
- 预训练：9T token（前 8T 为正式预训练 + 末 1T 继续预训练阶段）；数据含单语+平行多语语料、43 种编程语言。
- 算力/并行：768 台 DGX H100 节点（共 6144 张 H100 80GB SXM5，BF16 峰值 989 TFLOP/s·卡）；8-way Tensor Parallelism + 12-way Pipeline Parallelism。
- 部署：可在单台 8×H100 DGX 以 FP8 精度部署。
- 对齐：>98% 合成数据；约 20K 人工标注数据起步（10K SFT + 10K HelpSteer2 偏好）；RLHF + DPO + 一种 Reward-aware Preference Optimization (RPO)。
- Reward 模型：在 Nemotron-4-340B-Base 上替换为回归式 reward head；RewardBench 主榜居首（92.0），各类目如 Chat 95.8、Safety 93.7 等。
- 合成数据 pipeline：开源（生成 prompt → 生成回复 → 用 reward 模型筛选/质量过滤），用于训练更小模型。
- 许可：NVIDIA Open Model License。

## 原始链接
- url: https://arxiv.org/abs/2406.11704
- pdf_url: https://arxiv.org/pdf/2406.11704

## 一手源存档（sources/）
- [2406.11704.pdf](https://arxiv.org/pdf/2406.11704)  （arXiv 原文 PDF，不入 git）
