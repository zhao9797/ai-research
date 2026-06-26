---
title: "LongCat-Next: Lexicalizing Modalities as Discrete Tokens"
org: 美团 Meituan (LongCat Team)
country: China
date: 2026-03
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2603.27538
pdf_url: https://arxiv.org/pdf/2603.27538
github_url: https://github.com/meituan-longcat
downloaded: [longcat-next.pdf]
---

## 一句话定位
美团 LongCat-Next，原生多模态模型，提出 DiNA（离散原生自回归）框架，把文本/视觉/音频统一到共享离散空间，用单一自回归目标建模。

## 摘要
LongCat-Next（arXiv 2026-03-29，作者 "Meituan LongCat Team"，89 人）针对当前多模态系统仍以语言为中心、把非语言模态当作外挂导致架构碎片化的问题，提出 Discrete Native Autoregressive (DiNA) 统一框架：把多模态信息表示在共享离散空间，实现跨模态一致、有原则的自回归建模。关键创新是 Discrete Native Any-resolution Visual Transformer (dNaViT)，在任意分辨率上做 tokenization 与 de-tokenization，把连续视觉信号转为分层离散 token。基于此构建 LongCat-Next——在单一自回归目标下处理文本、视觉、音频的原生多模态模型，模态特定设计最少。作为工业级基座，擅长 seeing、painting 等任务。

## 关键技术细节
- **框架-DiNA**：Discrete Native Autoregressive，多模态统一到共享离散空间，单一 next-token 自回归目标。
- **视觉 tokenizer-dNaViT**：Discrete Native Any-resolution Visual Transformer，任意分辨率 tokenize/de-tokenize，连续视觉→分层离散 token。
- **统一建模**：文本/视觉/音频单一自回归目标，最少模态特定设计。
- **范式**：把所有模态"词化"（lexicalize）为离散 token，扩展 NTP 范式到多模态。
- **能力**：工业级基座，覆盖 seeing / painting 等理解与生成。

## 原始链接
- url: https://arxiv.org/abs/2603.27538
- pdf_url: https://arxiv.org/pdf/2603.27538
- github_url: https://github.com/meituan-longcat

## 一手源存档（sources/）
- longcat-next.pdf  （PDF 不入 git，走 HF bucket）
