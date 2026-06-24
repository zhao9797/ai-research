---
title: "ERNIE 3.0 Titan: Exploring Larger-scale Knowledge Enhanced Pre-training for Language Understanding and Generation"
org: 百度 (Baidu) & 鹏城实验室 (Peng Cheng Laboratory)
country: China
date: 2021-12
type: paper
categories: [架构, AI infra, 后训练]
url: https://arxiv.org/abs/2112.12731
pdf_url: https://arxiv.org/pdf/2112.12731
github_url: https://github.com/PaddlePaddle/ERNIE
downloaded: [arxiv-2112.12731.pdf]
---

## 一句话定位
百度 + 鹏城实验室的 ERNIE 3.0 Titan：260B 稠密中文知识增强模型（2021 年中文最大稠密模型之一），引入可信可控生成与在线蒸馏以降低部署成本。

## 摘要（3-6 句）
ERNIE 3.0 Titan 把知识增强预训练扩到 260B 参数，基于 PaddlePaddle 平台、由百度与鹏城实验室联合训练。为生成可信且可控的文本，设计了自监督对抗损失（self-supervised adversarial loss）与可控语言建模损失（controllable language modeling loss）。为降低计算与碳排放，提出在线蒸馏框架（online distillation），用大教师同时蒸馏多个学生。是 2021 年中文稠密大模型规模的代表。

## 关键技术细节
- 参数：260B（中文稠密模型）。
- 架构：基于 ERNIE 3.0 框架；universal representation modules 用 48 层、隐藏维 12288、192 个头；task-specific modules 较小（12 层/768/12 头）。
- 可信可控生成：self-supervised adversarial loss（区分真实/生成文本）+ controllable language modeling loss（属性可控生成，用 [t]/[k]/[senti]/[w] 等特殊 token）。
- 在线蒸馏（online distillation）：教师在训练中持续蒸馏多个不同规模学生，降低算力/碳排放。
- 硬件：论文测算单 NVIDIA V100（32GB，125 TFLOPS）下 2048 卡 50% 峰值需 28 天；实际在国产 + GPU 异构集群（含鹏城云脑 Ascend 910 与 GPU）训练。
- 平台：PaddlePaddle。
- 覆盖必须机构：百度 + 鹏城实验室（Peng Cheng Laboratory）。

## 原始链接
- url: https://arxiv.org/abs/2112.12731
- pdf_url: https://arxiv.org/pdf/2112.12731
- github_url: https://github.com/PaddlePaddle/ERNIE

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2112.12731.pdf
