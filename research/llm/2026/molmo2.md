---
title: Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding
org: Allen Institute for AI (Ai2) / University of Washington    country: US    date: 2026-01    type: paper
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2601.10611    pdf_url: https://arxiv.org/pdf/2601.10611    github_url: https://github.com/allenai/molmo2
downloaded: [molmo2-arxiv-2601.10611.pdf]
---

## 一句话定位
Ai2 + 华盛顿大学 2026-01 发布的 Molmo2——完全开放（权重/数据/代码）的视频-语言模型家族，支持视频与多图理解及像素级 grounding（指点/追踪/计数），训练于迄今最大的开放视频中心多模态语料之一。

## 摘要
当前最强视频-语言模型(VLM)仍是闭源；最强开放权重模型要么依赖来自闭源 VLM 的合成数据（实为蒸馏），要么不公开训练数据/配方，使开源社区缺乏改进 SOTA 视频(图像)语言模型的基础。许多下游应用还需要 grounding——通过指点或像素追踪，连闭源模型也常不具备。Molmo2 是新的 VLM 家族，state-of-the-art，开放权重、开放训练数据、开放训练代码，可一次分析视频与多张图像。它训练在迄今最大的完全开放视频中心多模态语料之一上，含九个新数据集（密集视频字幕、长文/长视频 QA、跨图/多图/视频的开放词表指点与追踪）。可接受单图、图集与视频输入，产出自由语言或带 grounding 的输出（如像素坐标）。已被 CVPR 2026 接收。

## 关键技术细节
- arXiv ID：2601.10611（2026-01）。机构：Allen Institute for AI + University of Washington。作者含 Christopher Clark、Ranjay Krishna、Ali Farhadi 等。58 页。
- 模型：Molmo2-4B、Molmo2-8B、Molmo2-O-7B（全开放权重）。
- 数据：Molmo2 Data —— 迄今最大开放视频中心多模态语料之一；9 个新数据集（密集视频字幕、长视频/长文 QA、开放词表 pointing & tracking）。
- 输入：单图 / 图集 / 视频；输出：自由语言 + grounded 输出（像素坐标 pointing/tracking/counting）。
- 开放程度：权重 + 训练数据 + 训练代码全开放（github.com/allenai/molmo2，playground.allenai.org）。
- 定位：开放视频 VLM，强调像素级 grounding（连闭源模型都缺）。

## 原始链接
- url: https://arxiv.org/abs/2601.10611
- pdf_url: https://arxiv.org/pdf/2601.10611
- github_url: https://github.com/allenai/molmo2
- blog: https://allenai.org/blog/molmo2

## 本地落盘文件
- ../../../sources/llm/2026/molmo2-arxiv-2601.10611.pdf
