---
title: "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model"
org: DeepSeek-AI
country: China
date: 2024-05
type: report
categories: [架构, 预训练数据, AI infra, 后训练]
url: https://arxiv.org/abs/2405.04434
pdf_url: https://arxiv.org/pdf/2405.04434
github_url: https://github.com/deepseek-ai/DeepSeek-V2
downloaded: [deepseek-v2.pdf]
---

## 一句话定位
DeepSeek-V2 首次提出 Multi-head Latent Attention (MLA)，用低秩潜向量压缩 KV cache 93.3%，并结合 DeepSeekMoE，实现 236B 总参/21B 激活的高性价比 MoE。

## 摘要（3-6 句）
DeepSeek-V2 是一个 236B 总参数、每 token 激活 21B、支持 128K 上下文的 MoE 模型。核心架构创新是 MLA（把 KV cache 压缩为一个低秩潜向量以保证高效推理）和 DeepSeekMoE（细粒度专家 + 共享专家的稀疏计算）。相比 DeepSeek 67B，训练成本省 42.5%、KV cache 减少 93.3%、最大生成吞吐提升至 5.76 倍。模型在 8.1T tokens 的多源高质量语料上预训练，再做 SFT 和 RL。即便只激活 21B 参数，仍在开源模型中达到顶尖水平。

## 关键技术细节
- 规模：236B 总参 / 21B 激活；128K 上下文；预训练 8.1T tokens。
- MLA（Multi-head Latent Attention）：将 K/V 联合压缩为低秩潜向量 c_KV，推理时只缓存潜向量，KV cache 减少 93.3%；用解耦 RoPE（decoupled RoPE）处理位置，把 RoPE 维度从压缩维度中分离。
- DeepSeekMoE：细粒度专家切分 + 共享专家（shared experts）隔离，提升专家专业化与参数效率。
- 效率：训练成本相比 DeepSeek 67B 降 42.5%；最大生成吞吐 ×5.76。
- 后训练：SFT + RL（采用 GRPO 类强化学习）解锁对话与对齐能力。

## 原始链接
- url: https://arxiv.org/abs/2405.04434
- pdf_url: https://arxiv.org/pdf/2405.04434
- github_url: https://github.com/deepseek-ai/DeepSeek-V2

## 一手源存档（sources/）
- deepseek-v2.pdf  （PDF 不入 git，走 HF bucket）
