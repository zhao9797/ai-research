---
title: "Stable-DiffCoder: Pushing the Frontier of Code Diffusion Large Language Model"
org: 字节跳动 Seed (ByteDance Seed)
country: China
date: 2026-01
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2601.15892
pdf_url: https://arxiv.org/pdf/2601.15892
github_url: https://github.com/ByteDance-Seed/Stable-DiffCoder
downloaded: [stable-diffcoder.pdf]
---

## 一句话定位
字节 Seed 的 Stable-DiffCoder，8B 代码扩散大模型，建立在 Seed-Coder 架构/数据/训练 pipeline 上，引入 block diffusion 持续预训练阶段，证明扩散训练可超越同设定下的自回归代码模型。

## 摘要
Stable-DiffCoder（arXiv 2026-01-22，作者 Chenghao Fan 等 9 人，ByteDance Seed）是一款强大的代码扩散大模型，直接建立在 Seed-Coder 的架构、数据与训练 pipeline 上，引入 block diffusion continual pretraining (CPT) 阶段，配定制 warmup 与 block-wise clipped noise schedule。在相同架构与数据设定下，团队系统分析并设计了既稳定又能提升性能上限的高效扩散训练 pipeline。该 recipe 下 Stable-DiffCoder 在广泛代码 benchmark 上相比其自回归（AR）对照整体提升：any-order 建模改善结构化代码处理（编辑/推理），diffusion-based corruption 有助低资源编程语言学习。仅 CPT + SFT 即超越许多强 ~8B AR 与扩散代码模型，证明扩散训练能在严格受控数据/架构下提升代码建模质量。

## 关键技术细节
- **规格**：8B 代码扩散 LLM（Mask Diffusion Language Models 类型）；上下文 8K；Base + Instruct 两版。
- **基座**：直接构建在 Seed-Coder 架构、数据、训练 pipeline 之上（受控对照实验）。
- **架构/训练-block diffusion CPT**：block diffusion continual pretraining 阶段 + 定制 warmup + block-wise clipped noise schedule。
- **优势**：any-order 建模改善结构化代码处理（编辑/推理）；diffusion-based corruption 助低资源语言学习。
- **结论**：相同数据/架构下，diffusion 训练可超越纯 AR 训练的代码建模质量；仅 CPT+SFT 即超越多个强 ~8B AR/扩散代码模型。
- **开源**：HF ByteDance-Seed 官方组织 + GitHub。
- **同机构 2026 H1 相关**：Cola-DLM（连续潜空间扩散语言模型，arXiv 2605.06548，见独立条目）；Valley3 多模态、VINCIE 等。

## 原始链接
- url: https://arxiv.org/abs/2601.15892
- pdf_url: https://arxiv.org/pdf/2601.15892
- github_url: https://github.com/ByteDance-Seed/Stable-DiffCoder

## 本地落盘文件
- ../../../sources/llm/2026/stable-diffcoder.pdf
