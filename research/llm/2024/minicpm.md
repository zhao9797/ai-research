---
title: "MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies"
org: 面壁智能 (ModelBest) / OpenBMB / 清华 THUNLP
country: 中国
date: 2024-04
type: arxiv
categories: [架构, 预训练数据, AI infra]
url: https://arxiv.org/abs/2404.06395
pdf_url: https://arxiv.org/pdf/2404.06395
github_url: https://github.com/OpenBMB/MiniCPM
downloaded: [files/minicpm.pdf]
---

## 一句话定位
面壁 MiniCPM（2.4B）端侧小模型，核心贡献是 WSD（Warmup-Stable-Decay）学习率调度 + 模型风洞（model wind tunnel）超参搜索，用小模型预测大模型最优配置。

## 摘要
MiniCPM 含 1.2B 与 2.4B 非嵌入参数版本，性能可与 7B–13B 模型抗衡。两大可扩展训练策略：(1) 模型侧"模型风洞实验"——在小模型上系统搜索超参（batch size、学习率等）并外推到大模型；(2) 数据侧 WSD（Warmup-Stable-Decay）学习率调度——稳定阶段恒定学习率、退火阶段快速降，便于持续训练与数据配比研究，并据此高效研究 scaling law。还推出 MoE、长上下文、端侧多模态等变体。

## 关键技术细节（带数字）
- 规模：MiniCPM-1.2B 与 2.4B（非嵌入参数）。
- WSD 调度：Warmup-Stable-Decay，稳定期恒定 LR、退火期急降；支持持续训练与可复用中间 checkpoint。
- 模型风洞：小模型网格搜超参 → 外推大模型最优配置。
- 数据：退火阶段引入高质量 SFT 风格数据，提升下游能力。
- 衍生：MiniCPM-MoE-8x2B、MiniCPM-128K、MiniCPM-V（端侧多模态）。

## 原始链接
- arXiv: https://arxiv.org/abs/2404.06395
- PDF: https://arxiv.org/pdf/2404.06395
- GitHub: https://github.com/OpenBMB/MiniCPM

## 本地落盘文件
- ../../../sources/llm/2024/minicpm.pdf
