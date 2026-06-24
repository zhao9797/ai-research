---
title: Toolformer: Language Models Can Teach Themselves to Use Tools
org: Meta AI
country: US
date: 2023-02
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2302.04761
pdf_url: https://arxiv.org/pdf/2302.04761
downloaded: [toolformer.pdf]
---

## 一句话定位
Meta 让模型自监督学会调用 API（计算器/搜索/翻译等），是 LLM 工具使用训练的开山论文。

## 摘要
Toolformer 训练模型自行决定调用哪个 API、何时调用、传什么参数、如何把结果并入后续 token 预测。以自监督方式完成，每个 API 仅需少量演示。集成计算器、QA、两个搜索引擎、翻译、日历等工具。在多项下游任务零样本性能大幅提升，常能匹敌更大模型且不损核心语言能力。

## 关键技术细节
- 训练方式（核心）：自监督——让 LM 在文本中插入候选 API 调用，仅保留“能降低后续 token 困惑度”的调用，自动构造训练数据，再在其上微调。
- 工具：calculator、QA 系统、Wikipedia 搜索、Google 搜索、机器翻译、日历。
- 底座：GPT-J 6.7B。
- 数据：每个 API 仅需少量人写演示作种子。
- 结果：零样本下数学/QA/时间问答等大幅超基线，部分匹敌 GPT-3(175B)，且保留语言建模能力。

## 原始链接
- url: https://arxiv.org/abs/2302.04761
- pdf_url: https://arxiv.org/pdf/2302.04761

## 本地落盘文件
- ../../../sources/llm/2023/toolformer.pdf
