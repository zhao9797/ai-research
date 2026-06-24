---
title: "DeepSeek LLM: Scaling Open-Source Language Models with Longtermism"
org: DeepSeek-AI
country: 中国
date: 2024-01
type: arxiv
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2401.02954
pdf_url: https://arxiv.org/pdf/2401.02954
github_url: https://github.com/deepseek-ai/DeepSeek-LLM
downloaded: [files/deepseek-llm.pdf]
---

## 一句话定位
DeepSeek 的第一代基础模型（7B/67B 稠密），重做了 scaling law 研究并给出独到结论，67B 全面超越 LLaMA-2 70B。

## 摘要
DeepSeek LLM 是面向长期主义的开源大模型项目，深入研究 scaling law 并给出在 7B、67B 两种开源常用配置下的独到发现。在 2T token 的双语语料上从头训练，再用 SFT + DPO 得到 Chat 模型。DeepSeek LLM 67B 在代码、数学、推理等多项基准上超越 LLaMA-2 70B，开放式评测中 Chat 版优于 GPT-3.5。

## 关键技术细节（带数字）
- 规模：7B 与 67B 稠密模型；67B 采用 GQA。
- 训练数据：2T tokens 双语（中英）语料。
- 学习率：multi-step learning rate scheduler（区别于 cosine，便于持续训练）。
- Scaling law：用非嵌入 FLOPs/token 表征模型规模，重新拟合数据/模型最优配比。
- 后训练：SFT + DPO（Direct Preference Optimization）。

## 原始链接
- arXiv: https://arxiv.org/abs/2401.02954
- PDF: https://arxiv.org/pdf/2401.02954
- GitHub: https://github.com/deepseek-ai/DeepSeek-LLM

## 本地落盘文件
- ../../../sources/llm/2024/deepseek-llm.pdf
