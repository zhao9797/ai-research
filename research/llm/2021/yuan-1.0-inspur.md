---
title: "Yuan 1.0: Large-Scale Pre-trained Language Model in Zero-Shot and Few-Shot Learning"
org: 浪潮 (Inspur)
country: China
date: 2021-10
type: paper
categories: [AI infra, 预训练数据, 后训练]
url: https://arxiv.org/abs/2110.04725
pdf_url: https://arxiv.org/pdf/2110.04725
github_url:
downloaded: [arxiv-2110.04725.pdf]
---

## 一句话定位
浪潮（Inspur）源 1.0：245B 中文单体（singleton）大模型，2021 年当时最大的中文稠密语言模型，配 5TB 高质量中文语料与面向分布式训练的协同设计。

## 摘要（3-6 句）
源 1.0（Yuan 1.0）提出把大规模分布式训练性能纳入模型架构设计的方法，训练出 245B 参数的单体语言模型，在数千张 GPU 上高效训练并在多个 NLP 任务取得 SOTA。构建了当时最大的高质量中文语料（5TB）。还提出校准与标签扩展方法提升 zero-shot/few-shot 表现。其生成文章难以与人写文章区分。

## 关键技术细节
- 参数：245B（中文 singleton/稠密大模型，2021 年最大中文稠密模型）。
- 数据：5TB 高质量中文语料（自研数据清洗管线从海量原始数据过滤）。
- 训练：数千张 GPU；把分布式训练性能与架构（层数/层宽）协同设计以提升效率。
- 并行：张量并行 + 流水并行 + 数据并行结合。
- 后训练/对齐萌芽：calibration + label expansion 方法稳定提升 zero/few-shot 精度。
- 生成质量：人类难以区分生成文与人写文。

## 原始链接
- url: https://arxiv.org/abs/2110.04725
- pdf_url: https://arxiv.org/pdf/2110.04725

## 一手源存档（sources/）
- [arxiv-2110.04725.pdf](https://arxiv.org/pdf/2110.04725)  （arXiv 原文 PDF，不入 git）
