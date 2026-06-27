---
title: "Longformer: The Long-Document Transformer"
org: Allen Institute for AI
country: US
date: 2020-04
type: paper
categories: [架构]
url: https://arxiv.org/abs/2004.05150
pdf_url: https://arxiv.org/pdf/2004.05150
github_url: https://github.com/allenai/longformer
downloaded: [longformer.pdf]
---

## 一句话定位
Longformer 用「滑动窗口 + 扩张窗口 + 全局注意力」的稀疏注意力把复杂度从 O(n²) 降到 O(n)，是 sliding-window attention 的代表作。

## 摘要（3-6 句）
标准自注意力随序列长度二次增长，无法处理长文档。Longformer 提出线性复杂度的注意力组合：每个 token 只关注局部固定窗口（sliding window），辅以 dilated window 扩大感受野，并对少量特殊 token（如 [CLS]、问答中的问题 token）赋予全局注意力。该机制可作为标准自注意力的 drop-in 替换。Longformer 在长文档分类、QA、共指消解等任务上优于 RoBERTa，并能处理数千 token 的输入。

## 关键技术细节
- 滑动窗口注意力：每个 token 关注左右各 w/2 个邻居，复杂度 O(n·w)。
- 扩张滑动窗口（dilated）：在窗口内引入间隔，多层叠加扩大感受野而不增计算。
- 全局注意力：对任务相关的少数 token 设置全局可见，兼顾局部效率与全局信息流。
- 支持长达 4096+ token 的输入；提供自定义 CUDA kernel 实现稀疏注意力。
- sliding-window attention 后被 Mistral、Gemma 等局部/全局混合注意力方案沿用。

## 原始链接
- url: https://arxiv.org/abs/2004.05150
- pdf_url: https://arxiv.org/pdf/2004.05150
- github_url: https://github.com/allenai/longformer

## 一手源存档（sources/）
- longformer.pdf  （PDF 不入 git，走 HF bucket）
