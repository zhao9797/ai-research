---
title: "Hunyuan-Large: An Open-Source MoE Model with 52 Billion Activated Parameters by Tencent"
org: 腾讯混元 (Tencent Hunyuan)
country: 中国
date: 2024-11
type: arxiv
categories: [架构, 预训练数据, AI infra, 后训练]
url: https://arxiv.org/abs/2411.02265
pdf_url: https://arxiv.org/pdf/2411.02265
github_url: https://github.com/Tencent/Tencent-Hunyuan-Large
downloaded: [files/hunyuan-large.pdf]
---

## 一句话定位
腾讯混元开源最大 MoE（389B 总参 / 52B 激活），核心实践是大规模合成数据（约 1.5T）+ KV cache 压缩（GQA+CLA）+ 专家专属学习率，比肩 Llama-3.1-405B。

## 摘要
Hunyuan-Large 是当时最大的开源 Transformer MoE，389B 总参、52B 激活，支持 256K 上下文。在语言理解生成、逻辑推理、数学、代码、长上下文等基准上超越 Llama3.1-70B，比肩更大的 Llama3.1-405B。关键实践：远超以往文献规模的大规模合成数据、混合专家路由策略、KV cache 压缩技术、专家专属学习率策略；并系统研究 MoE scaling law 与学习率调度。

## 关键技术细节（带数字）
- 规模：389B 总参 / 52B 激活；64 层；上下文 256K。
- MoE：每 token 激活 1 个 shared expert + 1 个 specialized expert（recycle routing 回收路由策略）。
- KV cache 压缩：GQA（Grouped-Query Attention）+ CLA（Cross-Layer Attention）。
- 训练数据：7T tokens，其中约 1.5T 为高质量多样合成数据。
- 训练技巧：专家专属学习率（不同 shared/specialized 专家用不同 LR）；研究 MoE scaling law。
- 后训练：SFT + RLHF（DPO/在线 RL）。
- 性能：超 Llama3.1-70B，比肩 Llama3.1-405B。

## 原始链接
- arXiv: https://arxiv.org/abs/2411.02265
- PDF: https://arxiv.org/pdf/2411.02265
- GitHub: https://github.com/Tencent/Tencent-Hunyuan-Large

## 本地落盘文件
- ../../../sources/llm/2024/hunyuan-large.pdf
