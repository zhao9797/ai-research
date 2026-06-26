---
title: "CogAgent: A Visual Language Model for GUI Agents"
org: "清华大学 / 智谱 AI (THUDM / Zhipu)"
country: China
date: 2023-12
type: paper
categories: [架构, agentic训练]
url: https://arxiv.org/abs/2312.08914
pdf_url: https://arxiv.org/pdf/2312.08914
github_url: https://github.com/THUDM/CogAgent
downloaded: [cogagent-2312.08914.pdf]
---

## 一句话定位
清华/智谱的 18B 视觉语言模型，专攻 GUI 理解与导航：高低分辨率双编码器支持 1120×1120 输入识别细小元素，仅凭截图就在 Mind2Web/AITW 上超过用 HTML 文本的 LLM 方法。

## 摘要
人们大量时间花在 GUI(电脑/手机屏幕)上。LLM 能帮写邮件，但难理解和操作 GUI，限制了自动化潜力。CogAgent 是一个 180 亿参数的视觉语言模型(VLM)，专精 GUI 理解与导航。通过同时使用低分辨率与高分辨率图像编码器，CogAgent 支持 1120×1120 分辨率输入，能识别细小页面元素和文本。作为通用 VLM，它在 5 个文本密集与 4 个通用 VQA 基准(VQAv2、OK-VQA、Text-VQA、ST-VQA、ChartQA、infoVQA、DocVQA、MM-Vet、POPE)上达 SOTA。仅以截图为输入，CogAgent 在 PC 和 Android GUI 导航任务(Mind2Web、AITW)上超过使用提取 HTML 文本的 LLM 方法，刷新 SOTA。

## 关键技术细节
- 规模：18B 参数 VLM(基于 CogVLM)；后续有 CogAgent-9B-20241220 版本。
- 双编码器：低分辨率 + 高分辨率交叉注意力分支，支持 1120×1120 高清输入，识别小图标/小字。
- 输入：纯截图(无需 HTML/a11y 树)；输出 GUI 动作(点击坐标、输入等)。
- 通用能力：9 个 VQA/多模态基准 SOTA(文本密集 + 通用)。
- GUI 任务：Mind2Web(PC 网页)、AITW(Android) 上超过基于 HTML 文本的 LLM。
- 是智谱 AutoGLM 等 GUI agent 产品的视觉基座之一。

## 原始链接
- url: https://arxiv.org/abs/2312.08914
- pdf_url: https://arxiv.org/pdf/2312.08914
- github_url: https://github.com/THUDM/CogAgent

## 一手源存档（sources/）
- [cogagent-2312.08914.pdf](https://arxiv.org/pdf/2312.08914)  （arXiv 原文 PDF，不入 git）
