---
title: "DeepNet: Scaling Transformers to 1,000 Layers (DeepNorm)"
org: Microsoft Research
country: US
date: 2022-03
type: paper
categories: [架构]
url: https://arxiv.org/abs/2203.00555
pdf_url: https://arxiv.org/pdf/2203.00555
github_url: https://github.com/microsoft/unilm
downloaded: [deepnorm.pdf]
---

## 一句话定位
DeepNet 提出 DeepNorm 归一化 + 理论推导的初始化，稳定训练极深 Transformer，首次把模型堆到 1000 层（2500 子层）。

## 摘要（3-6 句）
极深 Transformer 训练易发散。DeepNet 提出新的残差归一化函数 DeepNorm（在残差相加前对子层输出乘一个与深度相关的常数 α），并配套理论推导的初始化缩放 β，使模型更新被有界控制。它结合了 Post-LN 的好性能与 Pre-LN 的训练稳定性。作者据此把 Transformer 稳定堆到 1000 层（2500 个 attention/FFN 子层），比此前最深的深一个数量级。在 7482 个翻译方向的多语种基准上，200 层 3.2B 的 DeepNet 显著超过 48 层 SOTA。

## 关键技术细节
- DeepNorm：x = LayerNorm(α·x + f(x))，α、β 按编码器/解码器层数解析给定，约束更新幅度。
- 理论：推导出残差更新的上界，给出与深度匹配的初始化 β，避免梯度爆炸/消失。
- 结合 Post-LN 性能 + Pre-LN 稳定性。
- 规模：稳定训练到 1000 层（2500 子层）；200 层 3.2B 模型在多语种翻译上 SOTA。
- 作者：Hongyu Wang、Shuming Ma、Li Dong、Furu Wei 等。

## 原始链接
- url: https://arxiv.org/abs/2203.00555
- pdf_url: https://arxiv.org/pdf/2203.00555
- github_url: https://github.com/microsoft/unilm

## 一手源存档（sources/）
- deepnorm.pdf  （PDF 不入 git，走 HF bucket）
