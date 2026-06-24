---
title: "Qwen2.5-Coder Technical Report"
org: 阿里巴巴 Qwen Team
country: 中国
date: 2024-09
type: arxiv
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2409.12186
pdf_url: https://arxiv.org/pdf/2409.12186
github_url: https://github.com/QwenLM/Qwen2.5-Coder
downloaded: [files/qwen2.5-coder.pdf]
---

## 一句话定位
CodeQwen1.5 的重大升级，基于 Qwen2.5 架构续训 5.5T+ token，六个尺寸（0.5B–32B），32B-Instruct 成为当时最强开源代码模型。

## 摘要
Qwen2.5-Coder 系列含 0.5B/1.5B/3B/7B/14B/32B 六个模型，构建于 Qwen2.5 架构之上，在超过 5.5T token 的语料上继续预训练。通过细致的数据清洗、可扩展的合成数据生成与均衡的数据混合，展现强大的代码生成能力，同时保持通用与数学能力。

## 关键技术细节（带数字）
- 规模：0.5B / 1.5B / 3B / 7B / 14B / 32B 六档。
- 继续预训练：5.5T+ tokens（基于 Qwen2.5 base）。
- 数据：数据清洗 + 可扩展合成数据 + 均衡配比（源代码 / 文本-代码 grounding / 合成）。
- 任务：next-token + Fill-in-the-Middle（FIM）。
- 上下文：支持 128K。
- 性能：Qwen2.5-Coder-32B-Instruct 在 HumanEval/MBPP/多语言代码基准达开源 SOTA，比肩 GPT-4o。

## 原始链接
- arXiv: https://arxiv.org/abs/2409.12186
- PDF: https://arxiv.org/pdf/2409.12186
- GitHub: https://github.com/QwenLM/Qwen2.5-Coder

## 本地落盘文件
- ../../../sources/llm/2024/qwen2.5-coder.pdf
