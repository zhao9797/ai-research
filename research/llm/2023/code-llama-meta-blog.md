---
title: "Code Llama: Meta's state-of-the-art LLM for coding"
org: Meta AI
country: US
date: 2023-08
type: blog
categories: [预训练数据, 架构]
url: https://ai.meta.com/blog/code-llama-large-language-model-coding/
downloaded: [code-llama-meta-blog.md]
---

## 一句话定位
Meta 官方 Code Llama 发布博客，面向开发者讲清 7B/13B/34B 三档、填充、Python 专精与许可。

## 摘要
Meta AI 官方发布 Code Llama 的博客。Code Llama 是基于 Llama 2 的代码生成/理解 LLM，免费用于研究与商用。提供 7B/13B/34B 三档(博客初发时)与 base/Python/Instruct 三个变体。7B/13B 支持 fill-in-the-middle 适合 IDE 实时补全；34B 质量最高但更慢。支持长输入上下文(最长 100k token)，可在大代码库上工作。

## 关键技术细节
- 变体：Code Llama(base) / Code Llama-Python(Python 专精) / Code Llama-Instruct(自然语言指令)。
- 规模：7B / 13B / 34B(博客初发)；后续补 70B。
- 填充(infilling)：7B/13B 支持 FIM，用于 IDE 实时代码补全。
- 长上下文：训练 16k，支持最长 100k token 输入。
- 训练：在 500B 代码相关 token 上从 Llama 2 继续训练(Python 版 +100B)。
- 许可：同 Llama 2，研究 + 商用免费。
- 性能：HumanEval/MBPP 开源 SOTA(34B HumanEval 53.7%)。

## 原始链接
- url: https://ai.meta.com/blog/code-llama-large-language-model-coding/

## 一手源存档（sources/）
- [code-llama-meta-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/code-llama-meta-blog.md)
