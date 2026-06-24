---
title: "SimPO: Simple Preference Optimization with a Reference-Free Reward"
org: Princeton / University of Virginia
country: US
date: 2024-05
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2405.14734
pdf_url: https://arxiv.org/pdf/2405.14734
github_url: https://github.com/princeton-nlp/SimPO
downloaded: [2405.14734.pdf]
---

## 一句话定位
SimPO：比 DPO 更简单且更强的偏好优化——用序列平均对数概率作隐式奖励，无需参考模型，并加入目标奖励 margin。

## 摘要
DPO 是广泛使用的离线偏好优化算法，把 RLHF 的奖励重参数化以简化训练。SimPO 更简单也更有效，关键设计是用序列的平均对数概率作为隐式奖励——这与模型生成更一致，且无需参考模型，更省算力与显存。还在 Bradley-Terry 目标中引入目标奖励 margin，鼓励 chosen 与 rejected 间更大间隔。在 Mistral、Llama 3、Gemma 2 等多种 base/instruct 设置上，SimPO 持续显著超过 DPO 及其变体，且不显著增加回复长度：AlpacaEval 2 最高超 DPO 6.4 分、Arena-Hard 超 7.5 分。基于 Gemma-2-9B-it 的最强模型在 AlpacaEval 2 上 LC 胜率 72.4%、Arena-Hard 59.1%。

## 关键技术细节
- 隐式奖励：序列平均 log prob（length-normalized），消除 DPO 的长度偏置，无需 reference model。
- 目标 margin γ：在 BT 目标中减去 margin，强制 chosen-rejected 更大间隔。
- 无参考模型：相比 DPO 省一半前向、更省显存。
- 结果：vs DPO，AlpacaEval 2 +6.4、Arena-Hard +7.5；Gemma-2-9B-it 上 AlpacaEval 2 LC 72.4%，<10B 模型 Chatbot Arena 第一。

## 原始链接
- url: https://arxiv.org/abs/2405.14734
- pdf_url: https://arxiv.org/pdf/2405.14734
- github: https://github.com/princeton-nlp/SimPO

## 本地落盘文件
- ../../../sources/llm/2024/2405.14734.pdf
