---
title: Gemini 3.1 Pro Model Card
org: Google DeepMind
country: US
date: 2026-02
type: model-card
categories: [架构, 后训练]
url: https://deepmind.google/models/model-cards/gemini-3-1-pro/
pdf_url: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-1-Pro-Model-Card.pdf
github_url:
downloaded: [gemini-3-1-pro-model-card.pdf]
---

## 一句话定位
Google DeepMind 2026-02 发布的 Gemini 3.1 Pro 官方模型卡——Gemini 3 系列下一代、原生多模态推理模型，发布时为 Google 最先进的复杂任务模型，1M 上下文、64K 输出，基于 Gemini 3 Pro。

## 摘要
Gemini 3.1 Pro 是 Gemini 3 系列的下一迭代，高能力、原生多模态推理模型；截至模型卡发布日（2026-02）为 Google 最先进的复杂任务模型，可理解文本/音频/图像/视频与整库代码的海量多模态信息。它基于 Gemini 3 Pro（非独立从头训练），架构、训练数据、硬件、软件均承自 Gemini 3 Pro 的稀疏 MoE Transformer。输入支持文/图/音/视频，上下文窗口 1M token，输出 64K token。

## 关键技术细节
- 发布：Published February 2026。
- 定位：发布时 Google 最先进的复杂任务模型；Gemini 3 系列下一迭代。
- 依赖：基于 Gemini 3 Pro（model dependencies: based on Gemini 3 Pro）。
- 架构：承自 Gemini 3 Pro —— 稀疏 mixture-of-experts (MoE) Transformer，原生多模态。
- 上下文：输入 up to 1M token；输出 64K token。
- 输入模态：文本、图像、音频、视频，及整个代码仓库。
- 训练数据/处理/硬件/软件：均基于 Gemini 3 Pro（TPU + JAX/ML Pathways；公开网页/代码/图像/音频/视频 + 授权/用户数据；RL + 人类偏好后训练）。

## 原始链接
- url: https://deepmind.google/models/model-cards/gemini-3-1-pro/
- pdf_url: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-1-Pro-Model-Card.pdf

## 一手源存档（sources/）
- gemini-3-1-pro-model-card.pdf  （PDF 不入 git，走 HF bucket）
