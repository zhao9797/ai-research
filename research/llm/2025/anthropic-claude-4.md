---
title: Introducing Claude 4 (Opus 4 & Sonnet 4)
org: Anthropic
country: US
date: 2025-05
type: blog
categories: [后训练, agentic训练]
url: https://www.anthropic.com/news/claude-4
pdf_url:
github_url:
downloaded: [files/anthropic-claude-4-blog.md]
---

## 一句话定位
Anthropic 2025-05-22 发布的 Claude Opus 4 与 Claude Sonnet 4 官方博客，主打编码、长时程 agent 任务与 extended-thinking-with-tools，Opus 4 自称世界最强编码模型。

## 摘要
Claude 4 为 hybrid 模型（近即时回答 + extended thinking 两模式）。Opus 4 面向复杂长时程 agent 工作流（可持续工作数小时、数千步），Sonnet 4 为 3.7 的大幅升级。新增 extended thinking 期间调用工具、并行工具使用、读写本地文件的记忆能力；API 新增 code execution、MCP connector、Files API、最长 1 小时的 prompt 缓存。

## 关键技术细节（带数字）
- 模型：Claude Opus 4 与 Claude Sonnet 4，均为 hybrid（standard + extended thinking）。
- Opus 4 编码：SWE-bench Verified 72.5%，Terminal-bench 43.2%；可持续 agent 工作数小时（Rakuten 验证连续 7 小时开源重构）。
- Sonnet 4 编码：SWE-bench Verified 72.7%。
- 新能力：extended thinking + 工具交替；并行工具调用；访问本地文件时的"记忆"（抽取并保存关键事实）。
- API 新能力：code execution tool、MCP connector、Files API、prompt 缓存最长 1 小时。
- 定价：Opus 4 $15/$75，Sonnet 4 $3/$15（每百万 token 输入/输出）。
- 配套 system card（123 页，见 anthropic-claude-4-system-card.md）。
- 发布日期：2025-05-22。

## 原始链接
- 官方博客：https://www.anthropic.com/news/claude-4
- system card 列表：https://www.anthropic.com/system-cards

## 本地落盘文件
- ../../../sources/llm/2025/anthropic-claude-4-blog.md
