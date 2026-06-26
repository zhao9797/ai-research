---
title: Qwen3 Technical Report
org: 阿里巴巴 Qwen Team
country: China
date: 2025-05
type: paper
categories: [架构, 预训练数据, 后训练, agentic训练]
url: https://arxiv.org/abs/2505.09388
pdf_url: https://arxiv.org/pdf/2505.09388
github_url: https://github.com/QwenLM/Qwen3
downloaded: [qwen3.pdf, qwen3-blog.html]
---

## 一句话定位
阿里 Qwen3 系列（0.6B–235B，dense + MoE），首创 thinking/non-thinking 统一框架 + thinking budget，旗舰 Qwen3-235B-A22B，全系 Apache 2.0。博客 2025-04-29，论文 2025-05-14。

## 摘要
Qwen3 是 Qwen 家族最新一代，含 dense 与 MoE 两类架构，参数 0.6B–235B。核心创新是把 thinking mode（复杂多步推理）与 non-thinking mode（快速响应）统一到一个模型，可按 query/chat template 动态切换，并引入 thinking budget 机制让用户在推理时自适应分配算力（平衡延迟与性能）。通过从旗舰模型蒸馏知识大幅降低小模型训练成本。多语言从 Qwen2.5 的 29 种扩展到 119 种语言/方言。全系 Apache 2.0 开源。

## 关键技术细节
- 模型矩阵：MoE—Qwen3-235B-A22B（235B 总参/22B 激活，94 层，64/4 Q/KV heads，128 专家选 8），Qwen3-30B-A3B（30B/3B 激活，48 层，128 专家选 8）；Dense—32B/14B/8B/4B/1.7B/0.6B。
- 预训练数据：约 36T tokens，119 种语言/方言（Qwen2.5 为 18T tokens / 29 种语言）。
- 统一双模式：thinking / non-thinking 一体化，免去 chat 模型与推理模型切换。
- Thinking budget：推理时按任务复杂度自适应分配思考 token 预算。
- 后训练：四阶段——long-CoT 冷启动 → reasoning RL → thinking mode 融合 → general RL；并用 strong-to-weak 蒸馏把旗舰能力传给小模型。
- 上下文：dense 大模型与 MoE 支持 128K；小模型 32K。
- 开源协议：Apache 2.0。

## 原始链接
- url: https://arxiv.org/abs/2505.09388
- pdf_url: https://arxiv.org/pdf/2505.09388
- blog: https://qwenlm.github.io/blog/qwen3/
- github_url: https://github.com/QwenLM/Qwen3

## 一手源存档（sources/）
- qwen3.pdf  （PDF 不入 git，走 HF bucket）
- [qwen3-blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/qwen3-blog.html)
