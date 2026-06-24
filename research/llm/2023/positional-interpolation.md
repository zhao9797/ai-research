---
title: Extending Context Window of LLMs via Positional Interpolation
org: Meta AI
country: US
date: 2023-06
type: paper
categories: [架构]
url: https://arxiv.org/abs/2306.15595
pdf_url: https://arxiv.org/pdf/2306.15595
downloaded: [positional-interpolation.pdf]
---

## 一句话定位
Meta 的 Position Interpolation：线性下缩 RoPE 位置索引，1000 步微调把 LLaMA 扩到 32k，长上下文奠基方法。

## 摘要
提出 Position Interpolation(PI)，将 RoPE 类预训练 LLM(如 LLaMA) 的上下文窗口扩到最长 32768，仅需极少微调(1000 步内)，在 passkey 检索、语言建模、长文档摘要等需长上下文任务上表现强。扩展后模型在原窗口内任务质量保持良好。做法是线性下缩输入位置索引以匹配原窗口大小，而非外推超出训练长度(外推会致灾难性高注意力分数毁掉自注意力)。理论证明插值上界比外推至少小约 600 倍，更稳定；扩展模型保留原架构、可复用现有优化与基础设施。

## 关键技术细节
- 核心：把位置 m 缩放为 m·(L/L')，线性插值到原训练窗口内(而非外推)。
- 理论：插值的注意力分数上界比外推小约 600x，故稳定。
- 微调：仅 ≤1000 步即可适配。
- 范围：LLaMA 7B–65B 扩到 8k/16k/32k。
- 任务：passkey retrieval、PG19 语言建模、长文档摘要。
- 兼容：保留原架构，可复用现有 infra；启发 NTK/YaRN 等后续方法。

## 原始链接
- url: https://arxiv.org/abs/2306.15595
- pdf_url: https://arxiv.org/pdf/2306.15595

## 本地落盘文件
- ../../../sources/llm/2023/positional-interpolation.pdf
