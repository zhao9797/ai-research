---
title: "The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale"
org: Hugging Face
country: EU
date: 2024-06
type: paper
categories: [预训练数据]
url: https://arxiv.org/abs/2406.17557
pdf_url: https://arxiv.org/pdf/2406.17557
github_url: https://huggingface.co/datasets/HuggingFaceFW/fineweb
downloaded: [2406.17557.pdf]
---

## 一句话定位
FineWeb：15 万亿 token 开放预训练数据集（来自 96 个 Common Crawl 快照），及其 1.3T token 的教育子集 FineWeb-Edu；完整公开去重/过滤消融。

## 摘要
LLM 性能高度依赖预训练数据的质量与规模，但 Llama 3、Mixtral 等 SOTA 开放模型的预训练数据不公开、构建方式鲜为人知。HuggingFace 推出 FineWeb —— 来自 96 个 Common Crawl 快照的 15T token 数据集，训出的 LLM 优于其他开放预训练数据集。为推进对数据 curation 的理解，论文详尽记录并消融全部设计选择（含去重与过滤策略的深入研究）。还推出 FineWeb-Edu —— 从 FineWeb 用教育质量分类器筛出的 1.3T token 子集，在 MMLU、ARC 等知识/推理基准上显著更好。数据集、curation 代码与全部消融模型一并开放。

## 关键技术细节
- 规模：FineWeb 15T token（96 个 CC 快照）；FineWeb-Edu 1.3T token。
- pipeline：trafilatura 抽正文 → 语言过滤 → 改良版 C4/Gopher/自定义启发式过滤 → 全局 MinHash 去重（逐快照而非跨全量去重，反直觉地更优）→ PII 处理。
- FineWeb-Edu：用 Llama-3-70B 标注的教育质量分，训练分类器筛选；显著提升 MMLU/ARC。
- 全开放：数据 + datatrove 处理库 + 所有消融检查点。
- 影响：成为 2024 后众多开放模型的事实标准预训练数据。

## 原始链接
- url: https://arxiv.org/abs/2406.17557
- pdf_url: https://arxiv.org/pdf/2406.17557
- dataset: https://huggingface.co/datasets/HuggingFaceFW/fineweb

## 本地落盘文件
- ../../../sources/llm/2024/2406.17557.pdf
