---
title: "LongWriter: Unleashing 10,000+ Word Generation from Long Context LLMs"
org: 智谱 AI (Zhipu AI) / 清华大学
country: 中国
date: 2024-08
type: arxiv
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2408.07055
pdf_url: https://arxiv.org/pdf/2408.07055
github_url: https://github.com/THUDM/LongWriter
downloaded: [files/longwriter.pdf]
---

## 一句话定位
诊断出长上下文 LLM 输出长度受 SFT 样本最大长度限制，提出 AgentWrite 流水线构造 LongWriter-6k 数据集，让模型一次性生成 1 万字以上。

## 摘要
当前长上下文 LLM 可处理 10 万 token 输入，但输出常难超过 2000 字。受控实验发现：有效生成长度被 SFT 阶段见过的样本长度上界所限——根本原因是现有 SFT 数据缺少长输出样本。为此提出 AgentWrite：基于 agent 的流水线，把超长生成任务拆成子任务，让现成 LLM 生成超过 2 万字的连贯文本；据此构造 LongWriter-6k（6000 条、输出 2k–32k 字的 SFT 数据），加入训练后模型可稳定输出 1 万字以上。

## 关键技术细节（带数字）
- 诊断：输出长度上界 ≈ SFT 数据中见过的最长输出长度。
- AgentWrite：plan-then-write，拆任务为子段，逐段写作再拼接，单次产出 >20,000 字。
- 数据：LongWriter-6k（6000 条 SFT，输出长度 2,000–32,000 字）。
- 训练：在 GLM-4-9B / Llama-3.1-8B 上 SFT + DPO。
- 评测：自建 LongBench-Write，输出长度可达 10,000+ 字且质量稳定。

## 原始链接
- arXiv: https://arxiv.org/abs/2408.07055
- PDF: https://arxiv.org/pdf/2408.07055
- GitHub: https://github.com/THUDM/LongWriter

## 一手源存档（sources/）
- longwriter.pdf  （PDF 不入 git，走 HF bucket）
