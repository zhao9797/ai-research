---
title: "CogVLM: Visual Expert for Pretrained Language Models"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua）
country: China
date: 2023-11
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2311.03079
pdf_url: https://arxiv.org/pdf/2311.03079
github_url: https://github.com/THUDM/CogVLM
downloaded: [cogvlm.pdf]
---

## 一句话定位
智谱/清华 CogVLM 提出"视觉专家模块"深度融合视觉与语言，避免浅层对齐损失 NLP 能力，CogVLM-17B 在 10 个跨模态基准 SOTA。

## 摘要（3-6 句）
不同于将图像特征映射到语言模型输入空间的浅层对齐方法，CogVLM 在注意力与 FFN 层中加入可训练的"视觉专家模块"，在冻结的预训练语言模型与图像编码器之间架桥，实现视觉-语言特征的深度融合且不损害纯 NLP 性能。CogVLM-17B 在 NoCaps、Flickr30k、RefCOCO/+/g、Visual7W、GQA、ScienceQA、VizWiz、TDIUC 等 10 个经典跨模态基准达 SOTA，并在 VQAv2、OKVQA、TextVQA、COCO captioning 等排名第二。

## 关键技术细节
- 视觉专家模块（Visual Expert）：在每个 Transformer 层的注意力和 FFN 中为图像 token 增加一套独立的 QKV 矩阵与 FFN（与语言权重并行），实现深度融合。
- 冻结 LLM（Vicuna-7B/GLM 系），仅训视觉专家 + 视觉编码器适配，保留纯语言能力。
- 图像编码器：EVA2-CLIP-E + MLP adapter。
- 规模：CogVLM-17B（约 10B 语言 + 7B 视觉专家激活）。
- 性能：10 个经典跨模态基准 SOTA；多个 VQA 基准第二。
- 衍生：后续 CogAgent（GUI agent）即在 CogVLM 基础上扩展。

## 原始链接
- url: https://arxiv.org/abs/2311.03079
- pdf_url: https://arxiv.org/pdf/2311.03079
- github_url: https://github.com/THUDM/CogVLM

## 一手源存档（sources/）
- cogvlm.pdf  （PDF 不入 git，走 HF bucket）
