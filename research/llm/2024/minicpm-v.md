---
title: "MiniCPM-V: A GPT-4V Level MLLM on Your Phone"
org: 面壁智能 (ModelBest) / OpenBMB / 清华 THUNLP
country: 中国
date: 2024-08
type: arxiv
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2408.01800
pdf_url: https://arxiv.org/pdf/2408.01800
github_url: https://github.com/OpenBMB/MiniCPM-V
downloaded: [files/minicpm-v.pdf]
---

## 一句话定位
面壁端侧多模态模型系列，MiniCPM-Llama3-V 2.5（8B）以手机可跑的体量达到 GPT-4V 级别，强 OCR + 高分辨率 + 多语言 + RLAIF-V 降幻觉。

## 摘要
MiniCPM-V 是可部署到手机端的高效 MLLM 系列。最新 MiniCPM-Llama3-V 2.5 集成最新架构、预训练与对齐技术：在 OpenCompass（11 项基准）上超过 GPT-4V-1106、Gemini Pro、Claude 3；强 OCR 能力（支持 1.8M 像素任意宽高比，如 1344×1344）；通过 RLAIF-V 与 VisCPM 技术实现低幻觉与多语言（30+ 语言）支持，并可在端侧高效部署。

## 关键技术细节（带数字）
- 规模：MiniCPM-V 2.0（2.8B）、MiniCPM-Llama3-V 2.5（8B，基于 Llama3-8B）。
- 分辨率：支持最高 1.8M 像素、任意宽高比（如 1344×1344），自适应视觉编码。
- 性能：MiniCPM-Llama3-V 2.5 OpenCompass 11 基准平均超 GPT-4V-1106 / Gemini Pro / Claude 3。
- 降幻觉：RLAIF-V（AI 反馈强化学习）显著降低幻觉率。
- 多语言：30+ 种语言（VisCPM 跨语言泛化）。
- 端侧：量化后可在手机/边缘设备高效运行。

## 原始链接
- arXiv: https://arxiv.org/abs/2408.01800
- PDF: https://arxiv.org/pdf/2408.01800
- GitHub: https://github.com/OpenBMB/MiniCPM-V

## 一手源存档（sources/）
- minicpm-v.pdf  （PDF 不入 git，走 HF bucket）
