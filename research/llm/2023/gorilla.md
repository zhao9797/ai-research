---
title: "Gorilla: Large Language Model Connected with Massive APIs"
org: UC Berkeley / Microsoft Research
country: US
date: 2023-05
type: paper
categories: [agentic训练, 后训练]
url: https://arxiv.org/abs/2305.15334
pdf_url: https://arxiv.org/pdf/2305.15334
github_url: https://github.com/ShishirPatil/gorilla
downloaded: [gorilla.pdf]
---

## 一句话定位
Berkeley 的 Gorilla：微调 LLaMA 写 API 调用超 GPT-4，配检索缓解幻觉，工具调用训练+评测(APIBench)代表作。

## 摘要
LLM 用工具/API 的潜力未实现，即便 GPT-4 也难生成准确参数、易幻觉 API 用法。Gorilla 是微调的 LLaMA 模型，写 API 调用超过 GPT-4。结合文档检索器后，可适应测试时文档变化(支持版本更新)，并大幅减少幻觉。提出 APIBench 数据集(含 HuggingFace、TorchHub、TensorHub API)。检索+Gorilla 证明 LLM 能更准确用工具、跟上频繁更新的文档。

## 关键技术细节
- 底座：LLaMA-7B 微调。
- 训练数据：自指令式生成的 (instruction, API call) 对，覆盖 1645 个 API。
- RAG 训练(RAT)：训练时即注入检索到的 API 文档，使模型学会“看文档再调用”，测试时文档更新可即时适应。
- 评测 APIBench：TorchHub 95 / TensorHub 696 / HuggingFace 925 个 API；用 AST 子树匹配判正确性并检测幻觉。
- 结果：API 调用准确率超 GPT-4、ChatGPT、Claude；显著降幻觉。

## 原始链接
- url: https://arxiv.org/abs/2305.15334
- pdf_url: https://arxiv.org/pdf/2305.15334
- github_url: https://github.com/ShishirPatil/gorilla

## 一手源存档（sources/）
- gorilla.pdf  （PDF 不入 git，走 HF bucket）
