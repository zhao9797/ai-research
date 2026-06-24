---
title: "PanGu-α: Large-scale Autoregressive Pretrained Chinese Language Models with Auto-parallel Computation"
org: 华为 (Huawei) / 鹏城实验室 (Peng Cheng Laboratory)
country: China
date: 2021-04
type: report
categories: [架构, AI infra, 预训练数据]
url: https://arxiv.org/abs/2104.12369
pdf_url: https://arxiv.org/pdf/2104.12369
github_url:
downloaded: [arxiv-2104.12369.pdf]
---

## 一句话定位
华为 PanGu-α：最大 200B 的中文自回归大模型，全程在 2048 张昇腾 910（Ascend 910）上、用 MindSpore 五维自动并行训练——国产软硬件栈训练千亿大模型的标志性技术报告。

## 摘要（3-6 句）
PanGu-α 是华为训练的中文自回归预训练大模型，最大 2000 亿参数。模型在 MindSpore 上、于 2048 张 Ascend 910 AI 处理器集群训练，并行策略基于 MindSpore Auto-parallel，组合五个并行维度高效扩展到 2048 处理器。为增强泛化，收集 1.1TB 高质量多领域中文数据预训练。论文系统验证了 PanGu-α 在中文文本生成等任务上的能力。

## 关键技术细节
- 参数：最大 200B（另有 2.6B、13B、200B 三档）。
- 硬件：2048 × Ascend 910 AI 处理器集群（国产 NPU）。
- 软件：MindSpore + MindSpore Auto-parallel。
- 五维并行：data parallelism + op-level model parallelism + pipeline model parallelism + optimizer model parallelism + rematerialization（重计算）。
- 数据：1.1TB 高质量中文语料（多领域）。
- 架构：自回归 Transformer，额外加 query layer 预测下一 token（增强生成）。
- 由华为与鹏城实验室等联合（PanGu-α Team）。

## 原始链接
- url: https://arxiv.org/abs/2104.12369
- pdf_url: https://arxiv.org/pdf/2104.12369

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2104.12369.pdf
