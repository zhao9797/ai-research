---
title: "Pythia: A Suite for Analyzing LLMs Across Training and Scaling"
org: EleutherAI
country: US
date: 2023-04
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2304.01373
pdf_url: https://arxiv.org/pdf/2304.01373
github_url: https://github.com/EleutherAI/pythia
downloaded: [pythia.pdf]
---

## 一句话定位
EleutherAI 的 Pythia：16 个同序数据训练、含 154 个 checkpoint 的可复现模型套件，训练动力学研究基石。

## 摘要
为研究 LLM 训练中如何演化、规律如何随规模变化，引入 Pythia——16 个 LLM，全部在完全相同顺序的公开数据上训练，规模 70M 到 12B。每个模型公开 154 个 checkpoint，并提供工具下载/重建其精确训练 dataloader。可用于记忆、term frequency 对 few-shot 的影响、降低性别偏见等研究。训练模型、分析/训练代码与数据全部公开。

## 关键技术细节
- 模型：16 个，8 个尺寸(70M/160M/410M/1B/1.4B/2.8B/6.9B/12B)，分 deduped 与非 deduped 两套。
- 数据：The Pile(约 300B/207B token)，所有模型见到完全相同的数据顺序——可控对比关键。
- checkpoint：每模型 154 个(log+均匀间隔)，便于研究训练动力学。
- 架构：GPT-NeoX，RoPE、parallel attention+MLP、Flash Attention。
- 发现：记忆与训练步关系类泊松、term frequency 影响 few-shot、可干预降偏见。
- 开源：完整训练 dataloader 可精确重建。

## 原始链接
- url: https://arxiv.org/abs/2304.01373
- pdf_url: https://arxiv.org/pdf/2304.01373
- github_url: https://github.com/EleutherAI/pythia

## 一手源存档（sources/）
- pythia.pdf  （PDF 不入 git，走 HF bucket）
