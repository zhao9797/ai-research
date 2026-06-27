---
title: "Gorilla: Large Language Model Connected with Massive APIs"
org: "UC Berkeley / Microsoft Research"
country: US
date: 2023-05
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2305.15334
pdf_url: https://arxiv.org/pdf/2305.15334
github_url: https://github.com/ShishirPatil/gorilla
downloaded: [gorilla-2305.15334.pdf]
---

## 一句话定位
微调 LLaMA 专攻 API/函数调用，并用"检索感知训练(retriever-aware training)"应对 API 文档随时间变化，准确度超过 GPT-4 的工具调用、显著减少幻觉 API。

## 摘要
Gorilla 是基于 LLaMA 微调的模型，专门生成正确的 API 调用。作者构建 APIBench（来自 TorchHub、TensorHub、HuggingFace 三大 ML hub 的大量 API），并训练 Gorilla 在给定自然语言指令时生成语义与语法都正确的 API 调用。Gorilla 在 API 调用准确度上超过 GPT-4，同时大幅减少"幻觉"出不存在 API 的问题。关键创新是检索感知训练：训练时把 API 文档检索器纳入，使模型在测试时能适应文档变更（API 版本更新、参数变化），提升对真实世界 API 频繁变动的鲁棒性。

## 关键技术细节
- 基座：LLaMA-7B 微调。
- 数据集 APIBench：覆盖 TorchHub、TensorHub、HuggingFace 三个模型 hub 的 API（自指令式生成指令-API 对）。
- 检索感知训练(retriever-aware training)：训练样本中加入由检索器取回的 API 文档，使模型学会"读文档再调用"，从而适应 API 文档随时间变化。
- 评测两种模式：zero-shot(无检索) 与 retrieval(有检索)，并用 AST 子树匹配评测调用正确性与幻觉率。
- 结果：API 调用准确率超过 GPT-4、ChatGPT、Claude，幻觉 API 显著减少。
- 后续演化为 Gorilla OpenFunctions / Berkeley Function-Calling Leaderboard(BFCL)。

## 原始链接
- url: https://arxiv.org/abs/2305.15334
- pdf_url: https://arxiv.org/pdf/2305.15334
- github_url: https://github.com/ShishirPatil/gorilla

## 一手源存档（sources/）
- [gorilla-2305.15334.pdf](https://arxiv.org/pdf/2305.15334)  （arXiv 原文 PDF，不入 git）
