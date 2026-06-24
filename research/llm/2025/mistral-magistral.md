---
title: Magistral (Mistral 首个推理模型)
org: Mistral AI
country: France/EU
date: 2025-06
type: technical-report
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2506.10910
pdf_url: https://arxiv.org/pdf/2506.10910
github_url:
downloaded: [files/magistral.pdf]
---

## 一句话定位
Mistral AI 2025-06-12 的 Magistral 技术报告：Mistral 首个推理模型与自研可扩展 RL 流水线，完全不依赖他人实现或蒸馏自他模型的 RL traces，从零自建 RL 栈做纯 RL 训练。

## 摘要
Magistral 从头自建 RL 流水线，仅用自家模型与基础设施，探索 LLM 纯 RL 训练极限。给出强制推理语言（reasoning language）的简单方法，并证明仅在文本数据上做 RL 能维持初始检查点的大部分能力（多模态理解、指令遵循、函数调用保持或提升）。发布 Magistral Medium（在 Mistral Medium 3 上纯 RL 训练得到）与开源 Magistral Small（Apache 2.0，含来自 Medium 的 cold-start 数据）。

## 关键技术细节（带数字）
- Magistral Medium：在 Mistral Medium 3 之上仅用 RL（RLVR，Reinforcement Learning from Verifiable Rewards）训练推理。
- Magistral Small：在 Mistral Small 3 之上，含 Magistral Medium 的 cold-start 蒸馏数据 + RL；开源（Apache 2.0）。
- 方法：从零（ground-up）自建 RL 栈，不用现成实现、不蒸馏他模型 RL traces；提出强制 reasoning language 的简单方法。
- 发现：纯文本 RL 维持/提升 multimodal understanding、instruction following、function calling。
- 发布日期：2025-06-12（arXiv:2506.10910）；配套官方博客 https://mistral.ai/news/magistral 。

## 原始链接
- arXiv：https://arxiv.org/abs/2506.10910
- PDF：https://arxiv.org/pdf/2506.10910
- 官方博客：https://mistral.ai/news/magistral

## 本地落盘文件
- ../../../sources/llm/2025/magistral.pdf
