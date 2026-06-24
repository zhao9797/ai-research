---
title: "ERNIE-ViLG 2.0: Improving Text-to-Image Diffusion Model with Knowledge-Enhanced Mixture-of-Denoising-Experts"
org: 百度 (Baidu)
country: China
date: 2022-10
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2210.15257
pdf_url: https://arxiv.org/pdf/2210.15257
github_url:
downloaded: [ernie-vilg-2.pdf]
---

## 一句话定位
百度大规模中文文生图扩散模型，引入细粒度知识增强 + 去噪专家混合（MoE denoiser），MS-COCO zero-shot FID 6.75 创 SOTA。

## 摘要
扩散模型革新了文生图技术。现有方法虽能产出高分辨率写实图像，但仍有限制图像保真与文本相关性的开放问题。ERNIE-ViLG 2.0 是大规模中文文生图扩散模型，通过两点逐步提升生成质量：(1) 引入场景关键元素的细粒度文本与视觉知识；(2) 在不同去噪阶段使用不同的去噪专家。借此不仅在 MS-COCO 上取得 zero-shot FID 6.75 的新 SOTA，且在图像保真与图文对齐上显著超越近期模型。

## 关键技术细节
- 知识增强：用文本解析（关键词/属性）与视觉对象检测，引导模型关注场景关键元素，提升图文对齐。
- 去噪专家混合（Mixture-of-Denoising-Experts, MoDE）：把扩散去噪过程按时间步分段，不同阶段用不同专家网络，缓解单网络在不同噪声水平上的冲突。
- 规模：约 24B 参数（含多专家）。
- 结果：MS-COCO zero-shot FID 6.75（SOTA），中文文生图保真与对齐领先。
- 代表百度在生成式多模态（文心一格底座）方向的 2022 进展。

## 原始链接
- url: https://arxiv.org/abs/2210.15257
- pdf_url: https://arxiv.org/pdf/2210.15257

## 本地落盘文件
- ../../../sources/llm/2022/ernie-vilg-2.pdf
