---
title: GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models
org: Zhipu AI / Z.ai (智谱)
country: China
date: 2025-08
type: report
categories: [后训练, 架构, agentic训练]
url: https://arxiv.org/abs/2508.06471
pdf_url: https://arxiv.org/pdf/2508.06471
github_url: https://github.com/zai-org/GLM-4.5
downloaded: [glm-4.5.pdf]
---

## 一句话定位
智谱 GLM-4.5：把 Agentic / Reasoning / Coding（ARC）三类能力统一进一个 MoE 模型，后训练用专家蒸馏 + 大规模 RL（self-distillation 把多个专家模型能力合并），支持 hybrid thinking。

## 摘要（3-6 句）
GLM-4.5 是面向智能体、推理与编码（ARC）的统一基础模型，采用 MoE 架构（3550 亿总参 / 320 亿激活），并有轻量版 GLM-4.5-Air（1060 亿 / 120 亿激活）。它支持 hybrid reasoning：thinking 模式做复杂推理/工具调用，non-thinking 模式做即时响应。后训练流水线：先分别训练推理专家、agent 专家、通用聊天专家，再通过 self-distillation 把它们的能力蒸馏融合进统一模型，并叠加大规模 RL（含可验证奖励 + agent 任务 RL）。GLM-4.5 在 agentic、推理、代码综合榜单上居开放权重前列，权重开源（MIT）。

## 关键技术细节
- 架构：MoE，GLM-4.5 总参 355B / 激活 32B；GLM-4.5-Air 总参 106B / 激活 12B；相对"更深更窄"的设计、用 MTP（multi-token prediction）层加速。
- 预训练：约 23T tokens（含大量代码、推理、agent 轨迹数据），多阶段。
- 后训练：专家模型分训（reasoning / agent / general）→ self-distillation 融合 → RL（可验证奖励 + agent/工具任务的结果奖励）。
- hybrid thinking：thinking 与 non-thinking 双模式统一在一个模型内。
- agentic：原生工具调用、网页浏览、长程多步任务；在 BFCL、agent benchmark 上领先。
- 开源：GLM-4.5 / GLM-4.5-Air 权重 MIT 许可。

## 原始链接
- url: https://arxiv.org/abs/2508.06471
- pdf_url: https://arxiv.org/pdf/2508.06471
- github_url: https://github.com/zai-org/GLM-4.5

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/glm-4.5.pdf
