---
title: Flamingo: a Visual Language Model for Few-Shot Learning
org: DeepMind    country: UK    date: 2022-04    type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2204.14198    pdf_url: https://arxiv.org/pdf/2204.14198    github_url:
downloaded: [flamingo.pdf]
---

## 一句话定位
DeepMind 的视觉语言模型 Flamingo：桥接冻结的视觉与语言大模型，支持任意交错图文输入，开启多模态 in-context few-shot。

## 摘要
用极少标注样本快速适配新任务是多模态学习的开放挑战。Flamingo 是具备此能力的视觉语言模型（VLM）族。提出关键架构创新：(i) 桥接预训练的纯视觉与纯语言模型；(ii) 处理任意交错的图文序列；(iii) 无缝接收图像或视频输入。得益于灵活性，Flamingo 可在含任意交错图文的大规模多模态网页语料上训练，从而获得 in-context few-shot 学习能力。全面评测显示其能快速适配多种图像与视频任务（开放式 VQA、字幕、分类等），few-shot 超越针对性微调的模型。

## 关键技术细节
- 架构：冻结的视觉编码器（NFNet）+ 冻结的语言模型（Chinchilla 70B 等），中间插入可训练的 Perceiver Resampler 与门控交叉注意力层（gated xattn-dense）。
- 规模：Flamingo-3B / 9B / 80B（最大基于 Chinchilla-70B）。
- 交错图文：支持任意交错 image/video + text 序列，天然支持多模态 in-context few-shot。
- 训练数据：M3W（交错图文网页）+ 图文对（ALIGN 等）+ 视频文本，混合多源。
- 结果：在 16 个多模态基准中 few-shot 超过此前针对性微调 SOTA（如 VQAv2、COCO caption、视频任务）。
- 意义：奠定"冻结大模型 + 适配层"的多模态范式，影响后续 BLIP-2、LLaVA 等。

## 原始链接
- url: https://arxiv.org/abs/2204.14198
- pdf_url: https://arxiv.org/pdf/2204.14198

## 本地落盘文件
- ../../../sources/llm/2022/flamingo.pdf
