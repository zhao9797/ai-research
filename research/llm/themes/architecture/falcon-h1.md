---
title: "Falcon-H1: A Family of Hybrid-Head Language Models Redefining Efficiency and Performance"
org: TII (Technology Innovation Institute), Falcon LLM Team
country: other
date: 2025-07
type: report
categories: [架构]
url: https://arxiv.org/abs/2507.22448
pdf_url: https://arxiv.org/pdf/2507.22448
github_url: https://github.com/tiiuae/falcon-h1
downloaded: [falcon-h1.pdf]
---

## 一句话定位
Falcon-H1 是 TII 的并行混合架构模型族：在同一层并行运行注意力头与 SSM（Mamba）头，覆盖 0.5B 到 34B，30+ checkpoint。

## 摘要（3-6 句）
Falcon-H1 采用新颖混合架构，兼顾性能与效率。不同于此前纯 Transformer 或纯 Mamba 的 Falcon，Falcon-H1 用并行混合架构（parallel hybrid），把基于注意力的机制与状态空间模型 (SSM) 并行组合——SSM 擅长长上下文记忆与算力效率。作者系统重审了模型设计、数据策略和训练动力学的几乎每个环节，挑战若干常规做法。模型有 0.5B、1.5B、1.5B-deep、3B、7B、34B 多档（base 与 instruct），加上量化版共 30+ checkpoint，性能持续刷新同档新高。

## 关键技术细节
- 并行混合（parallel hybrid）：同一层里注意力头与 Mamba2-style SSM 头并行计算后合并（区别于 Jamba/Hymba 的层间或头间串/并方式），可独立调注意力与 SSM 通道比例。
- 规模：0.5B / 1.5B / 1.5B-deep / 3B / 7B / 34B，base + instruct + 量化，30+ checkpoint。
- 系统化重审：注意力 vs SSM 通道配比、宽深权衡、数据配比、学习率/批大小等训练动力学。
- 在同参数档位上对标并超过同规模 Transformer（如 Qwen、Llama 系小模型）。
- 发布于 2025-07-31，HuggingFace tiiuae 官方组织发布。

## 原始链接
- url: https://arxiv.org/abs/2507.22448
- pdf_url: https://arxiv.org/pdf/2507.22448
- github_url: https://github.com/tiiuae/falcon-h1

## 一手源存档（sources/）
- falcon-h1.pdf  （PDF 不入 git，走 HF bucket）
