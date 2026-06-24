---
title: "MAP-Neo: Highly Capable and Transparent Bilingual Large Language Model Series"
org: M-A-P / 滑铁卢大学 / 武汉人工智能研究院 / 01.AI
country: 中国
date: 2024-05
type: arxiv
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2405.19327
pdf_url: https://arxiv.org/pdf/2405.19327
github_url: https://github.com/multimodal-art-projection/MAP-NEO
downloaded: [files/map-neo.pdf]
---

## 一句话定位
完全透明开源的 7B 双语大模型——不只放权重，还开放预训练语料、数据清洗流水线、中间 checkpoint 与训练代码，对标 OLMo/Pythia 的"真开源"。

## 摘要
针对最强模型（GPT/Gemini/Claude）闭源、以及多数"开源"模型只放权重而不公开训练细节的问题，MAP-Neo 追求彻底透明：开源 7B 双语模型，并提供预训练语料、数据处理流水线（Matrix Data Pile）、中间 checkpoint、训练/评测代码，性能比肩同规模业界开源模型。

## 关键技术细节（带数字）
- 规模：MAP-Neo-7B（中英双语）。
- 训练数据：约 4.5T tokens；开源完整语料 Matrix Data Pile 与去重/过滤流水线。
- 全透明：放出预训练数据、清洗代码、中间 checkpoint、训练框架、评测脚本。
- 后训练：SFT + iterative DPO。
- 定位：与 OLMo、Pythia、Amber 并列的"完全开源/可复现" LLM。

## 原始链接
- arXiv: https://arxiv.org/abs/2405.19327
- PDF: https://arxiv.org/pdf/2405.19327
- GitHub: https://github.com/multimodal-art-projection/MAP-NEO

## 本地落盘文件
- ../../../sources/llm/2024/map-neo.pdf
