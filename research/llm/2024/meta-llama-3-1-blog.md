---
title: Introducing Llama 3.1 - Our most capable models to date (405B)
org: Meta
country: US
date: 2024-07
type: blog
categories: [预训练数据, 架构, AI infra, 后训练]
url: https://ai.meta.com/blog/meta-llama-3-1/
pdf_url:
github_url:
downloaded: [meta-llama-3-1-blog.md]
---

## 一句话定位
Llama 3.1 发布博客：首个前沿级开源模型 405B，连同升级版 8B/70B，扩展到 128K 上下文、8 种语言，并放开"用输出训练其他模型"的许可。

## 摘要
2024-07-23 发布。Llama 3.1 405B 是 Meta 宣称的"世界最大、最强的开放可用基础模型"，在通用知识、可控性、数学、工具使用、多语言翻译上比肩顶级闭源模型。同步升级 8B/70B：多语言、128K 上下文、SOTA 工具使用、更强推理。405B 在超 15T token 上训练，训练栈优化后推到 >16,000 块 H100。为支持大规模生产推理，模型从 16-bit（BF16）量化到 8-bit（FP8），可在单服务器节点运行。新许可允许用 Llama 输出（含 405B）改进其他模型（合成数据生成、蒸馏）。

## 关键技术细节
- 旗舰 405B：稠密 Transformer；405B 在 >15T token 上训练；>16,000 H100 GPU。
- 上下文/语言：8B/70B/405B 均 128K 上下文，支持 8 种语言。
- 推理量化：BF16 → FP8 量化，405B 可在单服务器节点部署。
- 许可变更：允许使用 Llama 输出（含 405B）训练/改进其他模型，开放合成数据生成与蒸馏。
- 用途：用 405B 改进小模型的后训练质量；支持长文摘要、多语言对话 agent、代码助手。
- 配套：详见技术报告 The Llama 3 Herd of Models（arXiv 2407.21783）。

## 原始链接
- url: https://ai.meta.com/blog/meta-llama-3-1/
- paper: https://ai.meta.com/research/publications/the-llama-3-herd-of-models/

## 一手源存档（sources/）
- [meta-llama-3-1-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/meta-llama-3-1-blog.md)
