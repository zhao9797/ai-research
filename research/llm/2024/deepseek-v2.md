---
title: "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model"
org: DeepSeek-AI
country: 中国
date: 2024-05
type: arxiv
categories: [架构, AI infra, 后训练]
url: https://arxiv.org/abs/2405.04434
pdf_url: https://arxiv.org/pdf/2405.04434
github_url: https://github.com/deepseek-ai/DeepSeek-V2
downloaded: [files/deepseek-v2.pdf]
---

## 一句话定位
DeepSeek 第二代旗舰 MoE 大模型，首次提出 Multi-head Latent Attention (MLA) 把 KV cache 压成低秩潜向量，配合 DeepSeekMoE 实现"经济训练 + 高效推理"。

## 摘要
DeepSeek-V2 是一个 236B 总参、每 token 激活 21B 的 MoE 语言模型，支持 128K 上下文。核心创新为 MLA（低秩 KV 联合压缩，消除推理瓶颈）与 DeepSeekMoE（细粒度专家 + 共享专家隔离）。相比 DeepSeek 67B，训练成本节省 42.5%，KV cache 减少 93.3%，最大生成吞吐提升至 5.76 倍。在 8.1T 高质量多源语料上预训练，再经 SFT + RL 解锁潜力。

## 关键技术细节（带数字）
- 规模：236B 总参，21B 激活/token；上下文 128K。
- 注意力：MLA，低秩 key-value 联合压缩为 latent vector；相比 DeepSeek 67B 把 KV cache 减少 93.3%。
- MoE：DeepSeekMoE 架构，细粒度专家切分 + 共享专家隔离（routed experts + shared experts，Top-K 路由）。
- 训练数据：8.1T tokens 高质量多源语料。
- 效率：训练成本相比 DeepSeek 67B 节省 42.5%；最大生成吞吐 5.76×。
- 后训练：SFT + RL（包含 GRPO 思路）。

## 原始链接
- arXiv: https://arxiv.org/abs/2405.04434
- PDF: https://arxiv.org/pdf/2405.04434
- GitHub: https://github.com/deepseek-ai/DeepSeek-V2

## 本地落盘文件
- ../../../sources/llm/2024/deepseek-v2.pdf
