---
title: "RecurrentGemma: Moving Past Transformers for Efficient Open Language Models"
org: Google DeepMind
country: US
date: 2024-04
type: report
categories: [架构]
url: https://arxiv.org/abs/2404.07839
pdf_url: https://arxiv.org/pdf/2404.07839
github_url: https://github.com/google-deepmind/recurrentgemma
downloaded: [recurrentgemma.pdf]
---

## 一句话定位
RecurrentGemma 把 Griffin 架构（门控线性递归 + 局部注意力）产品化成开放模型（2B/9B），固定大小状态、长序列推理省内存，是 DeepMind 非 Transformer 路线的落地。

## 摘要（3-6 句）
RecurrentGemma 是一族基于 Google 的 Griffin 架构的开放语言模型。Griffin 结合线性递归与局部注意力，在语言上表现优异，且状态大小固定，从而减少内存占用、在长序列上高效推理（不像 Transformer 的 KV cache 随长度线性增长）。提供 2B 与 9B 两档，各有预训练与指令微调版。尽管训练 token 更少，RecurrentGemma 性能与同规模 Gemma 基线相当。

## 关键技术细节
- 架构：Griffin（RG-LRU 门控线性递归块 + 局部/滑动窗口注意力块交替），固定大小递归状态。
- 推理优势：状态恒定，长序列吞吐高、延迟低、内存省（无随长度增长的 KV cache）。
- 规模：2B、9B（base + instruct）。
- 性能：与同规模 Gemma（Transformer）相当，但训练 token 更少。
- 是 Griffin/Hawk 论文（2402.19427）的产品化版本。

## 原始链接
- url: https://arxiv.org/abs/2404.07839
- pdf_url: https://arxiv.org/pdf/2404.07839
- github_url: https://github.com/google-deepmind/recurrentgemma

## 一手源存档（sources/）
- recurrentgemma.pdf  （PDF 不入 git，走 HF bucket）
