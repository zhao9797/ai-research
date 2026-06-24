---
title: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT)"
org: Google Research, Brain Team
country: US
date: 2020-10
type: paper
categories: [架构]
url: https://arxiv.org/abs/2010.11929
pdf_url: https://arxiv.org/pdf/2010.11929
github_url: https://github.com/google-research/vision_transformer
downloaded: [vit.pdf]
---

## 一句话定位
ViT 把图像切成 16×16 patch 序列直接喂给标准 Transformer，证明纯 Transformer 在大规模预训练下可超越 CNN，是多模态视觉编码器的架构基石。

## 摘要（3-6 句）
此前视觉任务以 CNN 为主，Transformer 应用有限。ViT 把图像分割成固定大小 patch（如 16×16），线性投影成 token 序列，加位置嵌入和一个 [CLS] token，直接用标准 Transformer 编码器分类。论文发现：在中等数据上 ViT 略逊 CNN（缺乏归纳偏置），但在大规模数据（JFT-300M）预训练后迁移，ViT 在 ImageNet 等基准上超过 SOTA CNN，且训练算力更省。

## 关键技术细节
- patch embedding：把 H×W 图像切成 N 个 P×P patch，线性映射为 token；加可学习位置嵌入与 [CLS]。
- 纯 Transformer 编码器，无卷积归纳偏置；规模 ViT-B/L/H。
- 数据依赖：小数据弱于 CNN，大数据（ImageNet-21k、JFT-300M）预训练后反超。
- 结果：ImageNet top-1 达 88%+（JFT 预训练 ViT-H/14），迁移多个基准 SOTA，训练算力低于同等 CNN。
- 影响：ViT 成为 CLIP、SigLIP、VLM 视觉塔的标准骨干。

## 原始链接
- url: https://arxiv.org/abs/2010.11929
- pdf_url: https://arxiv.org/pdf/2010.11929
- github_url: https://github.com/google-research/vision_transformer

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/vit.pdf
