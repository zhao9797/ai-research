---
title: "CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis"
org: Salesforce Research
country: US
date: 2022-03
type: paper
categories: [预训练数据, 后训练]
url: https://arxiv.org/abs/2203.13474
pdf_url: https://arxiv.org/pdf/2203.13474
github_url: https://github.com/salesforce/CodeGen
downloaded: [codegen.pdf]
---

## 一句话定位
Salesforce 开源的最高 16.1B 代码大模型 CodeGen，提出多轮程序合成范式，并开源训练库 JAXFORMER。

## 摘要
程序合成旨在根据问题规范（输入输出示例或自然语言描述）生成程序。大模型推进了程序合成 SOTA，但有限的训练资源与数据阻碍开放访问。为民主化，训练并发布一族最高 16.1B 参数的大模型 CODEGEN（在自然语言与编程语言数据上），并开源训练库 JAXFORMER。展示其在 HumanEval zero-shot Python 代码生成上与此前 SOTA 竞争。进一步研究多步（multi-turn）程序合成范式——把单个程序分解为多个指定子问题的提示。

## 关键技术细节
- 规模：350M / 2.7B / 6.1B / 16.1B；decoder-only 自回归。
- 三阶段数据：先自然语言（the Pile）→ 多语言代码（BigQuery）→ 单语言 Python（BigPython），渐进式预训练。
- 多轮合成：提出 Multi-Turn Programming Benchmark（MTPB），把复杂程序拆成多轮自然语言-代码交互。
- 结果：HumanEval zero-shot pass@k 与 Codex 竞争；多轮显著优于单轮。
- 开源：权重 + JAXFORMER 训练库，是开源代码 LLM 的早期代表（与 InCoder、SantaCoder 并列）。

## 原始链接
- url: https://arxiv.org/abs/2203.13474
- pdf_url: https://arxiv.org/pdf/2203.13474
- github_url: https://github.com/salesforce/CodeGen

## 一手源存档（sources/）
- codegen.pdf  （PDF 不入 git，走 HF bucket）
