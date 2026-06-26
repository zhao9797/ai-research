---
title: "ERNIE-Image Technical Report"
org: 百度 Baidu (ERNIE Team)
country: China
date: 2026-05
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2605.25347
pdf_url: https://arxiv.org/pdf/2605.25347
github_url: ""
downloaded: [ernie-image.pdf]
---

## 一句话定位
百度 ERNIE-Image，开源文生图模型，基于 8B 单流 DiT 架构，通过更有效的大规模预训练数据挖掘与监督质量提升缩小与闭源系统差距。

## 摘要
ERNIE-Image（arXiv 2026-05-25，作者 Jiaxiang Liu 等 49 人）是百度开源的文生图模型，建立在 8B 单流（single-stream）DiT 架构上，目标是通过更有效挖掘大规模预训练数据、提升全程监督质量，来缩小开源与领先闭源系统的差距。预训练采用 bottom-up 数据构造 pipeline——结合细粒度图像分类、丰富 caption 标注、美学评估、分层采样，降噪同时保留长尾概念与真实世界细节。后训练采用 top-down 数据构造 pipeline 面向高需求场景，多样化 prompt 标注以贴近真实用户输入，并用稳定化 DPO 对齐人类美学偏好。还训练 ERNIE-Image-Turbo 实现高效 8-NFE 生成，并提出 MT-DMD 缓解蒸馏中的能力漂移。

## 关键技术细节
- **架构**：8B 参数 single-stream DiT 文生图模型；开源。
- **预训练数据-bottom-up pipeline**：细粒度图像分类 + 丰富 caption 标注 + 美学评估 + 分层采样；降噪 + 保留长尾概念。
- **后训练-top-down pipeline**：面向高需求场景，多样化 prompt 标注贴近真实用户输入；stabilized DPO 对齐美学偏好。
- **加速-ERNIE-Image-Turbo**：高效 8-NFE 生成；提出 MT-DMD 缓解蒸馏能力漂移。
- **定位**：缩小开源 vs 闭源文生图差距。

## 原始链接
- url: https://arxiv.org/abs/2605.25347
- pdf_url: https://arxiv.org/pdf/2605.25347

## 一手源存档（sources/）
- ernie-image.pdf  （PDF 不入 git，走 HF bucket）
