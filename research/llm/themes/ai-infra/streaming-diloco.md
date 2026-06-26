---
title: "Streaming DiLoCo with overlapping communication: Towards a Distributed Free Lunch"
org: Google DeepMind / Google Research
country: US
date: 2025-01
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2501.18512
pdf_url: https://arxiv.org/pdf/2501.18512
downloaded: [streaming-diloco-2501.18512.pdf]
---

## 一句话定位
DeepMind 的低通信分布式训练算法 DiLoCo 的改进版，通过参数子集流式同步 + 通信与计算重叠 + 量化通信，使跨低带宽链路训练大模型几乎无吞吐损失。

## 摘要（3-6 句）
传统数据并行每步都要交换全部梯度，要求设备低延迟高带宽共置。DiLoCo 用 inner（本地多步 AdamW）+ outer（周期性全局动量同步）放松此约束。Streaming DiLoCo 再加三项改进：只在每轮同步参数的一个子集（streaming partial sync）、把同步通信与后续计算重叠、对交换的 outer 梯度做量化（如降到 FP4 量级）。结果在数量级更少的通信下达到与全同步数据并行相当的质量，朝「分布式免费午餐」迈进，利于跨数据中心/低带宽训练。

## 关键技术细节
- DiLoCo 框架：H 步本地 inner 优化（AdamW）后做一次 outer 全局同步（Nesterov 动量）。
- streaming：每次只同步参数的一个分片（错峰），降低单次通信峰值。
- overlapping：把 outer 梯度通信与下一轮 inner 计算重叠，隐藏通信延迟。
- 量化通信：outer gradient 低比特（论文探索到极低精度）传输；通信量降两个数量级而质量基本不降。

## 原始链接
- url: https://arxiv.org/abs/2501.18512
- pdf_url: https://arxiv.org/pdf/2501.18512

## 一手源存档（sources/）
- [streaming-diloco-2501.18512.pdf](https://arxiv.org/pdf/2501.18512)  （arXiv 原文 PDF，不入 git）
