---
title: dots.llm1 Technical Report
org: 小红书 hi lab (rednote / Xiaohongshu)
country: China
date: 2025-06
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2506.05767
pdf_url: https://arxiv.org/pdf/2506.05767
github_url: https://github.com/rednote-hilab/dots.llm1
downloaded: [dots-llm1.pdf]
---

## 一句话定位
小红书 hi lab 首个开源大模型：142B 总参 / 14B 激活 MoE，预训练 11.2T 高质量 token 且全程不用合成数据，性能对标 Qwen2.5-72B，每 1T token 开放中间 checkpoint。发布 2025-06-06。

## 摘要
dots.llm1 是大规模 MoE，142B 总参、每 token 激活 14B，性能比肩 SOTA 同时降低训练/推理成本。依托精心打造的高效数据处理 pipeline，在 11.2T 高质量 token 上预训练后即达到与 Qwen2.5-72B 相当的性能，并经后训练充分释放能力。值得注意：预训练全程不使用合成数据。为促进研究，开源每训练 1 万亿 token 的中间 checkpoint，提供学习动态洞察。

## 关键技术细节
- 架构：MoE，142B 总参 / 14B 激活（细粒度专家 + 共享专家，DeepSeek 风格）。
- 预训练数据：11.2T 高质量 tokens，全程无合成数据；自研高效数据处理 pipeline。
- 性能：预训练后即对标 Qwen2.5-72B。
- 开放：每 1T token 开放中间 checkpoint（罕见的训练动态透明度）。
- 后训练：SFT 等释放能力。
- 开源：GitHub rednote-hilab/dots.llm1。

## 原始链接
- url: https://arxiv.org/abs/2506.05767
- pdf_url: https://arxiv.org/pdf/2506.05767
- github_url: https://github.com/rednote-hilab/dots.llm1

## 本地落盘文件
- ../../../sources/llm/2025/dots-llm1.pdf
