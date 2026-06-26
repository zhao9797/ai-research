---
title: Apple Intelligence Foundation Language Models Tech Report 2025
org: Apple
country: US
date: 2025-07
type: technical-report
categories: [架构, AI infra, 预训练数据, 后训练]
url: https://machinelearning.apple.com/research/apple-foundation-models-tech-report-2025
pdf_url: https://arxiv.org/pdf/2507.13575
github_url:
downloaded: [files/apple-foundation-models-2025.pdf]
---

## 一句话定位
Apple 2025 基础模型技术报告：两款多语言多模态基础模型——~3B 端侧模型（KV-cache 共享 + 2-bit QAT）与基于新颖 Parallel-Track MoE（PT-MoE）的服务器模型（跑在 Private Cloud Compute）。

## 摘要
报告介绍驱动 Apple Intelligence 的两款模型：(i) ~3B 端侧模型，通过 KV-cache 共享与 2-bit 量化感知训练（QAT）针对 Apple 芯片优化；(ii) 服务器模型，基于新颖 Parallel-Track Mixture-of-Experts（PT-MoE）transformer，结合 track 并行、MoE 稀疏计算与交错 global-local 注意力，在 Private Cloud Compute 上以有竞争力的成本提供高质量。两者训练于大规模多语言多模态数据（负责任 web 爬取 + 授权语料 + 高质量合成数据），再用 SFT + RL 在新异步平台上精炼，支持图像理解与工具调用。配套 Swift 原生 Foundation Models 框架（guided generation、约束工具调用、LoRA 适配微调）。

## 关键技术细节（带数字）
- 端侧模型：~3B 参数；KV-cache 共享 + 2-bit 量化感知训练（QAT）优化 Apple 芯片。
- 服务器模型：Parallel-Track Mixture-of-Experts（PT-MoE）transformer——track 并行 + MoE 稀疏计算 + 交错 global-local attention；部署于 Private Cloud Compute。
- 数据：负责任 web 爬取 + 授权语料 + 高质量合成数据；多语言 + 多模态（含图像）。
- 后训练：SFT + RL（新异步 RL 平台）；支持工具调用（tool calling）。
- 开发者框架：Swift 原生 Foundation Models framework，支持 guided generation、constrained tool calling、LoRA adapter 微调。
- 发布日期：2025-07（arXiv:2507.13575）。

## 原始链接
- 官方页面：https://machinelearning.apple.com/research/apple-foundation-models-tech-report-2025
- arXiv PDF：https://arxiv.org/pdf/2507.13575

## 一手源存档（sources/）
- apple-foundation-models-2025.pdf  （PDF 不入 git，走 HF bucket）
