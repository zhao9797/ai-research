---
title: "Mind2Web: Towards a Generalist Agent for the Web"
org: "The Ohio State University"
country: US
date: 2023-06
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2306.06070
pdf_url: https://arxiv.org/pdf/2306.06070
github_url: https://github.com/OSU-NLP-Group/Mind2Web
downloaded: [mind2web-2306.06070.pdf]
---

## 一句话定位
首个面向"通用网页 agent"的大规模真实数据集：覆盖 137 个真实网站、2000+ 开放式任务，用真实快照训练/评测模型在任意网站上执行复杂多步操作。

## 摘要
Mind2Web 是为开发和评测"能在任意网站上按语言指令完成复杂任务的通用网页 agent"而构建的首个数据集。它收集了来自 137 个真实网站、覆盖 31 个领域的 2,000+ 开放式任务，每个任务带众包标注的动作序列(action sequence)。相比此前用模拟/简化网站、只支持受限动作的数据集，Mind2Web 提供真实网站的复杂多样环境，要求 agent 具备跨网站、跨领域的泛化能力。作者还提出 MindAct——先用小 LM 过滤网页元素(rank candidate elements)，再用大 LM 在候选中多选一地预测动作，以应对真实网页 HTML 过长的问题。

## 关键技术细节
- 规模：137 个真实网站、31 个领域、2,000+ 任务，含真实网页 DOM 快照与人类动作序列标注。
- 三种泛化评测设置：cross-task(同站新任务)、cross-website(新网站)、cross-domain(新领域)。
- MindAct 框架：两阶段——小型微调 LM 做元素排序(从上千 DOM 元素里筛候选)，大 LM(GPT-4 等)在候选集上以多选形式预测下一步动作。
- 意义：把 web agent 研究从玩具环境推向真实网站规模，为 GUI/web agent 训练提供了关键监督数据。

## 原始链接
- url: https://arxiv.org/abs/2306.06070
- pdf_url: https://arxiv.org/pdf/2306.06070
- github_url: https://github.com/OSU-NLP-Group/Mind2Web

## 一手源存档（sources/）
- [mind2web-2306.06070.pdf](https://arxiv.org/pdf/2306.06070)  （arXiv 原文 PDF，不入 git）
