---
title: Claude 3.7 Sonnet and Claude Code
org: Anthropic
country: US
date: 2025-02
type: blog
categories: [后训练, agentic训练]
url: https://www.anthropic.com/news/claude-3-7-sonnet
pdf_url:
github_url:
downloaded: [files/anthropic-claude-3-7-sonnet-blog.md]
---

## 一句话定位
Anthropic 2025-02-24 发布的 Claude 3.7 Sonnet 官方博客，号称市场首个"hybrid reasoning"模型——同一模型既能近即时回答又能 extended thinking，且 API 可精细控制思考预算；同时推出 agentic 编码工具 Claude Code。

## 摘要
Claude 3.7 Sonnet 把推理作为模型内生能力（而非独立模型），用户可选普通模式或可见的 extended thinking 模式，API 可设思考 token 预算。post-training 刻意少优化竞赛数学，更偏向真实业务任务。同时发布 Claude Code（终端 agentic 编码工具，研究预览）。在 SWE-bench Verified 与 TAU-bench 上达 SOTA。

## 关键技术细节（带数字）
- hybrid reasoning：同一模型，standard 与 extended thinking 两模式；extended thinking 可见思维链。
- 思考预算：API 可设 thinking 上限 N tokens，最高至输出上限 128K tokens（速度/成本与质量权衡）。
- post-training 取向：减少对数学/CS 竞赛的优化，转向真实业务任务。
- benchmark：SWE-bench Verified、TAU-bench 上当时 SOTA（agentic 工具+用户交互任务）。
- 定价：$3 / $15 每百万 token（输入/输出，含 thinking token），与前代一致。
- 同步发布 Claude Code（终端 agentic 编码 CLI，研究预览）。
- 发布日期：2025-02-24。

## 原始链接
- 官方博客：https://www.anthropic.com/news/claude-3-7-sonnet
- 相关：https://www.anthropic.com/research/visible-extended-thinking

## 本地落盘文件
- ../../../sources/llm/2025/anthropic-claude-3-7-sonnet-blog.md
