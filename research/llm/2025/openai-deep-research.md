---
title: Introducing deep research (OpenAI)
org: OpenAI
country: US
date: 2025-02
type: blog
categories: [agentic训练, 后训练]
url: https://openai.com/index/introducing-deep-research/
pdf_url:
github_url:
downloaded: [files/openai-deep-research-blog.md]
---

## 一句话定位
OpenAI 2025-02-02 推出的 ChatGPT agentic 能力"deep research"官方博客，基于 o3 专门为多步网页研究后训练，可自主浏览、推理并综合产出带引用的长报告。

## 摘要
Deep research 是 ChatGPT 中的 agent：给定 prompt 后，自主进行数百次网页检索/浏览、推理与综合，5–30 分钟产出带引用的研究报告。底层为针对 web 浏览与 Python 工具使用做强化学习后训练的 o3 专用版本。在 Humanity's Last Exam 上取得当时新高，验证 agentic 浏览+推理范式。

## 关键技术细节（带数字）
- 底层模型：o3 的专用版本，针对 web 浏览与数据分析做 RL 后训练（端到端强化学习训练真实浏览/工具使用任务）。
- Humanity's Last Exam：26.6%（pass@1），显著高于前代（GPT-4o 3.3%、o1 9.1%、o3-mini 13.0% 等同口径）。
- GAIA（外部基准）：开放式 web 浏览/工具任务上达 SOTA。
- 工作方式：自主多步浏览、解读文本/图像/PDF、Python 分析、产出带引用与思考摘要的报告，耗时 5–30 分钟。
- 发布日期：2025-02-02。

## 原始链接
- 官方博客：https://openai.com/index/introducing-deep-research/

## 一手源存档（sources/）
- [openai-deep-research-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/openai-deep-research-blog.md)
