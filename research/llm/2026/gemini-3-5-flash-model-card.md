---
title: Gemini 3.5 Flash Model Card
org: Google DeepMind
country: US
date: 2026-05
type: model-card
categories: [架构, 后训练]
url: https://deepmind.google/models/model-cards/gemini-3-5-flash/
pdf_url: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-5-Flash-Model-Card.pdf
github_url:
downloaded: [gemini-3-5-flash-model-card.pdf]
---

## 一句话定位
Google DeepMind 2026-05 发布的 Gemini 3.5 Flash 官方模型卡——Gemini 3 系列中的高效推理 Flash 档，1M 上下文、64K 输出，支持 thinking levels 调节质量/成本/延迟。

## 摘要
Gemini 3.5 Flash 是 Gemini 3 系列下一代原生多模态推理模型，基于 Gemini 3 Flash 推理基座，提供 thinking levels 控制质量、成本与延迟的折中。输入支持文本/图像/音频/视频，上下文窗口达 1M token，输出 64K token。架构、训练数据、硬件、软件均承自 Gemini 3 Flash（详见 Gemini 3 Flash 模型卡）。发布日期 2026 年 5 月。

## 关键技术细节
- 发布：Published May 2026。
- 定位：Gemini 3 系列推理 Flash 档；基于 Gemini 3 Flash 推理基座。
- 上下文：输入上下文窗口 up to 1M token；输出 64K token。
- 输入模态：文本、图像、音频、视频（原生多模态）。
- 推理：提供 "thinking levels" 控制质量/成本/延迟混合。
- 架构/训练/硬件/软件：均基于 Gemini 3 Flash（继承 MoE Transformer、TPU、JAX/ML Pathways；详见 Gemini 3 Flash 模型卡）。
- 分发渠道：Gemini App、Gemini Enterprise App、Gemini Enterprise Agent Platform、Google AI Studio、Gemini API、Google Search AI Mode、Google Antigravity。

## 原始链接
- url: https://deepmind.google/models/model-cards/gemini-3-5-flash/
- pdf_url: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-5-Flash-Model-Card.pdf

## 本地落盘文件
- ../../../sources/llm/2026/gemini-3-5-flash-model-card.pdf
