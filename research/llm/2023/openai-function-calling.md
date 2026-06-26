---
title: Function calling and other API updates
org: OpenAI
country: US
date: 2023-06
type: blog
categories: [agentic训练]
url: https://openai.com/index/function-calling-and-other-api-updates/
downloaded: [openai-function-calling-blog.md]
---

## 一句话定位
OpenAI 推出 function calling，把工具调用产品化进 API，奠定后续 tool use/agent 生态的工业标准。

## 摘要
OpenAI 官方博客，宣布 Chat Completions API 的 function calling 能力及多项更新。开发者可向 gpt-4-0613、gpt-3.5-turbo-0613 描述函数，模型智能地输出包含调用这些函数所需参数的 JSON 对象，从而可靠地把 GPT 能力与外部工具/API 连接。同时发布 gpt-3.5-turbo-16k(4x 上下文)、更可控的 system message、并大幅降价。

## 关键技术细节
- function calling：模型按开发者提供的函数 schema 输出结构化 JSON 参数(经微调以判断何时调用)。
- 新模型：gpt-4-0613、gpt-3.5-turbo-0613(均支持 function calling)、gpt-3.5-turbo-16k(16k 上下文)。
- 降价：gpt-3.5-turbo 输入 token 降 25%；text-embedding-ada-002 降 75%。
- 用途：把自然语言转 API 调用、从文本抽结构化数据、构建对话式 agent。
- 意义：将“工具使用”从研究(Toolformer/Gorilla)产品化为工业 API 标准，奠定 agent 生态。

## 原始链接
- url: https://openai.com/index/function-calling-and-other-api-updates/

## 一手源存档（sources/）
- [openai-function-calling-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/openai-function-calling-blog.md)
