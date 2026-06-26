---
title: Introducing Meta Llama 3 (8B & 70B)
org: Meta
country: US
date: 2024-04
type: blog
categories: [预训练数据, 架构, AI infra, 后训练]
url: https://ai.meta.com/blog/meta-llama-3/
pdf_url:
github_url:
downloaded: [meta-llama-3-blog.md]
---

## 一句话定位
Llama 3 首发博客（8B/70B），标准 decoder-only Transformer 大改进 + 15T token 预训练，公开了 Meta 24K GPU 集群训练栈细节。

## 摘要
2024-04-18 发布 8B 与 70B（预训练 + 指令微调）。架构为相对标准的 decoder-only Transformer，相比 Llama 2 引入 128K 词表 tokenizer 与全尺寸 GQA，序列长度 8192 并用 mask 防止跨文档注意力。预训练数据超 15T token（全公开来源，是 Llama 2 的 7 倍、代码量 4 倍，>5% 为覆盖 30+ 语言的非英文数据）。Meta 观察到即便远超 Chinchilla-optimal，8B/70B 在训到 15T token 仍 log-linear 提升。训练用 DP+MP+PP 三重并行，在 16K GPU 上达 >400 TFLOPS/GPU，跑在两个自建 24K GPU 集群上，有效训练时间 >95%。

## 关键技术细节
- 架构：decoder-only Transformer；128K 词表 tokenizer；8B 与 70B 均用 GQA；序列长 8192 + 文档边界 mask。
- 预训练数据：>15T token（全公开），是 Llama 2 的 7×，代码 4×，>5% 非英文覆盖 30+ 语言。
- scaling 观察：8B 训到 15T（约为 Chinchilla-optimal 200B 的 75 倍）仍持续提升。
- 后训练：SFT + 拒绝采样 + PPO + DPO；显著降低误拒率，提升对齐、推理、代码、指令遵循。
- infra：DP+MP+PP 三重并行；16K GPU 同时训练 >400 TFLOPS/GPU；两个自建 24K GPU 集群；自动错误检测/容错训练栈，有效训练时间 >95%，整体效率较 Llama 2 提升约 3×。
- 安全：Llama Guard 2、Code Shield、CyberSec Eval 2。

## 原始链接
- url: https://ai.meta.com/blog/meta-llama-3/

## 一手源存档（sources/）
- [meta-llama-3-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/meta-llama-3-blog.md)
