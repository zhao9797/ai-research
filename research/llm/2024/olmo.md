---
title: "OLMo: Accelerating the Science of Language Models"
org: Allen Institute for AI (AI2)
country: US
date: 2024-02
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2402.00838
pdf_url: https://arxiv.org/pdf/2402.00838
github_url: https://github.com/allenai/OLMo
downloaded: [2402.00838.pdf]
---

## 一句话定位
OLMo：真正"全开放"语言模型——不仅放权重，还放训练数据（Dolma）、训练代码、评估代码与训练日志，旨在让 LM 科学可复现。

## 摘要
随着最强模型日益闭源（训练数据/架构/开发细节不公开），科学研究受阻。AI2 构建 OLMo —— 一个有竞争力、真正开放的语言模型，以支持对 LM 的科学研究。不同于多数仅放权重+推理代码的工作，OLMo 连同开放训练数据、训练与评估代码一并发布，以赋能开放研究社区。

## 关键技术细节
- 规模：OLMo 1B 与 7B（后续 65B）；decoder-only Transformer。
- 训练数据：Dolma（3T token，见单独页）；7B 训约 2.46T token。
- 全开放栈：权重 + Dolma 数据 + 训练代码 + 评估（Catwalk/Paloma）+ W&B 训练日志 + 中间检查点。
- 架构：无 bias、SwiGLU、RoPE、非参数 LayerNorm；BPE 词表约 50K。
- 目的：让数据/架构/训练对模型能力与风险的影响可被科学研究。

## 原始链接
- url: https://arxiv.org/abs/2402.00838
- pdf_url: https://arxiv.org/pdf/2402.00838
- github: https://github.com/allenai/OLMo

## 本地落盘文件
- ../../../sources/llm/2024/2402.00838.pdf
