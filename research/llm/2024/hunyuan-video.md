---
title: "HunyuanVideo: A Systematic Framework For Large Video Generative Models"
org: 腾讯混元 (Tencent Hunyuan)
country: 中国
date: 2024-12
type: arxiv
categories: [架构, 预训练数据, AI infra]
url: https://arxiv.org/abs/2412.03603
pdf_url: https://arxiv.org/pdf/2412.03603
github_url: https://github.com/Tencent/HunyuanVideo
downloaded: [files/hunyuan-video.pdf]
---

## 一句话定位
腾讯开源 13B 视频生成基础模型，是当时最大的开源视频生成模型，性能比肩甚至超过闭源模型。

## 摘要
HunyuanVideo 是新颖的开源视频基础模型，视频生成性能比肩甚至超过领先闭源模型。框架整合数据筛选、先进架构设计、渐进式模型放大与训练、高效 infra（支持大规模训练推理）。模型超过 130 亿参数，是所有开源视频生成模型中最大者。

## 关键技术细节（带数字）
- 规模：13B+ 参数（最大开源视频生成模型）。
- 架构：Transformer + 双流转单流（dual- to single-stream）扩散，3D VAE 压缩时空，文本编码用 MLLM。
- 数据：分层数据筛选流水线（多阶段质量过滤）。
- 训练：渐进式分辨率/时长放大；高效分布式 infra。
- 能力：文生视频、图生视频，含 prompt 重写与高质量动作生成。

## 原始链接
- arXiv: https://arxiv.org/abs/2412.03603
- PDF: https://arxiv.org/pdf/2412.03603
- GitHub: https://github.com/Tencent/HunyuanVideo

## 本地落盘文件
- ../../../sources/llm/2024/hunyuan-video.pdf
