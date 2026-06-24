---
title: "Tele-FLM Technical Report"
org: 北京智源 (BAAI) / 中国电信 TeleAI
country: 中国
date: 2024-04
type: arxiv
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2404.16645
pdf_url: https://arxiv.org/pdf/2404.16645
github_url: https://github.com/CofeAI/Tele-FLM
downloaded: [files/tele-flm.pdf]
---

## 一句话定位
智源 + 中国电信 TeleAI 的 52B 多语言模型（FLM-2），主打"超 50B 规模、最小试错成本"的稳定高效预训练范式，并完整开源数据配比/架构/超参。

## 摘要
针对"如何以最小试错与算力高效扩展 50B+ LLM"这一缺乏开源方法论的问题，Tele-FLM（即 FLM-2）是 52B 开源多语言大模型，具备稳定高效的预训练范式与增强的事实判断能力。完成 2T token 训练全程除硬件故障外无不稳定问题。除 checkpoint 外，还公开数据组成、模型架构、超参等细节。

## 关键技术细节（带数字）
- 规模：52B 参数（多语言）。
- 训练数据：2T tokens；公开数据配比细节。
- 稳定性：2T token 训练全程无 loss 不稳定（仅硬件故障中断）。
- 扩展技巧：借鉴 FLM 家族的 growth 训练（小模型增长到大模型）与 μP 超参迁移，降低试错成本。
- 开放：开源 checkpoint + 数据组成 + 架构 + 超参细节。

## 原始链接
- arXiv: https://arxiv.org/abs/2404.16645
- PDF: https://arxiv.org/pdf/2404.16645
- GitHub: https://github.com/CofeAI/Tele-FLM

## 本地落盘文件
- ../../../sources/llm/2024/tele-flm.pdf
