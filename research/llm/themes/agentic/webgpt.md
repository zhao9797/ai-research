---
title: "WebGPT: Browser-assisted question-answering with human feedback"
org: OpenAI
country: US
date: 2021-12
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2112.09332
pdf_url: https://arxiv.org/pdf/2112.09332
github_url:
downloaded: [webgpt-2112.09332.pdf]
---

## 一句话定位
agentic 浏览器使用的开山之作：用 RLHF + 模仿学习训练 GPT-3 在一个文本化浏览器环境中检索、引用网页来作长问答，是 ReAct/工具调用范式的史前史。

## 摘要
WebGPT 微调 GPT-3，使其能在一个基于文本的网页浏览环境中回答开放式问题。模型可以发出搜索、点击链接、滚动、引用等命令（动作空间是离散的浏览指令），并在收集到足够证据后给出带引用的长答案。训练分两步：先用人类示范做行为克隆（模仿学习），再用人类对答案的偏好做奖励建模与强化学习（RLHF），并用 rejection sampling（best-of-n）进一步优化。在 ELI5 问题上，WebGPT 的答案被人类评判优于人类示范答案与 Reddit 高赞答案。

## 关键技术细节
- 基座：GPT-3（最大 175B），同时给出 760M、13B、175B 三档对比。
- 环境：把网页交互抽象成文本化命令（Search、Clicked on link、Find in page、Quote、Scroll、Back、End: Answer 等），便于纯文本 LM 操作——这是把"浏览"变成可由语言模型生成的 token 序列的早期思路。
- 训练方法：① 行为克隆（BC）模仿人类示范；② 奖励模型（RM）从人类成对偏好学习；③ 用 RM 做强化学习与 best-of-n rejection sampling。
- 引用机制：答案必须附上从浏览中摘录的引用片段，便于事实核查，缓解幻觉。
- 评测：在 ELI5 上，175B best-of-64 模型的答案 56% 被偏好于人类示范者答案、69% 被偏好于 Reddit 最高赞答案；在 TruthfulQA 上比 GPT-3 更真实且信息量更高。
- 作者团队即后来 InstructGPT/RLHF 核心成员（Nakano, Hilton, Ouyang, Cobbe, Schulman 等）。

## 原始链接
- url: https://arxiv.org/abs/2112.09332
- pdf_url: https://arxiv.org/pdf/2112.09332

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/webgpt-2112.09332.pdf
