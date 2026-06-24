---
title: DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model
org: DeepSeek-AI
country: China
date: 2024-05
type: report
categories: [架构, AI infra]
url: https://arxiv.org/abs/2405.04434
pdf_url: https://arxiv.org/pdf/2405.04434
github_url: https://github.com/deepseek-ai/DeepSeek-V2
downloaded: [deepseek-v2-2405.04434.pdf]
---

## 一句话定位
236B 总参 / 21B 激活的 MoE，首次提出 MLA（多头潜在注意力）把 KV cache 压缩 93.3%，并用 DeepSeekMoE 细粒度专家，是 V3 架构的奠基之作。

## 摘要（3-6 句）
DeepSeek-V2 是 236B 总参、每 token 激活 21B 的 MoE 模型，支持 128K 上下文。它提出 MLA：把 KV 联合压缩到一个低维 latent 向量，推理时只缓存 latent，KV cache 减少 93.3%。DeepSeekMoE 用细粒度专家 + 共享专家提升专家专精与效率。相比 DeepSeek 67B dense，V2 训练成本省 42.5%、KV cache 降 93.3%、最大生成吞吐提升 5.76×。在 8.1T token 上预训练并经 SFT/RL。

## 关键技术细节
- 规模：236B 总参 / 21B 激活；MLA + DeepSeekMoE；8.1T token 预训练；128K 上下文。
- MLA：low-rank KV 联合压缩到 latent（带解耦 RoPE），KV cache 减 93.3%，是省显存的关键架构创新。
- DeepSeekMoE：细粒度专家切分 + 共享专家隔离 + device-limited routing + 通信/负载均衡辅助损失。
- 经济性：vs DeepSeek-67B，训练成本 -42.5%、KV cache -93.3%、生成吞吐 +5.76×。

## 原始链接
- url: https://arxiv.org/abs/2405.04434
- pdf_url: https://arxiv.org/pdf/2405.04434
- github_url: https://github.com/deepseek-ai/DeepSeek-V2

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/deepseek-v2-2405.04434.pdf
