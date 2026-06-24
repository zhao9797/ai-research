---
title: "WebWalker: Benchmarking LLMs in Web Traversal"
org: "阿里巴巴 通义实验室 (Alibaba Tongyi Lab / Alibaba-NLP)"
country: China
date: 2025-01
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2501.07572
pdf_url: https://arxiv.org/pdf/2501.07572
github_url: https://github.com/Alibaba-NLP/WebAgent
downloaded: [webwalker-2501.07572.pdf]
---

## 一句话定位
通义提出"网页深度遍历"基准 WebWalkerQA + 多 agent 框架 WebWalker(explore-critic)，考查 LLM 系统性遍历网站子页提取深层信息的能力，是通义 DeepResearch 系列的评测基石。

## 摘要
传统搜索引擎常只检索浅层内容，限制 LLM 处理复杂多层信息。WebWalker 引入 WebWalkerQA 基准评估 LLM 的网页遍历(web traversal)能力——衡量其系统性遍历网站子页以抽取高质量数据的能力。并提出 WebWalker，一个模仿人类网页导航的多 agent 框架，采用 explore-critic 范式(探索者负责浏览，批评者判断信息是否充分/何时停止)。大量实验表明 WebWalkerQA 富有挑战性，且 RAG 结合 WebWalker 通过真实场景中的横向(跨页)与纵向(深入)信息整合表现有效。

## 关键技术细节
- 基准 WebWalkerQA：要求 agent 从网站入口出发，逐层点击进入子页，整合横向+纵向信息回答问题(深层信息检索)。
- 框架 WebWalker：多 agent explore-critic——explore agent 决定导航动作，critic agent 评估当前信息是否足以作答、是否继续探索。
- 结合 RAG：把遍历得到的网页内容供 LLM 推理作答。
- 隶属 Alibaba-NLP/WebAgent(后并入 DeepResearch) 系列；WebWalkerQA 被 WebDancer、WebSailor 等用作训练/评测基准。

## 原始链接
- url: https://arxiv.org/abs/2501.07572
- pdf_url: https://arxiv.org/pdf/2501.07572
- github_url: https://github.com/Alibaba-NLP/WebAgent

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/webwalker-2501.07572.pdf
