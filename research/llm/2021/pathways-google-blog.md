---
title: "Introducing Pathways: A next-generation AI architecture"
org: Google
country: US
date: 2021-10
type: blog
categories: [AI infra, 架构]
url: https://blog.google/technology/ai/introducing-pathways-next-generation-ai-architecture/
pdf_url:
github_url:
downloaded: [google-pathways-blog.html]
---

## 一句话定位
Jeff Dean 在 Google 官方博客（2021-10-28）提出 Pathways 愿景：一个能跨任务/多模态、稀疏激活、单一模型处理千万种任务的下一代 AI 架构——后来支撑 PaLM 的 Pathways 系统的起点。

## 摘要（3-6 句）
2021 年 10 月 28 日，Google 高级研究员 Jeff Dean 发表 Pathways 博客，提出下一代 AI 架构愿景：让单一模型能处理成千上万种任务、融合多种模态、并稀疏激活（仅调用与任务相关的部分网络）。这与当时"每个任务训一个专用模型、稠密激活全部参数"的范式相反。Pathways 旨在用更少能耗实现更通用、更高效的 AI。

## 关键技术细节
- 三大主张：①一个模型做多任务（multi-task）而非每任务单模型；②多模态（multimodal）统一；③稀疏激活（sparse activation）——按需调用网络子部分，类似 MoE 思想但更细粒度。
- 目标：更高样本/能耗效率、更强泛化。
- 该愿景于 2022 年由 "Pathways: Asynchronous Distributed Dataflow for ML"（系统论文）与 PaLM（540B，用 Pathways 系统训练）落地。
- 官方一手（blog.google），作者 Jeff Dean。

## 原始链接
- url: https://blog.google/technology/ai/introducing-pathways-next-generation-ai-architecture/

## 本地落盘文件
- ../../../sources/llm/2021/google-pathways-blog.html
