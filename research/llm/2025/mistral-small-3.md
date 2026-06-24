---
title: Mistral Small 3
org: Mistral AI
country: France/EU
date: 2025-01
type: blog
categories: [架构, 后训练]
url: https://mistral.ai/news/mistral-small-3
pdf_url:
github_url:
downloaded: [files/mistral-small-3-blog.md]
---

## 一句话定位
Mistral AI 2025-01-30 发布的延迟优化型 24B 模型 Mistral Small 3（Apache 2.0），层数远少于同类、单次前向更快，定位本地部署的高效基座。

## 摘要
Mistral Small 3 是 24B 参数、Apache 2.0 的延迟优化模型，设计目标是在适合本地部署的尺寸上"饱和"性能。层数比同类竞品少很多以缩短每次前向时间，MMLU >81%、延迟 150 tokens/s。同时发布 base 与 instruct 检查点；该版本不含 RL 也不含合成数据，定位为可用于构建推理能力的基座（早于 R1 等推理模型阶段）。

## 关键技术细节（带数字）
- 参数：24B；许可 Apache 2.0。
- 架构：层数远少于同类竞品（减少 time-per-forward-pass），延迟优化。
- 性能：MMLU >81%；延迟 150 tokens/s。
- 训练阶段：未用 RL、未用合成数据（更早期的 production pipeline 阶段），定位可二次构建推理能力的 base。
- 发布 base + instruct 两个检查点（Mistral-Small-24B-Base/Instruct-2501）。
- 对标：媲美 3 倍大的 Llama 3.3 70B。
- 发布日期：2025-01-30。

## 原始链接
- 官方博客：https://mistral.ai/news/mistral-small-3
- HF：https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501

## 本地落盘文件
- ../../../sources/llm/2025/mistral-small-3-blog.md
