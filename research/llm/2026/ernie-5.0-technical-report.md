---
title: "ERNIE 5.0 Technical Report"
org: 百度 Baidu (ERNIE Team)
country: China
date: 2026-02
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2602.04705
pdf_url: https://arxiv.org/pdf/2602.04705
github_url: ""
downloaded: [ernie-5.0.pdf]
---

## 一句话定位
百度 ERNIE 5.0，原生自回归的统一多模态理解+生成基座模型，文本/图像/视频/音频从零联合训练，超稀疏 MoE + 模态无关专家路由 + 弹性训练范式。

## 摘要
ERNIE 5.0（arXiv 2026-02-04，作者 Haifeng Wang 等 438 人）是百度面向统一多模态理解与生成的原生自回归基座模型，覆盖文本、图像、视频、音频。所有模态在统一的 next-group-of-tokens prediction 目标下从零训练，基于超稀疏 MoE 架构与模态无关（modality-agnostic）专家路由。为应对多样资源约束下的大规模部署，ERNIE 5.0 采用新颖的弹性训练范式：单次预训练 run 内即学出一族具有不同深度、专家容量、路由稀疏度的子模型，在内存/时间受限场景下灵活权衡性能-规模-延迟。同时系统性解决在超稀疏 MoE 与多样多模态设定下把 RL 扩展到统一基座模型的难题，保证高效稳定的后训练。同期还发布 ERNIE-Image（arXiv 2026-05，8B 单流 DiT 文生图，见独立条目）。

## 关键技术细节
- **定位**：原生自回归统一多模态（文本/图像/视频/音频）理解 + 生成基座。
- **训练目标**：统一 next-group-of-tokens prediction，所有模态从零（from scratch）训练。
- **架构**：ultra-sparse Mixture-of-Experts（超稀疏 MoE）+ modality-agnostic expert routing（模态无关专家路由）。
- **弹性训练范式**：单次预训练即学出一族子模型（不同 depth / expert capacity / routing sparsity），支持性能-规模-延迟灵活权衡。
- **后训练**：系统性解决超稀疏 MoE + 多模态下 RL 扩展到统一基座的稳定性/效率问题。
- **评测**：多模态多任务上强且均衡的性能（自称为公开披露中的领先统一模型之一）。
- **相关发布**：ERNIE-Image Technical Report（arXiv 2605.25347，8B 单流 DiT 文生图，开源）。

## 原始链接
- url: https://arxiv.org/abs/2602.04705
- pdf_url: https://arxiv.org/pdf/2602.04705

## 本地落盘文件
- ../../../sources/llm/2026/ernie-5.0.pdf
