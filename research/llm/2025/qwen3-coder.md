---
title: Qwen3-Coder: Agentic Coding in the World
org: 阿里巴巴 Qwen Team
country: China
date: 2025-07
type: blog
categories: [后训练, agentic训练, AI infra]
url: https://qwenlm.github.io/blog/qwen3-coder/
pdf_url:
github_url: https://github.com/QwenLM/Qwen3-Coder
downloaded: [qwen3-coder-blog.html]
---

## 一句话定位
阿里最强 agentic 代码模型 Qwen3-Coder-480B-A35B（480B MoE/35B 激活），原生 256K（外推 1M）上下文，agentic coding 对标 Claude Sonnet 4。发布 2025-07-22。

## 摘要
官方博客发布 Qwen3-Coder，旗舰为 Qwen3-Coder-480B-A35B-Instruct：4800 亿参数 MoE、激活 350 亿，原生支持 256K 上下文、可外推至 1M。在 Agentic Coding、Agentic Browser-Use、Agentic Tool-Use 上取得开源模型 SOTA，与 Claude Sonnet 4 相当。同步开源命令行工具 Qwen Code（fork 自 Gemini CLI，定制 prompt 与 function calling 协议）。强调通过大规模 agentic RL（在 20K 并行环境中执行真实软件工程任务）训练。

## 关键技术细节
- 架构：Qwen3-Coder-480B-A35B（480B 总参 / 35B 激活，MoE）。
- 上下文：原生 256K，外推至 1M tokens。
- Agentic RL：在 20,000 个并行独立环境上做大规模 code RL，执行真实多轮软件工程任务（Agentic Coding / Browser-Use / Tool-Use）。
- 预训练：约 7.5T tokens（代码占比高），用 Qwen2.5-Coder 清洗/重写低质数据。
- 工具：开源 Qwen Code CLI（fork Gemini CLI），适配 Claude Code / Cline 等。
- 成绩：开源 agentic coding SOTA，对标 Claude Sonnet 4。

## 原始链接
- url: https://qwenlm.github.io/blog/qwen3-coder/
- github_url: https://github.com/QwenLM/Qwen3-Coder

## 本地落盘文件
- ../../../sources/llm/2025/qwen3-coder-blog.html
