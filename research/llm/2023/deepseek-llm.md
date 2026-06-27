---
title: "DeepSeek LLM: Scaling Open-Source Language Models with Longtermism"
org: 深度求索（DeepSeek-AI）
country: China
date: 2024-01
type: paper
categories: [预训练数据, 架构, AI infra, 后训练]
url: https://arxiv.org/abs/2401.02954
pdf_url: https://arxiv.org/pdf/2401.02954
github_url: https://github.com/deepseek-ai/DeepSeek-LLM
downloaded: [deepseek-llm.pdf]
---

## 一句话定位
DeepSeek 首个通用大模型（7B/67B）技术报告，系统研究 scaling law 并据此设计超参与数据配比，67B Chat 在中英开放评测超过 GPT-3.5。（2024-01 发布，属 2023 工作的跨年报告。）

## 摘要（3-6 句）
DeepSeek LLM 提供 7B 与 67B 两种开源配置，在 scaling law 指导下设计。预训练数据集起步 2T token（中英为主，持续扩充）。在 SFT + DPO 后，67B Chat 在代码、数学、推理领域超越 LLaMA-2 70B，并在中英开放式评测中优于 GPT-3.5。报告深入讨论了 scaling law 对超参、模型/数据规模分配的指导，以及 SFT/DPO 阶段的数据与方法。

## 关键技术细节
- 规模与数据：7B 与 67B；预训练 2.0T token（中英为主），持续扩充。
- 架构表（Table 2）：7B = 30 层 / d_model 4096 / 32 heads / 32 kv-heads（MHA）/ seq 4096 / LR 4.2e-4；67B = 95 层 / d_model 8192 / 64 heads / 8 kv-heads（GQA）/ seq 4096 / LR 3.2e-4。
- 设计取舍：67B 选择"加深网络层数（95 层）"而非加宽 FFN；SwiGLU（FFN 中间维 8/3·d_model）；RoPE。
- Tokenizer：Byte-level BPE（BBPE），常规 token 10 万 + 15 特殊 token，模型词表设为 102,400。
- Scaling law：用 1.6B 模型 / 100B token 拟合 LR 调度等超参；提出以非 embedding FLOPs/token（M）刻画模型规模，给出 batch/LR 随算力的拟合公式。
- 学习率调度：multi-step learning rate scheduler（非 cosine，便于持续 / 增量训练）。
- 训练精度/infra：bf16 训练；on-the-fly 将 bf16 logits 转 fp32 再算梯度以省显存；融合 LayerNorm、GEMM、Adam 更新等算子。
- 后训练：SFT + DPO（直接偏好优化）；强调对齐后的无害性与中英开放式回答质量。

## 原始链接
- url: https://arxiv.org/abs/2401.02954
- pdf_url: https://arxiv.org/pdf/2401.02954
- github_url: https://github.com/deepseek-ai/DeepSeek-LLM

## 一手源存档（sources/）
- deepseek-llm.pdf  （PDF 不入 git，走 HF bucket）
