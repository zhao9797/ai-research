---
title: "CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer"
org: 智谱 AI (Zhipu AI) / 清华大学
country: 中国
date: 2024-08
type: arxiv
categories: [架构, 预训练数据, AI infra]
url: https://arxiv.org/abs/2408.06072
pdf_url: https://arxiv.org/pdf/2408.06072
github_url: https://github.com/THUDM/CogVideo
downloaded: [files/cogvideox.pdf]
---

## 一句话定位
智谱开源的文生视频扩散 Transformer，3D VAE + expert transformer + 专家自适应 LayerNorm，可生成 10 秒、768×1360、16fps 的连贯视频（"清影"背后模型）。

## 摘要
CogVideoX 是基于 diffusion transformer 的大规模文生视频模型，可生成与文本提示无缝对齐的 10 秒连续视频，帧率 16fps、分辨率 768×1360。技术贡献：(1) 3D VAE 沿空间与时间维度压缩视频，提升压缩率与重建质量；(2) expert transformer + expert adaptive LayerNorm，实现文本-视频两模态深度融合；(3) 渐进式训练 + 多分辨率帧打包；(4) 一套视频字幕（caption）流水线生成高质量文本-视频对，显著改善语义对齐与动作连贯性。

## 关键技术细节（带数字）
- 输出：10 秒视频，16 fps，768×1360 分辨率。
- 架构：diffusion transformer（DiT）+ expert transformer block + expert adaptive LayerNorm。
- 压缩：3D causal VAE（空间 + 时间联合压缩）。
- 数据：自建视频 caption 流水线，构造高质量 video-text 对。
- 训练：渐进式训练 + 多分辨率帧打包（frame pack）；3D full attention 建模长时序一致性。
- 应用：智谱"清影"文生视频产品背后模型，开源 2B/5B 版本。

## 原始链接
- arXiv: https://arxiv.org/abs/2408.06072
- PDF: https://arxiv.org/pdf/2408.06072
- GitHub: https://github.com/THUDM/CogVideo

## 本地落盘文件
- ../../../sources/llm/2024/cogvideox.pdf
