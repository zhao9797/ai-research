---
title: "Retentive Network: A Successor to Transformer for Large Language Models (RetNet)"
org: Microsoft Research / Tsinghua University
country: US/China
date: 2023-07
type: paper
categories: [架构]
url: https://arxiv.org/abs/2307.08621
pdf_url: https://arxiv.org/pdf/2307.08621
github_url: https://github.com/microsoft/torchscale
downloaded: [retnet.pdf]
---

## 一句话定位
RetNet 提出 retention 机制，同时支持并行训练、O(1) 递归推理、和 chunkwise 长序列线性计算三种等价形式，目标是「不可能三角」全拿下。

## 摘要（3-6 句）
RetNet 想同时实现训练并行、低成本推理和好性能（此前架构只能取其二）。它从递归与注意力的理论联系出发，提出 retention 机制，支持三种等价计算范式：parallel（训练并行）、recurrent（O(1) 推理、低显存低延迟）、chunkwise recurrent（长序列线性复杂度、块内并行块间递归）。实验显示 RetNet 在大模型规模上性能与 Transformer 相当，推理吞吐、延迟、显存显著优于 Transformer。

## 关键技术细节
- retention：用带复数衰减的状态递归替代 softmax 注意力，去掉 softmax 使得递归/并行形式等价。
- 三种范式：parallel（训练）、recurrent（推理 O(1)/step）、chunkwise（长序列线性，块内并行）。
- 多尺度 retention（multi-scale）：不同 head 用不同衰减率 γ，类似多分辨率记忆。
- 推理优势：相比 Transformer 显存与延迟随长度近乎常数，吞吐更高。
- 作者：Yutao Sun、Li Dong、Furu Wei 等（Microsoft Research）。

## 原始链接
- url: https://arxiv.org/abs/2307.08621
- pdf_url: https://arxiv.org/pdf/2307.08621
- github_url: https://github.com/microsoft/torchscale

## 一手源存档（sources/）
- retnet.pdf  （PDF 不入 git，走 HF bucket）
