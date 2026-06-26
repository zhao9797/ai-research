---
title: "Perceiver: General Perception with Iterative Attention"
org: DeepMind
country: US
date: 2021-03
type: paper
categories: [架构]
url: https://arxiv.org/abs/2103.03206
pdf_url: https://arxiv.org/pdf/2103.03206
downloaded: [perceiver.pdf]
---

## 一句话定位
Perceiver 用一组固定数量的 latent 通过迭代交叉注意力从超长输入中提取信息，把注意力复杂度与输入规模解耦，可统一处理图像/音频/点云等任意模态。

## 摘要（3-6 句）
生物感知能同时处理来自多种模态的高维输入，而深度学习模型多为单模态、依赖领域先验（如视觉的局部网格）。Perceiver 基于 Transformer，对输入间关系几乎不做架构假设，却能扩展到数十万规模的输入。它的关键是引入一组小数量的 latent 单元，通过不对称交叉注意力反复「查询」庞大的输入字节数组，把二次复杂度从输入长度上移到 latent 上。Perceiver 在图像、音频、视频、点云等多模态分类上不需模态专用结构即可匹敌强基线。

## 关键技术细节
- latent bottleneck：N 个 latent（如 512）通过 cross-attention 读取 M 个输入元素（M 可达 10 万+），复杂度 O(M·N) 而非 O(M²)。
- 迭代：交替 cross-attention（latent←输入）与 latent self-attention（latent 内部），可多次迭代、权重共享。
- 模态无关：输入只是字节数组 + Fourier 位置特征，无需卷积等模态先验，统一处理图像/音频/视频/点云。
- 后续 Perceiver IO 推广到任意输出；Perceiver Resampler 被 Flamingo 用作视觉 token 压缩。

## 原始链接
- url: https://arxiv.org/abs/2103.03206
- pdf_url: https://arxiv.org/pdf/2103.03206

## 一手源存档（sources/）
- perceiver.pdf  （PDF 不入 git，走 HF bucket）
