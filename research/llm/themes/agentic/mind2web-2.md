---
title: "Mind2Web 2: Evaluating Agentic Search with Agent-as-a-Judge"
org: "The Ohio State University / 等"
country: US
date: 2025-06
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2506.21506
pdf_url: https://arxiv.org/pdf/2506.21506
github_url: https://github.com/OSU-NLP-Group/Mind2Web-2
downloaded: [mind2web2-2506.21506.pdf]
---

## 一句话定位
面向 Deep Research 时代的 agentic 搜索评测：130 个长程、需实时浏览与信息综合的真实任务，提出 Agent-as-a-Judge 来评判带引用、随时间变化的复杂答案。

## 摘要
agentic 搜索(如 Deep Research 系统——agent 自主浏览网页、综合信息、返回带引用的完整答案)代表用户与网络规模信息交互方式的重大转变。但其日益增长的复杂性与开放性已超出现有评测基准与方法(后者多假设短检索时程与静态答案)。Mind2Web 2 引入含 130 个真实、高质量、长程任务的基准，需实时网页浏览与大量信息综合，构建耗费 1000+ 小时人力。为应对评测时变且复杂答案的难题，提出一种新颖的 Agent-as-a-Judge 框架——用一个具备引用核查能力的判定 agent 自动评估答案的正确性与引用归属，可靠衡量带引用的长答案。

## 关键技术细节
- 任务：130 个长程 agentic 搜索任务，需实时浏览 + 多源信息综合 + 带引用作答；构建用了 1000+ 小时人力标注。
- 评测创新 Agent-as-a-Judge：用判定 agent(而非简单字符串匹配)来核验答案正确性与引用归属(citation attribution)，应对答案随时间变化、形式开放的难点。
- 与 Mind2Web(2023) 的关系：从"单网站执行动作"升级为"跨网站深度研究与综合"评测，对齐 OpenAI/Google deep research 等系统。
- 出自 OSU NLP(Mind2Web 原班团队)。

## 原始链接
- url: https://arxiv.org/abs/2506.21506
- pdf_url: https://arxiv.org/pdf/2506.21506
- github_url: https://github.com/OSU-NLP-Group/Mind2Web-2

## 一手源存档（sources/）
- [mind2web2-2506.21506.pdf](https://arxiv.org/pdf/2506.21506)  （arXiv 原文 PDF，不入 git）
