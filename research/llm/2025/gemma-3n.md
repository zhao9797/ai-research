---
title: Introducing Gemma 3n
org: Google DeepMind
country: US
date: 2025-05
type: blog
categories: [架构, AI infra]
url: https://developers.googleblog.com/en/introducing-gemma-3n/
pdf_url:
github_url:
downloaded: [files/gemma-3n-blog.md]
---

## 一句话定位
Google 2025-05-20 发布的 Gemma 3n 官方开发者博客：为端侧实时多模态 AI 设计的全新共享架构（也驱动下一代 Gemini Nano），靠 Per-Layer Embeddings 与 MatFormer 嵌套训练把大模型塞进手机内存。

## 摘要
Gemma 3n 是基于全新端侧架构的首个开放模型，与 Qualcomm/MediaTek/Samsung 等移动硬件方合作优化。核心创新：Per-Layer Embeddings (PLE) 大幅降低 RAM 占用，使 5B/8B 原始参数模型以约 2B/4B 的内存开销运行（动态内存仅 2GB/3GB）；MatFormer 训练让 4B active 模型内嵌一个 2B active 子模型，可"mix'n'match"动态裁剪子模型权衡质量/延迟；支持音频（ASR + 语音翻译）、图像、视频、文本交错多模态输入。

## 关键技术细节（带数字）
- 架构：全新端侧共享架构（同时驱动下一代 Gemini Nano）。
- Per-Layer Embeddings (PLE)：原始参数 5B/8B，但内存开销相当于 2B/4B 模型，动态内存仅 2GB/3GB。
- MatFormer：4B active 模型内嵌 2B active 子模型（nested），mix'n'match 动态生成子模型（质量/延迟权衡），无需托管多个模型。
- 效率：相对 Gemma 3 4B，移动端响应快约 1.5x、质量更好、内存更低（PLE + KVC sharing + 激活量化）。
- 多模态：音频（高质量 ASR + speech-to-translated-text）+ 图像 + 视频 + 文本交错输入。
- 命名：E2B / E4B（effective 2B/4B 内存）。
- 发布日期：2025-05-20（early preview；技术报告后续发布）。

## 原始链接
- 官方博客：https://developers.googleblog.com/en/introducing-gemma-3n/
- 模型页：https://deepmind.google/models/gemma/gemma-3n/

## 本地落盘文件
- ../../../sources/llm/2025/gemma-3n-blog.md
