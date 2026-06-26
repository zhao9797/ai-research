---
title: "Introducing Command R+: A Scalable LLM Built for Business"
org: Cohere
country: other
date: 2024-04
type: blog
categories: [后训练, agentic训练]
url: https://cohere.com/blog/command-r-plus-microsoft-azure
pdf_url:
github_url:
downloaded: [cohere-command-r-plus-blog.md]
---

## 一句话定位
Command R+ 发布博客：面向企业、RAG 优化的旗舰模型，128K 上下文、带引用的高级 RAG、多步工具使用（Multi-Step Tool Use）、10 种语言，首发 Microsoft Azure。

## 摘要
2024-04-04 发布。Command R+ 是 RAG 优化的 SOTA 模型，为企业级负载设计，首发 Microsoft Azure。与此前 Command R 一样有 128K token 上下文，主打：带引用以减少幻觉的高级 RAG；支持全球业务的 10 种关键语言多语言覆盖；以及多步工具使用（Multi-Step Tool Use / agent），让模型能组合多个工具完成复杂任务。配合 Cohere 的 Embed 与 Rerank 模型构成端到端 RAG 栈。

## 关键技术细节
- 定位：企业 RAG + 工具使用旗舰（约 104B 参数，按社区/模型卡）。
- 上下文：128K token。
- RAG：检索增强生成 + 内联引用（citation）以降低幻觉、可溯源。
- 工具：Multi-Step Tool Use（agent）—— 规划并按序调用多个工具/API。
- 多语言：10 种关键业务语言（英/法/西/意/德/葡/日/韩/阿/中）。
- 可用性：首发 Azure，随后 Cohere API、Oracle、Amazon Bedrock 等。

## 原始链接
- url: https://cohere.com/blog/command-r-plus-microsoft-azure
- 模型卡/文档: https://docs.cohere.com/docs/command-r-plus

## 一手源存档（sources/）
- [cohere-command-r-plus-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/cohere-command-r-plus-blog.md)
