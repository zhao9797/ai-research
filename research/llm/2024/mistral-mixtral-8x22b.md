---
title: "Cheaper, Better, Faster, Stronger (Mixtral 8x22B)"
org: Mistral AI
country: EU
date: 2024-04
type: blog
categories: [架构]
url: https://mistral.ai/news/mixtral-8x22b/
pdf_url:
github_url:
downloaded: [mistral-mixtral-8x22b-blog.md]
---

## 一句话定位
Mixtral 8x22B 发布博客：稀疏 MoE 开源模型，141B 总参数仅激活 39B，64K 上下文，原生函数调用，Apache 2.0。

## 摘要
2024-04-17 发布。Mixtral 8x22B 是 Mistral 当时最新开源模型，为 AI 社区树立性能与效率新标准。它是稀疏 MoE（SMoE）模型，141B 总参数中仅用 39B 激活参数，提供同尺寸下无与伦比的成本效率。原生支持函数调用，配合 la Plateforme 的约束输出模式可大规模开发应用。64K 上下文窗口可从大文档精确召回信息。多语言（英/法/德/西/意）、强数学与编码。以最宽松的 Apache 2.0 许可发布。稀疏激活使其比任何稠密 70B 更快、又比其他开放权重模型更强。

## 关键技术细节
- 架构：稀疏 MoE，8 专家、每 token top-2；141B 总参数 / 39B 激活。
- 上下文：64K token。
- 能力：原生函数调用 + 约束输出（JSON）；强数学（GSM8K/Math）与编码。
- 多语言：英、法、德、西、意。
- 许可：Apache 2.0（base 与 instruct 均开放）。

## 原始链接
- url: https://mistral.ai/news/mixtral-8x22b/

## 一手源存档（sources/）
- [mistral-mixtral-8x22b-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/mistral-mixtral-8x22b-blog.md)
