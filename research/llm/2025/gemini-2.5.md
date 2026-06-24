---
title: Gemini 2.5 Technical Report
org: Google DeepMind
country: US
date: 2025-06
type: technical-report
categories: [架构, 后训练, agentic训练, AI infra]
url: https://arxiv.org/abs/2507.06261
pdf_url: https://arxiv.org/pdf/2507.06261
github_url:
downloaded: [files/gemini-2.5-report.pdf]
---

## 一句话定位
Google DeepMind 的 Gemini 2.X 系列技术报告（Gemini 2.5 Pro/Flash + 2.0 Flash/Flash-Lite），原生多模态、稀疏 MoE、带"thinking"的推理模型，覆盖能力/成本的完整 Pareto 前沿。

## 摘要
Gemini 2.5 Pro 为最强 thinking 模型，前沿编码/推理 SOTA，可处理长达 3 小时视频；Gemini 2.5 Flash 为可控 thinking 预算的 hybrid 推理模型；2.0 Flash/Flash-Lite 为低延迟非 thinking 模型。全系原生多模态（文本/图像/视频/音频）、原生工具使用、>1M token 长上下文，面向新一代 agentic 系统。底层均为 sparse MoE，TPU 训练。

## 关键技术细节（带数字）
- 架构：sparse mixture-of-experts（MoE），每 token 仅激活部分参数；原生多模态（text/image/video/audio 输入）。
- 上下文：输入 1M tokens（2.5 Pro 部分配置达 2M）；输出 8K（部分变体 64K）。
- thinking：2.5 Pro/Flash 为 thinking 模型，2.5 Flash 思考预算可控（dynamic / 可设上限）；2.0 Flash 为 non-thinking。
- 多模态：2.5 Pro 可处理最长 3 小时视频内容。
- 训练：Google TPU 集群；后训练含 RL 提升推理与工具使用。
- 模型家族跨越能力-成本 Pareto 前沿（Pro/Flash/Flash-Lite）。
- 同步官方 PDF 镜像：https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf

## 原始链接
- arXiv：https://arxiv.org/abs/2507.06261
- PDF：https://arxiv.org/pdf/2507.06261
- DeepMind 官方 PDF：https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf

## 本地落盘文件
- ../../../sources/llm/2025/gemini-2.5-report.pdf
