---
title: Phi-4-reasoning-vision-15B Technical Report
org: Microsoft Research    country: US    date: 2026-03    type: report
categories: [预训练数据, 架构, 后训练]
url: https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/Phi-4-reasoning-vision-15B-Tech-Report.pdf    pdf_url: https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/Phi-4-reasoning-vision-15B-Tech-Report.pdf    github_url: https://github.com/microsoft/Phi-4-reasoning-vision-15B
downloaded: [phi-4-reasoning-vision-15b-tech-report.pdf]
---

## 一句话定位
Microsoft Research 2026-03-04 发布的 Phi-4-reasoning-vision-15B 技术报告——一个 15B 紧凑型开放权重多模态推理模型，强调用数据质量与架构选择以远低算力达成竞争力，擅长科学/数学推理与 UI 理解。

## 摘要
该报告介绍 Phi-4-reasoning-vision-15B：一个紧凑（15B）的开放权重多模态推理模型，目标是用更少的训练/推理算力与 token 达到与更大开放权重模型相当的视觉-语言能力，并在科学、数学推理与用户界面理解上表现突出。核心结论是"数据质量是模型性能的首要杠杆"——通过系统化过滤、纠错与合成增强获得最大提升。系统消融显示高分辨率、动态分辨率视觉编码器带来一致增益（精确感知是高质量推理的前提）。模型用"显式 mode token"混合推理/非推理数据，使单一模型既能对简单任务给出快速直答、又能对复杂问题做链式推理。属 Phi 系列，开放权重已上 HuggingFace。

## 关键技术细节
- 发布：2026-03-04（AI Frontiers / Microsoft Research）。作者：Jyoti Aneja, Michael Harrison, Neel Joshi, Tyler LaBonte, John Langford, Eduardo Salinas。
- 规模：15B 参数，紧凑开放权重多模态（视觉+语言）推理模型。
- 数据策略：系统化过滤 + 错误纠正 + 合成增强（synthetic augmentation）；强调数据质量为性能首要杠杆；做了大规模视觉编码器与图像处理消融。
- 架构：高分辨率、动态分辨率视觉编码器（dynamic-resolution encoders）带来一致增益；careful architecture choices。
- 推理模式：hybrid mix of reasoning 和 non-reasoning data + 显式 mode tokens —— 单模型可切换"快速直答"与"链式推理(CoT)"。
- 定位：用显著更少的训练与推理时算力/token 达到与现有开放权重模型竞争力。
- 资源：HuggingFace microsoft/Phi-4-reasoning-vision-15B；GitHub microsoft/Phi-4-reasoning-vision-15B；Foundry Labs。

## 原始链接
- url / pdf_url: https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/Phi-4-reasoning-vision-15B-Tech-Report.pdf
- github_url: https://github.com/microsoft/Phi-4-reasoning-vision-15B
- huggingface: https://huggingface.co/microsoft/Phi-4-reasoning-vision-15B

## 本地落盘文件
- ../../../sources/llm/2026/phi-4-reasoning-vision-15b-tech-report.pdf
