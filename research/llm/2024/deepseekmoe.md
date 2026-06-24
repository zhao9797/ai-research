---
title: "DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models"
org: DeepSeek-AI
country: 中国
date: 2024-01
type: arxiv
categories: [架构]
url: https://arxiv.org/abs/2401.06066
pdf_url: https://arxiv.org/pdf/2401.06066
github_url: https://github.com/deepseek-ai/DeepSeek-MoE
downloaded: [files/deepseekmoe.pdf]
---

## 一句话定位
提出 DeepSeekMoE 架构（细粒度专家切分 + 共享专家隔离），是后续 DeepSeek-V2/V3 MoE 的基石；16B 版以约 40% 计算量比肩 LLaMA2 7B。

## 摘要
针对 GShard 式 top-K MoE 难以保证专家专精的问题，DeepSeekMoE 引入两大策略：(1) 细粒度专家切分（fine-grained expert segmentation），把专家切得更细以获得更灵活的组合；(2) 共享专家隔离（shared expert isolation），把若干专家固定为共享以承载公共知识、减少冗余。2B 规模即可逼近同总参稠密模型上界；放大到 16B 时以约 40% 计算量达到 LLaMA2 7B 水平。

## 关键技术细节（带数字）
- 核心架构：fine-grained expert segmentation + shared expert isolation。
- 16B 模型：以约 40% 计算量达到 LLaMA2 7B 性能（约 2.8B 激活）。
- 路由：每 token 激活共享专家 + Top-K routed 专家。
- 后续影响：直接成为 DeepSeek-V2（160 routed）/V3（256 routed + 1 shared）的 FFN 基础。

## 原始链接
- arXiv: https://arxiv.org/abs/2401.06066
- PDF: https://arxiv.org/pdf/2401.06066
- GitHub: https://github.com/deepseek-ai/DeepSeek-MoE

## 本地落盘文件
- ../../../sources/llm/2024/deepseekmoe.pdf
