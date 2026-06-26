---
title: DeepSeek-R1-0528 Release
org: DeepSeek
country: China
date: 2025-05
type: blog
categories: [后训练, agentic训练]
url: https://api-docs.deepseek.com/news/news250528
pdf_url:
github_url: https://huggingface.co/deepseek-ai/DeepSeek-R1-0528
downloaded: [deepseek-r1-0528.html, deepseek-r1-0528-modelcard.md]
---

## 一句话定位
DeepSeek-R1 的 2025-05-28 小版本升级（0528）：靠"加大算力 + 后训练算法优化"显著加深推理（AIME 2025 从 70% 提升到 87.5%），平均思考 token 从 12K 增到 23K，并新增 JSON 输出与 function calling；同架构 671B MoE / 37B 激活，权重 MIT 开源。

## 摘要
官方发布说明 + HuggingFace 模型卡：R1-0528 是 R1 的 minor 升级，通过增加计算资源并在后训练中引入算法优化机制，大幅提升数学、编程、通用逻辑的推理深度，整体性能逼近 o3 与 Gemini 2.5 Pro。核心机制是"延长思考深度"——AIME 测试集上平均每题用 token 从旧版 12K 增至新版 23K。同时减少幻觉、增强 function calling 与前端/vibe coding 体验。API 用法不变，权重开源于 HuggingFace。还把 R1-0528 的 CoT 蒸馏到 Qwen3-8B-Base 得到 DeepSeek-R1-0528-Qwen3-8B（AIME 2024 上比 Qwen3-8B +10%、追平 Qwen3-235B-thinking）。

## 关键技术细节
- 架构：与 R1 同——671B 总参 MoE / 每 token 激活 37B（基于 DeepSeek-V3-Base）。
- 后训练增强：增加算力 + 后训练算法优化，扩大推理深度；思考 token AIME 上 12K → 23K/题。
- Benchmark（旧 R1 → R1-0528，Pass@1）：AIME 2024 79.8 → 91.4；AIME 2025 70.0 → 87.5；HMMT 2025 41.7 → 79.4；GPQA-Diamond 71.5 → 81.0；LiveCodeBench(2408-2505) 63.5 → 73.3；Tau-Bench 53.5(Airline)/63.9(Retail)。
- 新增能力：JSON 结构化输出、function calling（工具调用），增强 agentic 可用性；减少幻觉。
- 蒸馏版：DeepSeek-R1-0528-Qwen3-8B（用 R1-0528 的 CoT 后训练 Qwen3-8B-Base），开源小模型 AIME24 SOTA。
- 开源：权重 MIT 协议，发布于 huggingface.co/deepseek-ai/DeepSeek-R1-0528。

## 原始链接
- url: https://api-docs.deepseek.com/news/news250528
- github_url: https://huggingface.co/deepseek-ai/DeepSeek-R1-0528

## 一手源存档（sources/）
- [deepseek-r1-0528.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/deepseek-r1-0528.html)
- [deepseek-r1-0528-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/deepseek-r1-0528-modelcard.md)
