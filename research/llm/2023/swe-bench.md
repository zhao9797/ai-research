---
title: SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
org: Princeton / University of Chicago
country: US
date: 2023-10
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2310.06770
pdf_url: https://arxiv.org/pdf/2310.06770
github_url: https://github.com/princeton-nlp/SWE-bench
downloaded: [swe-bench.pdf]
---

## 一句话定位
SWE-bench：用真实 GitHub issue/PR 评测模型修真实代码库，agentic coding 的事实标准基准。

## 摘要
把真实软件工程作为评测前沿能力的测试床。SWE-bench 含 2294 个软件工程问题，取自 12 个流行 Python 仓库的真实 GitHub issue 及对应 PR。给定代码库与 issue 描述，模型需编辑代码库解决该 issue——常需跨多函数/类/文件协调修改、与执行环境交互、处理超长上下文、复杂推理，远超传统代码生成。评测显示 SOTA 闭源模型与微调的 SWE-Llama 都只能解最简单的：最佳模型 Claude 2 仅解 1.96%。

## 关键技术细节
- 规模：2294 个 task，来自 Django、Flask、scikit-learn、matplotlib 等 12 个 Python 仓库。
- 任务构造：真实 issue + 合并该 issue 的 PR（含代码 patch 与测试），用 PR 引入/修改的单元测试做验证。
- 评测：模型生成 patch，apply 后跑 FAIL_TO_PASS 与 PASS_TO_PASS 测试判定解决与否。
- 难度：需长上下文(整库)、跨文件、与执行环境交互。
- 基线：Claude 2 仅 1.96%、GPT-4 1.74%；SWE-Llama(微调 Code Llama) 亦低。
- 影响：成为 agentic SWE(后续 SWE-agent、Devin 等)的核心评测。

## 原始链接
- url: https://arxiv.org/abs/2310.06770
- pdf_url: https://arxiv.org/pdf/2310.06770
- github_url: https://github.com/princeton-nlp/SWE-bench

## 本地落盘文件
- ../../../sources/llm/2023/swe-bench.pdf
