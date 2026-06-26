---
title: Towards a Human-like Open-Domain Chatbot (Meena)
org: Google Brain
country: US
date: 2020-01
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2001.09977
pdf_url: https://arxiv.org/pdf/2001.09977
github_url:
downloaded: [arxiv-2001.09977.pdf, google-meena.html]
---

## 一句话定位
Google 的 Meena：26 亿参数端到端神经对话模型，提出 SSA 人工评测指标，并发现困惑度与对话质量强相关，是开放域对话大模型的标志性工作（后续演化为 LaMDA）。

## 摘要（3-6 句）
Meena 是一个 2.6B 参数、端到端训练的神经对话模型，仅以最小化困惑度为目标，便能进行比当时 SOTA 聊天机器人更有意义、更具体的对话。论文提出新的人工评测指标 SSA（Sensibleness and Specificity Average，合理性与具体性平均），并发现困惑度与 SSA 高度相关（R²≈0.93），意味着只需优化困惑度即可提升对话质量。最佳端到端 Meena 困惑度 10.2、SSA 72%；加入过滤与解码调优的完整版 SSA 达 79%，接近人类 86%。

## 关键技术细节
- 架构：Evolved Transformer（由神经架构搜索得到的 seq2seq Transformer）；1 个 encoder block + 13 个 decoder block，强解码器是质量关键。
- 参数：2.6B；上下文最长 7 轮对话。
- 训练数据：341 GB 文本，过滤自公开社交媒体对话；相比 GPT-2 模型容量大 1.7 倍、数据多 8.5 倍。
- 训练目标：最小化下一 token 困惑度（perplexity）。
- 评测指标 SSA：众包对话中对每条回复标注“是否合理(sensible)”与“是否具体(specific)”，取两者均值；对比 Mitsuku、Cleverbot、XiaoIce、DialoGPT。
- 核心发现：困惑度与 SSA 强相关（R²=0.93），8 个不同超参/架构版本拟合。
- Meena(base) 困惑度 10.2 / SSA 72%；完整版（过滤 + 调优解码）SSA 79%；人类 86%。
- 因安全与偏见顾虑，未发布外部 demo。

## 原始链接
- url: https://arxiv.org/abs/2001.09977
- pdf_url: https://arxiv.org/pdf/2001.09977
- blog: https://research.google/blog/towards-a-conversational-agent-that-can-chat-aboutanything/

## 一手源存档（sources/）
- [arxiv-2001.09977.pdf](https://arxiv.org/pdf/2001.09977)  （arXiv 原文 PDF，不入 git）
- [google-meena.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2020/google-meena.html)
