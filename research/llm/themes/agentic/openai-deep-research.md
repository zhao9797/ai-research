---
title: "Introducing deep research"
org: OpenAI
country: US
date: 2025-02
type: blog
categories: [后训练, agentic训练]
url: https://openai.com/index/introducing-deep-research/
pdf_url: https://cdn.openai.com/deep-research-system-card.pdf
github_url:
downloaded: [openai-introducing-deep-research.html, openai-deep-research-system-card.pdf]
---

## 一句话定位
OpenAI 的 agentic 深度研究能力：由专为网页浏览优化的 o3 早期版本驱动，端到端 RL 训练于真实浏览+Python 任务，自主多步检索/综合并产出带引用的长报告，GAIA 创 SOTA。

## 摘要
2025-02-02，OpenAI 推出 deep research——ChatGPT 中的一项新 agentic 能力，可就复杂任务在互联网上做多步研究。其模型是为网页浏览优化的 OpenAI o3 早期版本：利用推理来搜索、解读、分析海量文本/图像/PDF，并据所见信息随时调整方向；也能读取用户提供的文件，并通过编写执行 Python 代码做数据分析。配套《Deep Research System Card》(2025-02-25) 详述：模型通过对浏览任务的强化学习训练，学会核心浏览能力(搜索、点击、滚动、解读文件)、在沙盒中用 Python 工具(计算/数据分析/绘图)、以及综合大量网站找到具体信息或写出完整报告。在 GAIA(需浏览+推理的真实问答)与 Humanity's Last Exam 等基准上取得当时 SOTA。

## 关键技术细节
- 模型：为网页浏览优化的 OpenAI o3 早期版本。
- 训练：端到端强化学习——在新构建的浏览数据集上训练；任务从"可自动判分(有 ground truth)"到"带评分 rubric 的开放式"，模型回答按结果打分。
- 能力：搜索/点击/滚动/读文件 + 沙盒 Python(计算、数据分析、画图) + 多网站信息综合 → 带引用长报告。
- 基准(博客/系统卡口径)：GAIA SOTA；Humanity's Last Exam 创纪录准确率(随工具/浏览大幅高于无浏览模型)。
- 发布：2025-02-02，先给 Pro 用户；系统卡 2025-02-25。
- 安全：强化个人信息隐私保护、训练模型抵御网上恶意指令(prompt injection) 等。

## 原始链接
- url: https://openai.com/index/introducing-deep-research/
- pdf_url: https://cdn.openai.com/deep-research-system-card.pdf

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/openai-introducing-deep-research.html
- ../../../../sources/llm/themes/agentic/openai-deep-research-system-card.pdf
