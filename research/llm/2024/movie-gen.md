---
title: "Movie Gen: A Cast of Media Foundation Models"
org: Meta
country: US
date: 2024-10
type: report
categories: [架构, AI infra, 预训练数据]
url: https://arxiv.org/abs/2410.13720
pdf_url: https://arxiv.org/pdf/2410.13720
github_url:
downloaded: [2410.13720.pdf]
---

## 一句话定位
Movie Gen：Meta 的媒体基础模型族，30B 参数 Transformer 生成 1080p 带同步音频视频，并支持指令式视频编辑与个性化视频。

## 摘要
Movie Gen 是一族生成高质量 1080p HD 视频（不同宽高比）且带同步音频的基础模型，还支持精确的指令式视频编辑与基于用户图像的个性化视频生成。模型在文本到视频合成、视频个性化、视频编辑、视频到音频、文本到音频等多任务上达 SOTA。最大的视频生成模型是 30B 参数 Transformer，最大上下文 73K 视频 token，对应 16 秒、16 fps 的视频。论文给出架构、潜空间、训练目标与配方、数据 curation、评测协议、并行化技术与推理优化等多项技术创新与简化。

## 关键技术细节
- 视频模型：30B 参数 Transformer（flow matching 训练目标）；最大 73K 视频 token 上下文 = 16s@16fps。
- 音频模型：13B 音频生成模型（视频到音频 + 文本到音频，同步）。
- 潜空间：时空压缩的 TAE（temporal autoencoder）。
- 能力：T2V、视频个性化（基于用户图）、指令式视频编辑、V2A、T2A。
- infra：大规模训练并行化与推理优化（含 temporal tiling 等）。
- 文本编码器：组合多个（含 UL2、ByT5、MetaCLIP）。

## 原始链接
- url: https://arxiv.org/abs/2410.13720
- pdf_url: https://arxiv.org/pdf/2410.13720

## 一手源存档（sources/）
- [2410.13720.pdf](https://arxiv.org/pdf/2410.13720)  （arXiv 原文 PDF，不入 git）
