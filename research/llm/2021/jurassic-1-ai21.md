---
title: "Jurassic-1: Technical Details and Evaluation (White Paper)"
org: AI21 Labs
country: other
date: 2021-08
type: report
categories: [架构, 预训练数据]
url: https://www.ai21.com/blog/announcing-ai21-studio-and-jurassic-1
pdf_url: https://uploads-ssl.webflow.com/60fd4503684b466578c0d307/61138924626a6981ee09caf6_jurassic_tech_paper.pdf
github_url: https://github.com/ai21labs/lm-evaluation
downloaded: [ai21-jurassic1-techpaper.pdf]
---

## 一句话定位
以色列 AI21 Labs 的 Jurassic-1 白皮书：178B 的 J1-Jumbo 与 7.5B 的 J1-Large，关键创新是 256K 超大词表（更高 tokenization 效率）与不同于 GPT-3 的深宽比。

## 摘要（3-6 句）
Jurassic-1 是 AI21 Labs 发布的一对自回归语言模型：J1-Jumbo（178B）和 J1-Large（7.5B）。白皮书描述其架构与训练，并相对 GPT-3 评估困惑度、zero-shot 与 few-shot 表现。与 GPT-3 类似但有重要差异：更大的词表与不同的深度/宽度比。作者同时开源了 zero/few-shot 评测套件（github.com/ai21labs/lm-evaluation）作为大模型评测的共享资源。

## 关键技术细节
- J1-Jumbo：178B 参数，76 层（n_layers），d_model=13,824，96 个头（n_heads），d_head=144，词表 256K。
- J1-Large：7.5B 参数，32 层，d_model=4096，32 头，d_head=128，词表 256K。
- 词表创新：256K SentencePiece 词表（vs GPT-3/T5 的 ~32K-50K），显著提升 tokens-per-byte 效率（如 Wikipedia 0.171 vs T5 SP 0.255），等价更快推理与更长有效上下文。
- 架构调整：相对 GPT-3 采用更深的层数 / 不同深宽比以提升推理速度。
- 训练语料：英文语料混合，规模与训练时长在白皮书第 2 节。
- 配套：lm-evaluation 评测套件开源。

## 原始链接
- url: https://www.ai21.com/blog/announcing-ai21-studio-and-jurassic-1
- pdf_url: https://uploads-ssl.webflow.com/60fd4503684b466578c0d307/61138924626a6981ee09caf6_jurassic_tech_paper.pdf
- github_url: https://github.com/ai21labs/lm-evaluation

## 本地落盘文件
- ../../../sources/llm/2021/ai21-jurassic1-techpaper.pdf
