---
title: "GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism"
org: Google
country: US
date: 2018-11
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/1811.06965
pdf_url: https://arxiv.org/pdf/1811.06965
downloaded: [gpipe-1811.06965.pdf]
---

## 一句话定位
首个通用流水线并行库，用 micro-batch 切分 + 重计算把模型按层切到多加速器训练，是后续所有 pipeline parallelism 的起点。

## 摘要（3-6 句）
GPipe 把模型按层划分为多个 stage 放到不同加速器，将一个 mini-batch 拆成多个 micro-batch 顺序注入流水线以提高设备利用，并用激活重计算降低显存。它给出近线性的扩展：对 stage 数与 micro-batch 数下 bubble 与吞吐的分析。论文用 GPipe 训练了 5.57 亿参数的 AmoebaNet 与多语言翻译 Transformer（6B 参数、128 TPU），证明几乎线性的加速与可扩展性。

## 关键技术细节
- micro-batch 流水：mini-batch 切成 m 个 micro-batch，bubble 比例约 (K-1)/(m+K-1)（K 为 stage 数）。
- 激活重计算（re-materialization）省显存，使单 stage 可放更大子模型。
- 同步训练（梯度在 micro-batch 上累加），等价单卡数值。
- 规模：557M AmoebaNet（ImageNet）、6B 参数多语言 Transformer（128 TPU v3）。

## 原始链接
- url: https://arxiv.org/abs/1811.06965
- pdf_url: https://arxiv.org/pdf/1811.06965

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/gpipe-1811.06965.pdf
