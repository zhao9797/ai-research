---
title: Grok 3 Beta — The Age of Reasoning Agents
org: xAI
country: US
date: 2025-02
type: blog
categories: [AI infra, 后训练, agentic训练]
url: https://x.ai/news/grok-3
pdf_url:
github_url:
downloaded: [files/xai-grok-3-blog.md]
---

## 一句话定位
xAI 2025-02-19 发布的 Grok 3 官方博客：在 Colossus 超算（10x 前代算力）上预训练、并用大规模 RL 做推理后训练，推出 Grok 3 (Think) 与 Grok 3 mini (Think) 两款 beta 推理模型。

## 摘要
Grok 3 融合强推理与广博预训练知识，在 Colossus 超算上以 10x 前 SOTA 算力训练。推理能力经大规模 RL 精炼，可思考数秒至数分钟，自我纠错、回溯、探索多方案。Grok 3 (Think) 与 Grok 3 mini (Think) 为 beta 推理模型；Grok 3 在 Chatbot Arena 取得 Elo 1402。

## 关键技术细节（带数字）
- 预训练算力：Colossus 超算，约前代 SOTA 模型 10x 的训练算力。
- 推理后训练：大规模强化学习（RL）精炼思维链，data-efficient；可思考数秒到数分钟，回溯/纠错/简化步骤。
- AIME 2025（cons@64，最高 test-time compute）：Grok 3 (Think) 93.3%。
- GPQA（研究生级专家推理）：84.6%；LiveCodeBench：79.4%。
- Grok 3 mini：AIME 2024 95.8%，LiveCodeBench 80.4%（高性价比 STEM 推理）。
- Chatbot Arena Elo：1402。
- agentic：Grok Agents 结合推理与工具使用（DeepSearch 等）。
- 发布日期：2025-02-19（仍在训练，将随反馈快速迭代）。

## 原始链接
- 官方博客：https://x.ai/news/grok-3

## 一手源存档（sources/）
- [xai-grok-3-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/xai-grok-3-blog.md)
