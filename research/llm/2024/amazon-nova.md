---
title: "Introducing Amazon Nova: A new generation of foundation models"
org: Amazon (AWS)
country: US
date: 2024-12
type: blog
categories: [架构, 后训练]
url: https://press.aboutamazon.com/2024/12/introducing-amazon-nova-a-new-generation-of-foundation-models
pdf_url:
github_url:
downloaded: [amazon-nova-blog.md]
---

## 一句话定位
Amazon Nova（re:Invent 2024 发布）：AWS 自研基础模型族，含理解模型（Micro/Lite/Pro，及预告 Premier）与生成模型（Canvas 图像 / Reel 视频），主打前沿智能 + 行业领先性价比，独占 Amazon Bedrock。

## 摘要
2024-12-03（AWS re:Invent）发布。Amazon Nova 是新一代基础模型，从理解模型到多模态内容生成，主打前沿智能与行业领先的价格/性能。理解模型：Nova Micro（纯文本、最低延迟最低成本）、Nova Lite（低成本多模态，处理图像/视频/文本）、Nova Pro（高能力多模态，准确度/速度/成本均衡），并预告 2025 年初的 Nova Premier（最强、用于复杂推理与蒸馏 teacher）。生成模型：Nova Canvas（文生图）、Nova Reel（文生视频）。支持多语言、长上下文，并针对 agentic 工作流与 RAG 优化，独占 Amazon Bedrock。

## 关键技术细节
- 理解模型：Nova Micro（纯文本）、Nova Lite（多模态低成本）、Nova Pro（多模态高能力）；Nova Premier 预告（2025Q1）。
- 上下文：Micro/Lite/Pro 支持 300K token（Premier 预告更长）。
- 多模态：Lite/Pro 处理文本+图像+视频输入，输出文本。
- 生成模型：Nova Canvas（图像，含水印/内容审核）、Nova Reel（视频）。
- 优化：为 agentic 应用与 RAG（结合 Bedrock Knowledge Bases）微调；支持 fine-tuning 与蒸馏。
- 可用性：独占 Amazon Bedrock；价格对标更便宜。

## 原始链接
- url: https://press.aboutamazon.com/2024/12/introducing-amazon-nova-a-new-generation-of-foundation-models
- 概览/指南（落盘）: https://www.aboutamazon.com/news/aws/amazon-nova-foundation-models-guide
- 技术报告/模型卡: https://www.amazon.science/publications/the-amazon-nova-family-of-models-technical-report-and-model-card

## 本地落盘文件
- ../../../sources/llm/2024/amazon-nova-blog.md
