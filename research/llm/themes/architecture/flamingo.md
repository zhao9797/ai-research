---
title: "Flamingo: a Visual Language Model for Few-Shot Learning"
org: DeepMind
country: US
date: 2022-04
type: paper
categories: [架构]
url: https://arxiv.org/abs/2204.14198
pdf_url: https://arxiv.org/pdf/2204.14198
downloaded: [flamingo.pdf]
---

## 一句话定位
Flamingo 用 Perceiver Resampler + 门控交叉注意力把冻结的视觉编码器接到冻结的大语言模型上，实现交错图文输入的少样本多模态学习，是「冻结 LLM + 视觉桥接」范式的代表。

## 摘要（3-6 句）
Flamingo 是一族视觉语言模型 (VLM)，目标是用极少标注样本快速适应新任务。它的关键架构创新：(i) 用门控交叉注意力层把强大的预训练视觉模型与预训练语言模型桥接（两者均冻结）；(ii) 用 Perceiver Resampler 把可变数量的视觉特征压成固定数量的 token；(iii) 能处理任意交错的图文/视频序列。Flamingo 在大量图文交错网页数据上训练，在 16 个多模态基准上以少样本超过此前需任务专门微调的方法。

## 关键技术细节
- Perceiver Resampler：把视觉编码器输出的可变长特征重采样成固定数量（如 64）的视觉 token。
- gated cross-attention dense (GATED XATTN-DENSE) 层：插在冻结 LLM 各层间，tanh 门控初始为 0，保证训练初期不破坏 LLM。
- 视觉与语言主干均冻结，只训练桥接层 + resampler，参数高效。
- 支持任意交错图文/视频；少样本 in-context 学习。
- 最大 Flamingo-80B（基于 Chinchilla 70B LM），在 16 个 VL 任务少样本 SOTA。

## 原始链接
- url: https://arxiv.org/abs/2204.14198
- pdf_url: https://arxiv.org/pdf/2204.14198

## 一手源存档（sources/）
- flamingo.pdf  （PDF 不入 git，走 HF bucket）
