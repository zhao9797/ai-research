---
title: Effective Long-Context Scaling of Foundation Models (Llama 2 Long)
org: Meta AI
country: US
date: 2023-09
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2309.16039
pdf_url: https://arxiv.org/pdf/2309.16039
downloaded: [llama-2-long.pdf]
---

## 一句话定位
Meta 通过继续预训练把 Llama 2 扩到 32k 上下文，70B 长任务超 gpt-3.5-turbo-16k，长上下文配方研究。

## 摘要
提出支持最长 32,768 token 有效上下文的长上下文 LLM 系列：从 Llama 2 继续预训练(更长序列 + 上采样长文本数据集)。在语言建模、合成上下文探针、众多研究基准上广泛评测。研究基准上多数常规任务一致提升、长上下文任务显著提升。用低成本指令微调(不需人工长指令数据)，70B 变体即可在一套长上下文任务上超过 gpt-3.5-turbo-16k。深入分析 RoPE 限制并改进。

## 关键技术细节
- 上下文：扩到 32,768 token(有效)。
- 方法：从 Llama 2 继续预训练(continual pretraining)，额外约 400B token，长文本上采样。
- 位置编码：调整 RoPE base 频率(增大 θ)以建模更长依赖。
- 关键发现：预训练数据里“大量长文本”不是关键；长上下文继续预训练比从头长序列预训练更高效且同样有效。
- 指令微调：仅用短指令数据 + 少量合成长数据即可，无需人工长标注。
- 结果：70B 在长上下文任务套件超 gpt-3.5-turbo-16k。

## 原始链接
- url: https://arxiv.org/abs/2309.16039
- pdf_url: https://arxiv.org/pdf/2309.16039

## 本地落盘文件
- ../../../sources/llm/2023/llama-2-long.pdf
