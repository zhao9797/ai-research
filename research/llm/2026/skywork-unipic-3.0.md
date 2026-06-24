---
title: "Skywork UniPic 3.0: Unified Multi-Image Composition via Sequence Modeling"
org: 昆仑万维 Skywork (Kunlun)
country: China
date: 2026-01
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2601.15664
pdf_url: https://arxiv.org/pdf/2601.15664
github_url: https://huggingface.co/Skywork
downloaded: [skywork-unipic-3.0.pdf]
---

## 一句话定位
昆仑万维 Skywork UniPic 3.0，统一多模态框架，把单图编辑与多图合成统一，支持任意 1~6 张输入图与任意输出分辨率，聚焦人-物交互（HOI）多图合成。

## 摘要
Skywork UniPic 3.0（arXiv 2026-01-22，作者 Hongyang Wei 等 14 人）面向社区高热度的多图合成任务（受 Nano-Banana、Seedream 4.0 流行驱动）。相比单图编辑，多图合成在一致性与质量上挑战更大，而既有模型未公开高质量融合的方法细节。通过统计分析，团队识别 Human-Object Interaction (HOI) 为社区最需类别，系统分析并实现以 HOI 为主的 SOTA 多图合成方案。UniPic 3.0 是统一多模态框架，整合单图编辑与多图合成，支持任意 1~6 张数量与分辨率的输入、任意输出分辨率（总像素预算 1024×1024 内）。设计了完整的数据收集、过滤、合成 pipeline 应对多图合成挑战。

## 关键技术细节
- **定位**：统一多模态框架（单图编辑 + 多图合成 unified）。
- **输入/输出**：任意 1~6 张输入图（任意分辨率）；任意输出分辨率（总像素预算 1024×1024 内）。
- **聚焦-HOI**：通过统计分析识别 Human-Object Interaction 为社区最需类别，做 HOI 为主的多图合成。
- **方法-序列建模**：via sequence modeling 统一多图合成。
- **数据 pipeline**：完整的数据收集 + 过滤 + 合成 pipeline 应对一致性/质量挑战。
- **机构/开源**：昆仑万维 Skywork，HF Skywork 组织开源。

## 原始链接
- url: https://arxiv.org/abs/2601.15664
- pdf_url: https://arxiv.org/pdf/2601.15664
- HF: https://huggingface.co/Skywork

## 本地落盘文件
- ../../../sources/llm/2026/skywork-unipic-3.0.pdf
