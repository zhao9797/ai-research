---
title: "Baichuan-Omni Technical Report"
org: 百川智能 (Baichuan Inc.) / 西湖大学 / 浙江大学
country: 中国
date: 2024-10
type: arxiv
categories: [架构, 后训练]
url: https://arxiv.org/abs/2410.08565
pdf_url: https://arxiv.org/pdf/2410.08565
github_url: https://github.com/westlake-baichuan-mllm/bc-omni
downloaded: [files/baichuan-omni.pdf]
---

## 一句话定位
百川的首个开源 7B 全模态（image+video+audio+text）大模型，支持四模态并发处理与实时交互。

## 摘要
Baichuan-Omni 是首个开源 7B 全模态 MLLM，能并发处理图像、视频、音频、文本四种模态，提供先进多模态交互体验与强性能。训练采用从 7B 模型出发、经"多模态对齐 + 多任务微调"两阶段的有效训练方案，覆盖音频/图像/视频/文本模态，使模型具备跨模态理解与交互能力。

## 关键技术细节（带数字）
- 规模：7B（全模态 MLLM）。
- 模态：image + video + audio + text 四模态并发处理。
- 训练方案：两阶段——(1) 多模态对齐（multimodal alignment）；(2) 多任务微调（multitask fine-tuning）。
- 定位：首个开源 7B 全模态模型；在图像/视频/音频多个基准上与 Qwen2-VL、VITA 等比较。

## 原始链接
- arXiv: https://arxiv.org/abs/2410.08565
- PDF: https://arxiv.org/pdf/2410.08565
- GitHub: https://github.com/westlake-baichuan-mllm/bc-omni

## 本地落盘文件
- ../../../sources/llm/2024/baichuan-omni.pdf
