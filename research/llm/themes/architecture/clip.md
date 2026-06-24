---
title: "Learning Transferable Visual Models From Natural Language Supervision (CLIP)"
org: OpenAI
country: US
date: 2021-02
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2103.00020
pdf_url: https://arxiv.org/pdf/2103.00020
github_url: https://github.com/openai/CLIP
downloaded: [clip.pdf]
---

## 一句话定位
CLIP 用 4 亿图文对做对比学习，训练出可零样本迁移的视觉-文本双塔编码器，是几乎所有现代多模态 LLM 视觉编码器的祖先。

## 摘要（3-6 句）
CLIP（Contrastive Language-Image Pre-training）用图像编码器和文本编码器构成双塔，在 4 亿（图像，文本）对上做对比学习：让匹配图文对的嵌入相似度最大、不匹配的最小。训练后，可用自然语言提示直接做零样本分类（把类名写成句子作文本侧）。CLIP 在 30+ 数据集上零样本迁移，ImageNet 零样本 76.2% top-1，匹敌有监督 ResNet-50，且对分布偏移更鲁棒。

## 关键技术细节
- 数据：自建 WIT 数据集，4 亿图文对（来自互联网）。
- 训练目标：对称的 InfoNCE 对比损失，batch 内 N² 对里识别 N 个正确配对。
- 编码器：图像侧用 ResNet 或 ViT，文本侧用 Transformer；最大模型 ViT-L/14。
- 零样本：ImageNet 零样本 76.2%（ViT-L/14@336px 达 ~76.2%），无需任何 ImageNet 标签训练。
- 影响：CLIP/SigLIP 视觉编码器被 LLaVA、Flamingo、Qwen-VL 等几乎所有 VLM 用作视觉主干。

## 原始链接
- url: https://arxiv.org/abs/2103.00020
- pdf_url: https://arxiv.org/pdf/2103.00020
- github_url: https://github.com/openai/CLIP

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/clip.pdf
