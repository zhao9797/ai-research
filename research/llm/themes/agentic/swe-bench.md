---
title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
org: "Princeton University / University of Chicago"
country: US
date: 2023-10
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2310.06770
pdf_url: https://arxiv.org/pdf/2310.06770
github_url: https://github.com/princeton-nlp/SWE-bench
downloaded: [swe-bench-2310.06770.pdf]
---

## 一句话定位
软件工程 agent 的奠基性评测：从真实 GitHub issue+PR 抽取 2294 个修复任务，用单元测试做执行级判定，成为衡量 coding agent 能力的事实标准。

## 摘要
SWE-bench 是评估 LLM 解决真实软件工程问题能力的评测框架，含 2,294 个软件工程任务，来自 12 个流行 Python 仓库的真实 GitHub issue 及对应 PR。给定代码库与 issue 描述，模型须编辑代码库以解决问题；解决常需理解并协调跨多个函数/类/文件的改动，与执行环境交互、处理超长上下文、做复杂推理，远超传统代码生成。评测显示当时最先进的闭源/开源模型仅能解决最简单的问题：表现最好的 Claude 2 仅解决 1.96% 的 issue。SWE-bench 上的进步代表迈向更实用、智能、自主的 LM。

## 关键技术细节
- 规模：2,294 个任务，来自 12 个流行 Python 开源仓库的真实 issue+PR。
- 评测方式：执行级——每个样本带 FAIL_TO_PASS(修复后应通过) 与 PASS_TO_PASS(不应破坏既有功能) 单元测试；patch 需通过两类测试才算 resolved；测试不展示给模型。
- 长上下文/跨文件：任务常需跨多个函数、类、文件协调修改。
- 基线：Claude 2 仅 1.96% resolved；论文还微调出 SWE-Llama。
- 衍生：SWE-bench Lite(子集)、SWE-bench Verified(OpenAI 人审子集 500 例)、SWE-bench Multimodal 等，成为 SWE-agent/OpenHands/各大模型对标的核心榜单。

## 原始链接
- url: https://arxiv.org/abs/2310.06770
- pdf_url: https://arxiv.org/pdf/2310.06770
- github_url: https://github.com/princeton-nlp/SWE-bench

## 一手源存档（sources/）
- [swe-bench-2310.06770.pdf](https://arxiv.org/pdf/2310.06770)  （arXiv 原文 PDF，不入 git）
