---
title: Qwen3-Next：迈向更极致的训练推理性价比 (Qwen3-Next-80B-A3B)
org: 阿里巴巴 Qwen Team
country: China
date: 2025-09
type: blog
categories: [架构, AI infra, 预训练数据, 后训练]
url: https://qwen.ai/blog?id=qwen3-next
pdf_url:
github_url: https://github.com/QwenLM/Qwen3-Next
downloaded: [qwen3-next-blog.html]
---

## 一句话定位
阿里全新架构 Qwen3-Next-80B-A3B：混合注意力（Gated DeltaNet + Gated Attention 3:1）+ 极致稀疏 MoE（512 专家激活 3.7%）+ MTP，训练成本不到 Qwen3-32B 的 1/10，长上下文推理吞吐 10×+。发布 2025-09-11。

## 摘要
官方博客：为提升长上下文与大总参下的训练推理效率，Qwen3-Next 相比 Qwen3 MoE 做四项核心改进——混合注意力机制、高稀疏度 MoE、训练稳定性优化、MTP。基于该结构训练的 Qwen3-Next-80B-A3B-Base（800 亿总参、激活约 30 亿）性能与 Qwen3-32B dense 相近甚至略好，但训练 GPU hours 不到其 1/10，32k+ 上下文推理吞吐 10 倍以上。配套发布 Instruct 与 Thinking 版本，Instruct 表现与旗舰 Qwen3-235B-A22B-Instruct-2507 相当，Thinking 超越 Gemini-2.5-Flash-Thinking。

## 关键技术细节
- 混合架构：Gated DeltaNet（线性注意力）+ Gated Attention，3:1 比例（75% 层 Gated DeltaNet，25% 层标准注意力）。
- 标准注意力增强：输出门控缓解低秩；注意力头维度 128→256；仅对前 25% 位置维度加 RoPE 提升外推。
- 极致稀疏 MoE：80B 总参，激活约 3B（3.7%）；512 总专家 + 10 路由专家 + 1 共享专家（Qwen3 为 128/8）；全局负载均衡。
- 稳定性：Zero-Centered RMSNorm + norm weight 加 weight decay；MoE router 参数初始化归一化。
- MTP：原生 Multi-Token Prediction，提升主干性能 + 高接受率投机解码（训推一致多步训练）。
- 预训练：Qwen3 36T 语料均匀采样子集，仅 15T tokens；GPU 计算仅为 Qwen3-32B 的 9.3%。
- 推理：prefill 4k 上下文近 7×、32k+ 10×+ 吞吐；decode 4k 近 4×、32k+ 10×+；上下文 256K。

## 原始链接
- url: https://qwen.ai/blog?id=qwen3-next
- github_url: https://github.com/QwenLM/Qwen3-Next

## 一手源存档（sources/）
- [qwen3-next-blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/qwen3-next-blog.html)
