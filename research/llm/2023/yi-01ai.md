---
title: "Yi: Open Foundation Models by 01.AI"
org: 零一万物（01.AI）
country: China
date: 2024-03
type: paper
categories: [预训练数据, 架构, AI infra, 后训练]
url: https://arxiv.org/abs/2403.04652
pdf_url: https://arxiv.org/pdf/2403.04652
github_url: https://github.com/01-ai/Yi
downloaded: [yi-01ai.pdf, yi-readme.md]
---

## 一句话定位
零一万物 Yi（6B/34B）技术报告，强调"数据工程优先"的路线：以高质量 3.1T token 与精细化 SFT 取胜，并扩展到 200K 长上下文、深度复制（depth-upscaling）与视觉语言模型。（模型 2023-11 发布，正式报告 2024-03，属 2023 工作。）

## 摘要（3-6 句）
Yi 模型家族基于 6B 与 34B 基座，扩展出 chat、200K 长上下文、深度复制及视觉语言模型。基座模型在 MMLU 等基准表现强劲，chat 模型在 AlpacaEval、Chatbot Arena 上人类偏好率高。作者将性能主要归因于数据工程带来的数据质量：预训练用级联去重 + 质量过滤构建 3.1T 中英语料；微调阶段精修 <10K 条指令数据并多轮人工逐条验证。

## 关键技术细节
- 规模：6B 与 34B；34B 在 24G 显存可服务（量化后）。
- 数据：3.1T 高质量中英 token；级联去重（cascaded dedup）+ 质量过滤 + 无监督语义聚类打质量标签；偏好 3T 精炼数据而非 10T 未充分过滤数据。
- 架构（Table 1，34B）：hidden 7168 / Q-heads 56 / KV-heads 8（GQA）/ 60 层 / 预训练序列 4096 / maxLR 1.5e-4；基于 LLaMA 实现。
- 注意力：6B 与 34B 均用 GQA（LLaMA2 仅 70B 用 GQA）；SwiGLU（4h→8/3h）；RoPE + 调整基频（RoPE ABF）。
- Tokenizer：BPE（SentencePiece），词表 64,000；用 identity tokenizer 避免标点转换。
- 长上下文：4K 训练基座 → 用 RoPE ABF + 10B token 轻量继续预训练（上采样长序列，多来自书籍）扩展到 200K；1-2B token 即收敛。
- 微调：小规模（<10K）指令集多轮迭代精修，每条人工验证。
- infra：跨云弹性任务调度、按实时可用 GPU 节点跨集群运行；分层调度的微调框架；KV cache 量化控制推理成本。

## 原始链接
- url: https://arxiv.org/abs/2403.04652
- pdf_url: https://arxiv.org/pdf/2403.04652
- github_url: https://github.com/01-ai/Yi

## 一手源存档（sources/）
- yi-01ai.pdf  （PDF 不入 git，走 HF bucket）
- [yi-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/yi-readme.md)
