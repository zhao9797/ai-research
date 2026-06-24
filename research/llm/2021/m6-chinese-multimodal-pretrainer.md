---
title: "M6: A Chinese Multimodal Pretrainer"
org: 阿里巴巴 (Alibaba) / 清华 (Tsinghua)
country: China
date: 2021-03
type: paper
categories: [架构, 预训练数据, AI infra]
url: https://arxiv.org/abs/2103.00823
pdf_url: https://arxiv.org/pdf/2103.00823
github_url:
downloaded: [arxiv-2103.00823.pdf]
---

## 一句话定位
阿里达摩院 + 清华的 M6：中文多模态（图文）大规模预训练模型，构建最大中文多模态数据集，后续扩展到万亿/十万亿参数 MoE 路线的起点。

## 摘要（3-6 句）
M6（Multi-Modality to Multi-Modality Multitask Mega-transformer）构建了当时最大的中文多模态预训练数据集（>1.9TB 图像 + 292GB 文本，覆盖多领域），并提出统一的跨模态预训练方法对单/多模态任务统一建模。模型可做图文理解与生成（如视觉问答、图像描述、文本到图像生成、产品描述生成等）。是阿里后续把 M6 扩到万亿（M6-T）乃至十万亿参数 MoE 的基础。

## 关键技术细节
- 数据：>1.9TB 图像 + 292GB 文本（当时最大中文多模态语料）。
- 架构：统一的多模态 Transformer（M6），支持纯文本/图文跨模态任务。
- 任务：视觉问答、图文匹配、图像描述、文本到图像生成、商品文案生成等多任务统一预训练。
- 由阿里巴巴 + 清华（Jie Tang 等）联合。
- M6 系列后续在 2021 内扩展为 M6-T（万亿 MoE）/十万亿参数（用 Whale/EPL 等阿里分布式框架），本论文是其基础版。

## 原始链接
- url: https://arxiv.org/abs/2103.00823
- pdf_url: https://arxiv.org/pdf/2103.00823

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2103.00823.pdf
