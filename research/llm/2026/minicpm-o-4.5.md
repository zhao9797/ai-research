---
title: "MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction"
org: 面壁智能 ModelBest / OpenBMB (清华 THUNLP)
country: China
date: 2026-04
type: paper
categories: [架构, 后训练]
url: https://arxiv.org/abs/2604.27393
pdf_url: https://arxiv.org/pdf/2604.27393
github_url: https://github.com/OpenBMB/MiniCPM-o
downloaded: [minicpm-o-4.5.pdf]
---

## 一句话定位
面壁 MiniCPM-o 4.5，端侧全模态模型，面向实时全双工（full-duplex）的视觉/语音/文本全模态交互。

## 摘要
MiniCPM-o 4.5（arXiv 2026-04，OpenBMB / 面壁智能 MiniCPM Team）是面壁端侧全模态（omni-modal）大模型，目标是实时全双工（real-time full-duplex）的全模态交互——同时处理视觉、语音、文本并支持边听边说的双工对话。延续 MiniCPM 系列"小参数高能力 + 端侧可部署"的路线，在架构、数据、训练 recipe 上做高效优化。同系列 2026 H1 还有 MiniCPM-SALA（arXiv 2026-02，混合稀疏与线性注意力做高效长上下文建模，见独立条目）。

## 关键技术细节
- **定位**：端侧 omni-modal 模型，real-time full-duplex 交互（视觉+语音+文本）。
- **全双工**：支持边听边说（full-duplex），面向实时语音交互。
- **路线**：MiniCPM 系列小参数高能力、端侧（on-device）可部署。
- **相关 MiniCPM-SALA（arXiv 2602.11761，2026-02）**：Hybridizing Sparse and Linear Attention，混合稀疏注意力与线性注意力做高效长上下文建模。
- **机构/开源**：OpenBMB / 面壁智能 / 清华 THUNLP，GitHub OpenBMB/MiniCPM-o 开源。
- **备注**：具体参数/上下文/训练数字以本地 PDF 原文为准（已落盘）。

## 原始链接
- url: https://arxiv.org/abs/2604.27393
- pdf_url: https://arxiv.org/pdf/2604.27393
- github_url: https://github.com/OpenBMB/MiniCPM-o
- MiniCPM-SALA: https://arxiv.org/abs/2602.11761

## 本地落盘文件
- ../../../sources/llm/2026/minicpm-o-4.5.pdf
- ../../../sources/llm/2026/minicpm-sala.pdf
