---
title: "YaRN: Efficient Context Window Extension of Large Language Models"
org: Nous Research / EleutherAI / University of Geneva
country: US/EU
date: 2023-08
type: paper
categories: [架构]
url: https://arxiv.org/abs/2309.00071
pdf_url: https://arxiv.org/pdf/2309.00071
github_url: https://github.com/jquesnelle/yarn
downloaded: [yarn.pdf]
---

## 一句话定位
YaRN（Yet another RoPE extensioN）是一种高效的 RoPE 上下文窗口扩展方法，用极少的继续训练即可把 LLaMA 类模型的上下文从 4K 扩到 64K/128K。

## 摘要（3-6 句）
RoPE 模型默认无法外推到训练长度之外。YaRN 改进了之前的位置插值（PI）与 NTK 方法，按频率分段处理 RoPE 维度（NTK-by-parts）：高频维度不插值、低频维度插值、中间维度按比例混合，并引入注意力温度缩放（attention scaling）补偿熵变化。该方法只需在约 0.1% 原始预训练 token 数上继续训练即可达到目标长度。作者把 LLaMA 扩展到 64K 和 128K 上下文，困惑度和长文检索均优于 PI 与 NTK。

## 关键技术细节
- NTK-by-parts 插值：按波长把 RoPE 维度分三档（不插值 / 线性插值 / 斜坡过渡），避免高频信息丢失。
- attention scaling：softmax 前对 logits 乘温度系数 1/t（t 随扩展比例增长），补偿长上下文下注意力分布熵的变化。
- 训练成本极低：约 400 步、0.1% 预训练数据量即可完成扩展。
- 在 LLaMA / LLaMA-2 上验证扩到 64K、128K，长文困惑度与 passkey retrieval 均优于 Position Interpolation 与纯 NTK。
- 已被大量开源长上下文模型采用（如多个 128K 版本）。

## 原始链接
- url: https://arxiv.org/abs/2309.00071
- pdf_url: https://arxiv.org/pdf/2309.00071
- github_url: https://github.com/jquesnelle/yarn

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/yarn.pdf
