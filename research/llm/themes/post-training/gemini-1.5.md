---
title: "Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context"
org: Google DeepMind
country: US
date: 2024-03
type: report
categories: [架构, 后训练]
url: https://arxiv.org/abs/2403.05530
pdf_url: https://arxiv.org/pdf/2403.05530
downloaded: [gemini1.5.pdf]
---

## 一句话定位
Google DeepMind Gemini 1.5 技术报告：稀疏 MoE 多模态模型，上下文扩到百万级 token，后训练用人类偏好数据做指令微调与 RLHF（官方一手报告，体现 Google 的对齐栈）。

## 摘要（3-6 句）
Gemini 1.5（Pro / Flash）是基于稀疏 MoE Transformer 的多模态模型，最大亮点是把上下文长度扩展到 100 万 token（实验中可到 1000 万），可处理超长文档、长视频、长音频并近乎完美地做 needle-in-a-haystack 检索。报告说明其后训练阶段用人类偏好数据进行指令微调与基于人类反馈的强化学习（RLHF）对齐，并辅以安全过滤与红队评估。Gemini 1.5 Flash 通过蒸馏从 Pro 获得高效小模型。作为 Google 官方一手报告，它反映了 Google/DeepMind 的多模态对齐与后训练实践。

## 关键技术细节
- 架构：稀疏 MoE Transformer，多模态（文本/图像/音频/视频）原生输入。
- 上下文：标准 1M token（Pro/Flash），研究中扩展至 10M token；长上下文检索准确率近 100%。
- 后训练：指令微调 + 基于人类偏好的 RLHF 对齐（报告明确 human-preference data + RLHF）；安全微调与策略红队。
- Flash：通过在线蒸馏（online distillation）从 Gemini 1.5 Pro 蒸出高效模型。
- 评测：长上下文 NIAH、长文档/视频/音频理解、数学/代码/多语言；在多项基准超过 1.0 Ultra。
- 一手性：Google DeepMind 官方技术报告（arXiv 托管，官方作者署名）。

## 原始链接
- url: https://arxiv.org/abs/2403.05530
- pdf_url: https://arxiv.org/pdf/2403.05530

## 一手源存档（sources/）
- gemini1.5.pdf  （PDF 不入 git，走 HF bucket）
