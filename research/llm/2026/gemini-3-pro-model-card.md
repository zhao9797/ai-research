---
title: Gemini 3 Pro Model Card (Last Updated May 2026)
org: Google DeepMind
country: US
date: 2026-05
type: model-card
categories: [架构, 预训练数据, 后训练, AI infra]
url: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf
pdf_url: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf
github_url:
downloaded: [gemini-3-pro-model-card.pdf]
---

## 一句话定位
Google DeepMind 的 Gemini 3 Pro 官方模型卡，初次发布 2025-11、最近更新 2026-05；这一版比以往模型卡披露更多训练数据/架构信息，并列出 2026 上半年扩展出的 Gemini 3 家族成员。

## 摘要
Gemini 3 Pro 是 Gemini 系列新一代、原生多模态、推理模型，是 Google 当时最先进的复杂任务模型，能理解文本/音频/图像/视频与整库代码。模型卡（更新于 2026-05）说明 Gemini 3 Pro 采用稀疏 MoE Transformer 架构，原生支持文/视/音输入；新增 Deep Think 推理模式。模型卡明确 Gemini 3 Pro 不是对前代的微调，并列出基于它派生的家族：Gemini 3 Pro Image、Gemini 3 Flash、Gemini 3.1 Pro、Gemini 3.1 Flash Image、Gemini 3.1 Flash-Lite、Gemini 3.1 Flash Live、Gemini 3.5 Flash（其中 3.1/3.5 系列为 2026 上半年推出）。训练用 TPU + JAX/ML Pathways。

## 关键技术细节
- 模型发布：2025 年 11 月；模型卡最后更新：2026 年 5 月（本条以 2026-05 更新版为准）。
- 架构：稀疏 mixture-of-experts (MoE) Transformer；每 token 仅激活部分专家（参数）以解耦容量与单 token 计算/服务成本；原生多模态（文/视/音）。
- 推理：新增 Deep Think 模式（推理时可选增强复杂问题求解）。
- 派生家族（基于 Gemini 3 Pro）：Gemini 3 Pro Image、Gemini 3 Flash、Gemini 3.1 Pro、Gemini 3.1 Flash Image、Gemini 3.1 Flash-Lite、Gemini 3.1 Flash Live、Gemini 3.5 Flash。
- 预训练数据：大规模多领域多模态——公开网页文档、文本、代码、图像、音频（语音及其他）、视频；含公开可下载数据集、爬虫数据、商业授权数据、Google 产品用户数据（依服务条款与用户控制）。
- 后训练：含多种指令微调数据、强化学习数据、人类偏好数据；用 RL 技术利用多步推理、问题求解与定理证明数据。
- Infra：训练用 Google TPU（TPU Pods 大规模集群）；软件用 JAX 与 ML Pathways。
- 分发渠道：Gemini App、Google Cloud/Vertex AI、Google AI Studio、Gemini API、Google AI Mode、Google Antigravity、NotebookLM。

## 原始链接
- url / pdf_url: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf

## 本地落盘文件
- ../../../sources/llm/2026/gemini-3-pro-model-card.pdf
