---
title: "Qwen3-Next：迈向更极致的训练推理性价比 (Qwen3-Next-80B-A3B)"
org: Qwen Team, Alibaba Group
country: China
date: 2025-09
type: blog
categories: [架构, AI infra, 后训练]
url: https://qwen.ai/blog?id=4074cca80393150c248e508aa62983f9cb7d27cd&from=research.latest-advancements-list
github_url: https://huggingface.co/collections/Qwen/qwen3-next-68c25fd6838e585db8eeea9d
downloaded: [qwen3-next-blog.html]
---

## 一句话定位
Qwen3-Next-80B-A3B 是 Qwen 的新架构：Gated DeltaNet + Gated Attention 混合（3:1）+ 极致稀疏 MoE（80B 总参仅激活 3B）+ 原生 MTP，训练成本不到 Qwen3-32B 的 1/10、长上下文吞吐 10 倍以上。

## 摘要（3-6 句）
Qwen 认为 Context Length Scaling 与 Total Parameter Scaling 是两大趋势，为此设计了全新 Qwen3-Next 结构：混合注意力、高稀疏度 MoE、训练稳定优化、多 token 预测。Qwen3-Next-80B-A3B-Base 拥有 800 亿参数仅激活 30 亿，性能与 Qwen3-32B dense 相近甚至略好，而训练 GPU 卡时不到其 1/10，32K 以上上下文推理吞吐为其 10 倍以上。基于 Base 发布 Instruct 与 Thinking 版：Instruct 与旗舰 Qwen3-235B-A22B-Instruct-2507 相当且在 256K 长上下文显著占优；Thinking 优于 Qwen3-32B-Thinking 并超过 Gemini-2.5-Flash-Thinking。

## 关键技术细节
- 混合架构：Gated DeltaNet（线性注意力）+ Gated Attention（标准注意力），3:1 混合比例（75% 层 Gated DeltaNet，25% 层标准注意力），优于纯滑窗注意力或纯 Mamba2。
- 极致稀疏 MoE：80B 总参、每次激活约 3B（约 3.7%）；512 总专家 + 10 路由专家 + 1 共享专家（对比 Qwen3 MoE 的 128 总/8 路由）；全局负载均衡。
- 稳定性优化：注意力输出门控（消除 attention sink / 极大激活）；Zero-Centered RMSNorm + 对 norm weight 加 weight decay（替代 Qwen3 的 QK-Norm 异常）；MoE router 初始化归一化。
- 原生 MTP（Multi-Token Prediction）：训练推理一致的多步训练，提高 speculative decoding 接受率并增强主干性能。
- 数据：Qwen3 36T 语料的均匀子集 15T token；GPU 卡时不到 Qwen3-30B-A3B 的 80%，仅为 Qwen3-32B 的 9.3%。
- 推理：4K 上下文 prefill 吞吐约 7×、>32K 上下文 prefill/decode >10×（对比 Qwen3-32B）。
- 发布 2025-09，HuggingFace/ModelScope 官方开源；代码已合入 transformers 主分支。

## 原始链接
- url: https://qwen.ai/blog?id=4074cca80393150c248e508aa62983f9cb7d27cd&from=research.latest-advancements-list
- github_url: https://huggingface.co/collections/Qwen/qwen3-next-68c25fd6838e585db8eeea9d

## 一手源存档（sources/）
- [qwen3-next-blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/architecture/qwen3-next-blog.html)
