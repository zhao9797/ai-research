---
title: An Image is Worth 16x16 Words — Transformers for Image Recognition at Scale (ViT)
org: Google Research / Google Brain
country: US
date: 2020-10
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2010.11929
pdf_url: https://arxiv.org/pdf/2010.11929
github_url: https://github.com/google-research/vision_transformer
downloaded: [arxiv-2010.11929.pdf]
---

## 一句话定位
Vision Transformer (ViT)：把图像切成 16×16 的 patch 当作 token 直接喂给纯 Transformer，证明在大规模数据预训练下纯注意力可在图像分类上超越 CNN，是多模态大模型视觉侧的奠基架构。

## 摘要（3-6 句）
ViT 将图像分割为固定大小的 patch（如 16×16），线性投影为序列 token，加上位置编码后送入标准 Transformer encoder 做分类，几乎不引入图像专有归纳偏置。论文表明：在中等数据上 ViT 略逊于 ResNet（缺少卷积归纳偏置），但在大规模数据（ImageNet-21k、JFT-300M）预训练后，ViT 在 ImageNet 等基准上超过 SOTA CNN，且预训练算力更省。

## 关键技术细节
- 输入：图像切成 N 个 patch（如 224×224 切成 16×16 共 196 个 patch），每个 patch 线性投影为 embedding + 可学习位置编码 + 一个 [class] token。
- 架构：标准 Transformer encoder（与 NLP 的 BERT/GPT 同构），无卷积。
- 规模：ViT-Base (86M) / Large (307M) / Huge (632M)，patch 大小 14/16/32。
- 预训练数据：ImageNet-21k（1400 万图）或 JFT-300M（3 亿图）；数据越大优势越明显。
- 关键发现：缺乏 CNN 的局部/平移不变归纳偏置，故需大数据补偿；大数据下超过 BiT(ResNet) SOTA，预训练算力更低。
- ImageNet top-1 约 88.5%（ViT-H/14，JFT-300M 预训练）。

## 原始链接
- url: https://arxiv.org/abs/2010.11929
- pdf_url: https://arxiv.org/pdf/2010.11929
- github_url: https://github.com/google-research/vision_transformer

## 一手源存档（sources/）
- [arxiv-2010.11929.pdf](https://arxiv.org/pdf/2010.11929)  （arXiv 原文 PDF，不入 git）
