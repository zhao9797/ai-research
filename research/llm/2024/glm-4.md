---
title: "ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools"
org: 智谱 AI (Zhipu AI) / 清华大学
country: 中国
date: 2024-06
type: arxiv
categories: [架构, 后训练, 预训练数据, agentic训练]
url: https://arxiv.org/abs/2406.12793
pdf_url: https://arxiv.org/pdf/2406.12793
github_url: https://github.com/THUDM/GLM-4
downloaded: [files/glm-4.pdf]
---

## 一句话定位
智谱 GLM-4 系列技术报告（GLM-4 / GLM-4-Air / GLM-4-9B），整体逼近 GPT-4-Turbo，中文对齐超 GPT-4；GLM-4 All Tools 强调自主调用工具（agentic）。

## 摘要
报告梳理从 GLM-130B 到 GLM-4 的演进，聚焦 GLM-4 语言系列（GLM-4、GLM-4-Air、GLM-4-9B）。GLM-4 在 MMLU/GSM8K/MATH/BBH/GPQA/HumanEval 上接近 GPT-4/GPT-4-Turbo；指令跟随（IFEval）接近 GPT-4-Turbo；长上下文（128K/1M）匹配 GPT-4-Turbo 与 Claude-3；中文对齐（AlignBench）超过 GPT-4。GLM-4 All Tools 进一步对齐为可自主理解用户意图、规划并调用网页浏览器、Python 解释器、文生图等工具完成复杂任务。

## 关键技术细节（带数字）
- 模型：GLM-4（旗舰）、GLM-4-Air、GLM-4-9B（开源）。
- 预训练：约 10T tokens（以中英为主，覆盖 24 种语言）。
- 上下文：128K，并扩展到 1M。
- 后训练：SFT + RLHF（多阶段对齐）；GLM-4 All Tools 做 agent 对齐（自主规划+工具调用）。
- 基准：MMLU/GSM8K/MATH 接近 GPT-4；中文 AlignBench 超 GPT-4；长上下文匹配 GPT-4-Turbo(128K) 与 Claude-3。

## 原始链接
- arXiv: https://arxiv.org/abs/2406.12793
- PDF: https://arxiv.org/pdf/2406.12793
- GitHub: https://github.com/THUDM/GLM-4

## 一手源存档（sources/）
- glm-4.pdf  （PDF 不入 git，走 HF bucket）
