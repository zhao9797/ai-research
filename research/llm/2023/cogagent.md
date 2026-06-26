---
title: "CogAgent: A Visual Language Model for GUI Agents"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua）
country: China
date: 2023-12
type: paper
categories: [架构, agentic训练]
url: https://arxiv.org/abs/2312.08914
pdf_url: https://arxiv.org/pdf/2312.08914
github_url: https://github.com/THUDM/CogVLM
downloaded: [cogagent.pdf]
---

## 一句话定位
智谱/清华 CogAgent：18B 视觉语言模型专攻 GUI 理解与操作，用高低分辨率双编码器看清 1120×1120 屏幕细节，是中国 GUI agent 一手论文。

## 摘要（3-6 句）
人们大量时间花在图形界面（GUI）上，但 ChatGPT 等 LLM 难以理解与操作 GUI。CogAgent 是一个 180 亿参数、专注 GUI 理解与导航的视觉语言模型，通过低分辨率与高分辨率双图像编码器支持 1120×1120 输入，从而识别细小页面元素与文字。作为通才 VLM，CogAgent 在多项通用 VQA 基准（VQAv2、MM-Vet、POPE、ST-VQA 等）达 SOTA，并在 PC/安卓 GUI 导航数据集（Mind2Web、AITW）上超过基于抽取式 HTML 的 LLM 方法。

## 关键技术细节
- 规模：18B 参数，基于 CogVLM 扩展。
- 高分辨率交叉模块（high-resolution cross-module）：在原低分辨率（224）视觉专家之外，加入轻量高分辨率分支（1120×1120，小型高分编码器 EVA2-CLIP-L + 交叉注意力），低开销看清小文字/图标。
- 输入分辨率：支持 1120×1120。
- agent 能力：可输出"plan + next action + grounded operation（带坐标的点击/输入）"，面向 GUI 自动化。
- 数据：构造 GUI grounding、OCR、网页/移动端截图问答等预训练与指令数据。
- 性能：通用 VQA 多基准 SOTA；GUI 导航 Mind2Web、AITW 超过抽取式 HTML+LLM 方法。

## 原始链接
- url: https://arxiv.org/abs/2312.08914
- pdf_url: https://arxiv.org/pdf/2312.08914
- github_url: https://github.com/THUDM/CogVLM

## 一手源存档（sources/）
- cogagent.pdf  （PDF 不入 git，走 HF bucket）
