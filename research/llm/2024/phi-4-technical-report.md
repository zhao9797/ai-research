---
title: "Phi-4 Technical Report"
org: Microsoft
country: US
date: 2024-12
type: report
categories: [预训练数据, 后训练]
url: https://arxiv.org/abs/2412.08905
pdf_url: https://arxiv.org/pdf/2412.08905
github_url:
downloaded: [2412.08905.pdf]
---

## 一句话定位
phi-4（14B）技术报告：把合成数据贯穿整个训练流程，在 STEM QA 上反超其 teacher（GPT-4），证明数据生成 + 后训练超越单纯蒸馏。

## 摘要
phi-4 是 14B 参数模型，训练配方以数据质量为中心。不同于多数模型主要用网页/代码等有机数据，phi-4 在整个训练过程中策略性地引入合成数据。此前 Phi 系列主要蒸馏 teacher（GPT-4），而 phi-4 在 STEM 类 QA 上大幅超过其 teacher，说明数据生成与后训练手段超越了纯蒸馏。架构相比 phi-3 几乎不变，但靠更优数据、训练课程与后训练创新，在推理类基准上相对其规模表现强劲。

## 关键技术细节
- 规模：14B 参数（架构基本沿用 phi-3，仅微调）。
- 数据核心：合成数据贯穿预训练全程（多样化 prompt、自修订、指令逆转等生成方法）；约 10T token。
- 超越 teacher：在 GPQA、MATH 等 STEM QA 上反超 GPT-4（teacher），非简单蒸馏。
- 后训练创新：SFT + 一种 pivotal token DPO（针对决定答案对错的关键 token 构造偏好对）。
- 上下文：预训练 4K，后续中训扩到 16K。

## 原始链接
- url: https://arxiv.org/abs/2412.08905
- pdf_url: https://arxiv.org/pdf/2412.08905

## 一手源存档（sources/）
- [2412.08905.pdf](https://arxiv.org/pdf/2412.08905)  （arXiv 原文 PDF，不入 git）
