---
title: "Introducing Apple's On-Device and Server Foundation Models"
org: Apple
country: US
date: 2024-06
type: blog
categories: [架构, AI infra, 后训练]
url: https://machinelearning.apple.com/research/introducing-apple-foundation-models
pdf_url:
github_url:
downloaded: [apple-intelligence-foundation-models-blog.md]
---

## 一句话定位
WWDC24 配套官方博客，首次公布 Apple Intelligence 端侧约 3B 模型与服务器模型，强调 adapter 动态切换、低比特量化与隐私优先的数据策略。

## 摘要
2024-06-10 发布。Apple 介绍其端侧（约 3B）与服务器基础模型，作为 Apple Intelligence 的核心。博客概述模型如何为日常任务（写作润色、通知摘要、图像、App 内动作）微调与优化，关键技术包括 LoRA adapter 动态切换、grouped-query attention、低比特调色板量化以在 iPhone 上高效运行。数据来自授权与公开网络（AppleBot），明确不使用用户私有数据训练。给出在人评上对比开源/商业模型的胜率。

## 关键技术细节
- 端侧模型：约 3B 参数；2-bit/4-bit 混合调色板量化（平均 ~3.5 bit/权重），保持质量。
- adapter：针对每个功能训练 LoRA adapter，运行时按任务热切换（端侧）。
- 服务器模型：在 Private Cloud Compute 上运行（Apple 芯片 + 隐私保护）。
- 训练：AXLearn（JAX）on TPU；数据含授权出版物、AppleBot 网页、合成数据；不用用户数据。
- 后训练：拒绝采样 SFT + RLHF（iTeC、MDLOO）。
- 性能：端侧约 3B 在人评 IFEval/摘要上胜过同级开源（Gemma、Phi-3-mini 等）。

## 原始链接
- url: https://machinelearning.apple.com/research/introducing-apple-foundation-models

## 本地落盘文件
- ../../../sources/llm/2024/apple-intelligence-foundation-models-blog.md
