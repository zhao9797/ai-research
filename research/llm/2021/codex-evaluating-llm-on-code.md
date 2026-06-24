---
title: "Evaluating Large Language Models Trained on Code (Codex)"
org: OpenAI
country: US
date: 2021-07
type: paper
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2107.03374
pdf_url: https://arxiv.org/pdf/2107.03374
github_url: https://github.com/openai/human-eval
downloaded: [arxiv-2107.03374.pdf, openai-codex-blog.md, openai-codex-blog.html]
---

## 一句话定位
OpenAI 的 Codex：在 GitHub 代码上微调 GPT 得到的代码生成模型（GitHub Copilot 的底座），并发布 HumanEval 评测集，开创代码 LLM 评测范式。

## 摘要（3-6 句）
Codex 是在 GitHub 公开代码上微调的 GPT 语言模型，研究其 Python 代码生成能力；其生产版本驱动 GitHub Copilot。作者发布了新评测集 HumanEval（用 docstring 合成程序、按功能正确性评测）。单次采样 Codex 解决 28.8% 的问题（GPT-3 为 0%）；重复采样 100 次并选最优可解 70.2%。论文还讨论了代码 LLM 的安全、对齐与经济影响。官方博客（2021-08-10）发布改进版 Codex 并通过 API 私测开放。

## 关键技术细节
- 基座：GPT 系列，在公开 GitHub 代码上微调（fine-tune）。
- 评测集 HumanEval：164 个手写编程问题，pass@k 指标（按功能正确性 functional correctness）。
- 结果：pass@1 = 28.8%（GPT-3 0%，GPT-J 11.4%）；pass@100 重复采样可达 70.2%。
- 训练数据：2020-05 抓取的 5400 万 GitHub 仓库中的 159 GB Python 文件（过滤后）。
- 衍生：Codex-S（在正确实现样本上进一步监督微调）提升 pass@1；驱动 GitHub Copilot 生产版。
- 是"工具使用/编码 agent"链条的早期一手工作，并强调安全/对齐评估。

## 原始链接
- url: https://arxiv.org/abs/2107.03374
- pdf_url: https://arxiv.org/pdf/2107.03374
- blog: https://openai.com/index/openai-codex/
- github_url: https://github.com/openai/human-eval

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2107.03374.pdf
- ../../../sources/llm/2021/openai-codex-blog.md
- ../../../sources/llm/2021/openai-codex-blog.html
