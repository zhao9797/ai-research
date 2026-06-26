---
title: "The Llama 3 Herd of Models"
org: Meta AI
country: US
date: 2024-07
type: report
categories: [架构, 预训练数据, AI infra, 后训练]
url: https://arxiv.org/abs/2407.21783
pdf_url: https://arxiv.org/pdf/2407.21783
github_url: https://github.com/meta-llama/llama3
downloaded: [llama3.pdf]
---

## 一句话定位
Llama 3 是 Meta 的 dense Transformer 模型族，旗舰 405B/128K 上下文，用 15T+ token 预训练，详尽公开数据、infra、并行与后训练配方，是最透明的前沿级开源报告之一。

## 摘要（3-6 句）
Llama 3 原生支持多语言、代码、推理与工具使用。最大模型是 405B 参数的 dense Transformer，上下文窗口达 128K。论文给出大量实证评测，发现 Llama 3 在众多任务上与 GPT-4 等领先模型质量相当。Meta 公开发布预训练与后训练版的 405B 模型及 Llama Guard 3 安全模型。报告还展示了通过组合式（compositional）方法把图像、视频、语音能力集成进 Llama 3 的实验。

## 关键技术细节
- 架构：标准 dense Transformer + GQA + RoPE + SwiGLU + RMSNorm；8B/70B/405B；128K 上下文（分阶段扩展）。
- 预训练：超过 15T 多语言 token；tokenizer 词表 128K。
- infra：405B 用最多 16K H100 训练；4D 并行（TP + PP + CP/上下文并行 + DP/FSDP）；BF16；详述故障率与训练稳定性工程。
- 数据：大规模数据清洗/去重/质量与领域配比、退火（annealing）阶段提升数学/代码。
- 后训练：多轮 SFT + 拒绝采样 + DPO（用 DPO 而非 PPO 做偏好优化）。
- 多模态：组合式接入视觉/视频/语音 adapter（实验性）。

## 原始链接
- url: https://arxiv.org/abs/2407.21783
- pdf_url: https://arxiv.org/pdf/2407.21783
- github_url: https://github.com/meta-llama/llama3

## 一手源存档（sources/）
- llama3.pdf  （PDF 不入 git，走 HF bucket）
