---
title: Introducing the next generation of Claude (Claude 3 family)
org: Anthropic
country: US
date: 2024-03
type: blog
categories: [架构, 后训练]
url: https://www.anthropic.com/news/claude-3-family
pdf_url:
github_url:
downloaded: [anthropic-claude-3-family.md]
---

## 一句话定位
Claude 3 系列（Haiku / Sonnet / Opus 三档）发布博客，Opus 在多项基准上超越同期竞品，统一 200K 上下文，原生支持视觉。

## 摘要
2024-03-04 发布。Claude 3 含三个由弱到强的模型：Haiku、Sonnet、Opus。Opus 为最强模型，在 MMLU（本科级知识）、GPQA（研究生级推理）、GSM8K（数学）等基准上领先同期竞品，接近人类的复杂任务理解与流畅度。三档模型初始均提供 200K 上下文窗口（理论可接受 >100 万 token，对部分客户开放）。Claude 3 在长上下文 NIAH 召回上 Opus 超 99%，并显著降低了对无害 prompt 的过度拒绝率。

## 关键技术细节
- 三档模型：Haiku（最快最省）、Sonnet（性价比/企业）、Opus（最强）。
- 上下文：初始 200K，全部模型理论可接受 >1M token（对选定客户开放）。
- 多模态：原生视觉输入（图表、照片、文档），Haiku 可在 3 秒内读完约 10k token 的含图表 arXiv 论文。
- 速度：Sonnet 对多数负载比 Claude 2/2.1 快 2 倍；Opus 速度与 2/2.1 相当但智能更高。
- 长上下文召回：增强版 NIAH（30 组随机 needle/question）Opus 召回 >99%，甚至能识别人为插入的 needle。
- 安全：拒答行为更克制；BBQ 偏见基准较前代更低。
- 可用性：Opus/Sonnet 上线 claude.ai 与 API（159 国 GA），并通过 Amazon Bedrock 与 Google Cloud Vertex AI 提供。

## 原始链接
- url: https://www.anthropic.com/news/claude-3-family
- model card pdf: https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf

## 本地落盘文件
- ../../../sources/llm/2024/anthropic-claude-3-family.md
