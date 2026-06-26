---
title: "GLaM: Efficient Scaling of Language Models with Mixture-of-Experts"
org: Google
country: US
date: 2021-12
type: paper
categories: [架构, 预训练数据, AI infra]
url: https://arxiv.org/abs/2112.06905
pdf_url: https://arxiv.org/pdf/2112.06905
downloaded: [glam.pdf]
---

## 一句话定位
GLaM 是 1.2 万亿参数的 MoE 语言模型，每 token 只激活约 97B（8%），训练能耗约为 GPT-3 的 1/3，却在零样本/少样本上超过 GPT-3。

## 摘要（3-6 句）
GLaM（Generalist Language Model）是稀疏激活的 MoE 模型族，最大版本 1.2T 总参数，每个 token 仅激活 96.6B 参数（top-2 路由）。相比稠密的 GPT-3（175B），GLaM 训练只用约 1/3 的能耗、约一半的推理 FLOPs，却在 29 个 NLP 任务的零样本和单样本平均上超过 GPT-3。论文系统研究了 MoE 的数据质量、扩展规律与稀疏激活效率。

## 关键技术细节
- 规模：最大 1.2T 总参数、64 专家/层、每 token top-2 激活约 96.6B（约 8%）。
- 效率：训练能耗约为 GPT-3 的 1/3；推理每 token FLOPs 约为 GPT-3 的一半。
- 数据：1.6T tokens 的高质量语料，强调数据质量过滤对 MoE 表现的重要性。
- 路由：top-2 gating + 容量因子；研究了专家数与激活参数的扩展行为。
- 训练于 GLaM 自有 TPU 集群，展示稀疏模型在质量/算力权衡上优于稠密模型。

## 原始链接
- url: https://arxiv.org/abs/2112.06905
- pdf_url: https://arxiv.org/pdf/2112.06905

## 一手源存档（sources/）
- glam.pdf  （PDF 不入 git，走 HF bucket）
