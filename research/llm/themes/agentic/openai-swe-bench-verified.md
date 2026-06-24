---
title: "Introducing SWE-bench Verified"
org: OpenAI
country: US
date: 2024-08
type: blog
categories: [agentic训练, agentic环境与数据]
url: https://openai.com/index/introducing-swe-bench-verified/
pdf_url:
github_url:
downloaded: [openai-swe-bench-verified.html]
---

## 一句话定位
OpenAI 与 SWE-bench 原作者合作，发布经人工验证的 500 题子集 SWE-bench Verified，修正原基准低估模型能力的问题，成为衡量 coding agent 自主能力的更可靠标尺(纳入 Preparedness 框架)。

## 摘要
2024-08-13，OpenAI 发布 SWE-bench 的人工验证子集 SWE-bench Verified，以更可靠地评估 AI 模型解决真实软件问题的能力。作为 Preparedness 框架的一部分，OpenAI 跟踪/评估/预测模型自主执行软件工程任务的能力(属"模型自主性"风险类别的中等风险关键组件)。测试发现原 SWE-bench 中部分任务难以或无法解决，导致系统性低估模型能力。OpenAI 与 SWE-bench 作者合作，针对三类问题改进：① 单元测试过于特定、甚至与 issue 无关，可能误拒正确解；② 许多样本 issue 描述欠明确(underspecified)，导致问题/解法歧义；③ 开发环境有时难以可靠搭建，导致有效解被误判失败。最终得到一个 500 样本的人审子集。

## 关键技术细节
- 内容：从原 SWE-bench(2294 题，源自 12 个 Python 仓库的真实 issue+PR)中人工筛选出 500 个高质量样本。
- 评测机制(继承自 SWE-bench)：FAIL_TO_PASS(修复后应通过) + PASS_TO_PASS(不应破坏既有功能)单元测试，patch 须两类全过才算 resolved。
- 三大修正：去除过度特定/无关单元测试、剔除描述欠明确的 issue、保证环境可可靠搭建。
- 用途：纳入 OpenAI Preparedness 框架，作为更可靠的自主软件工程能力指标；后被各大模型(GPT/Claude/Gemini/GLM/Kimi 等)普遍采用为标准报告口径。
- 注：博客提及当时 SWE-bench 榜单顶尖 agent 约 20%(full)/43%(Lite)。

## 原始链接
- url: https://openai.com/index/introducing-swe-bench-verified/

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/openai-swe-bench-verified.html
