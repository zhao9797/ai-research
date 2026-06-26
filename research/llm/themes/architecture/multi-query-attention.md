---
title: "Fast Transformer Decoding: One Write-Head is All You Need (Multi-Query Attention)"
org: Google
country: US
date: 2019-11
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/1911.02150
pdf_url: https://arxiv.org/pdf/1911.02150
downloaded: [mqa.pdf]
---

## 一句话定位
Noam Shazeer 提出 Multi-Query Attention (MQA)：所有注意力头共享同一组 K/V，只保留多个 Q 头，大幅缩小 KV cache、加速自回归解码。

## 摘要（3-6 句）
标准多头注意力在增量解码时反复读取大尺寸的 K/V 张量，内存带宽成为瓶颈。MQA 让多个 query head 共享单一 key head 和单一 value head，把 KV cache 缩小到原来的 1/h（h 为头数），显著降低解码时的内存访问。实验显示 MQA 解码速度大幅提升，质量仅有轻微下降。MQA 成为后续 GQA、MLA 等 KV 压缩方法的起点。

## 关键技术细节
- 结构：Q 保留 h 个头，K 和 V 各只有 1 个头，所有 Q 头共享同一 K/V。
- 收益：KV cache 体积与解码时内存带宽降为 MHA 的约 1/h；增量解码显著加速。
- 代价：模型质量略降，训练可能略不稳，催生了折中方案 GQA。
- 后被 PaLM、Falcon 等采用；是 KV 压缩谱系（MQA → GQA → MLA）的源头。
- 作者：Noam Shazeer。

## 原始链接
- url: https://arxiv.org/abs/1911.02150
- pdf_url: https://arxiv.org/pdf/1911.02150

## 一手源存档（sources/）
- mqa.pdf  （PDF 不入 git，走 HF bucket）
