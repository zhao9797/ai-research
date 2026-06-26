---
title: "WebGPT: Browser-assisted question-answering with human feedback"
org: OpenAI
country: US
date: 2021-12
type: paper
categories: [agentic训练, 后训练]
url: https://arxiv.org/abs/2112.09332
pdf_url: https://arxiv.org/pdf/2112.09332
github_url:
downloaded: [arxiv-2112.09332.pdf]
---

## 一句话定位
OpenAI 的 WebGPT：微调 GPT-3 在文本浏览器环境中检索/导航网页来回答长问答，用模仿学习 + 人类反馈训练——工具使用 + agentic 训练的早期一手范例。

## 摘要（3-6 句）
WebGPT 把 GPT-3 微调为能在基于文本的网页浏览环境中搜索与导航的模型，从而回答长式问题。任务被设计成人也能完成，使得可以先用模仿学习（行为克隆）训练，再用人类反馈优化答案质量。模型在浏览时必须收集引用以支撑答案，便于人工核查事实。在 ELI5（Reddit 长问答）数据集上，最佳模型 = 行为克隆 + 针对偏好奖励模型的拒绝采样（rejection sampling）。其答案被人类偏好的比例：56% 优于人类示范者，69% 优于 Reddit 最高赞答案。

## 关键技术细节
- 任务环境：基于文本的浏览器环境，模型可发出 search / 点击链接 / 滚动 / 引用 / 结束等命令（动作空间），是 agent + 工具使用的雏形。
- 训练流程：①行为克隆（behavior cloning，模仿人类演示）→ ②训练奖励模型（预测人类偏好）→ ③对奖励模型做拒绝采样（best-of-n），并探索 RL。
- 强制收集引用（references）以便事实核查（可验证性、对齐导向）。
- 数据集：ELI5（Explain Like I'm Five，Reddit 长问答）。
- 偏好结果：56% > 人类示范者、69% > Reddit 最高赞。
- 是 OpenAI 后续 InstructGPT/RLHF 与 agent/工具使用路线的关键前置工作。

## 原始链接
- url: https://arxiv.org/abs/2112.09332
- pdf_url: https://arxiv.org/pdf/2112.09332

## 一手源存档（sources/）
- [arxiv-2112.09332.pdf](https://arxiv.org/pdf/2112.09332)  （arXiv 原文 PDF，不入 git）
