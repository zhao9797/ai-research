---
title: Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B
org: Microsoft & NVIDIA
country: US
date: 2022-01
type: paper
categories: [AI infra, 预训练数据, 架构]
url: https://arxiv.org/abs/2201.11990
pdf_url: https://arxiv.org/pdf/2201.11990
github_url: https://github.com/microsoft/Megatron-DeepSpeed
downloaded: [megatron-turing-nlg-530b.pdf]
---

## 一句话定位
微软 + NVIDIA 联手训练当时最大的单体（monolithic）Transformer——5300 亿参数 MT-NLG，重点展示 DeepSpeed + Megatron 的 3D 并行 infra。

## 摘要
预训练通用语言模型可通过 zero/few-shot/微调适配下游，取得 SOTA。成功推动模型规模快速增长，需要高性能硬件、软件与算法。作为微软与 NVIDIA 的联合成果，本文给出训练最大单体 Transformer——Megatron-Turing NLG 530B（5300 亿参数）的细节：先聚焦基础设施与用 DeepSpeed + Megatron 实现的 3D 并行方法，再详述训练过程、语料设计与数据清洗（数据质量是成功关键），最后讨论评测结果与新观察到的特性。

## 关键技术细节
- 模型：530B 参数，105 层，隐藏维度 20480，128 注意力头；decoder-only。
- 训练数据：约 270B token，基于 the Pile + 额外网页/书籍等，强调数据去重与质量过滤。
- Infra：NVIDIA Selene 超算，560 台 DGX A100（共 4480 块 A100 80GB），NVLink/NVSwitch + InfiniBand。
- 3D 并行：张量并行（TP=8）× 流水并行（PP=35）× 数据并行；DeepSpeed ZeRO + Megatron-LM 结合。
- 精度：混合精度训练；达到约 113–126 TFLOP/s/GPU。
- 评测：在多项 zero/one/few-shot NLP 基准上 SOTA；讨论 few-shot 与 bias。

## 原始链接
- url: https://arxiv.org/abs/2201.11990
- pdf_url: https://arxiv.org/pdf/2201.11990
- github_url: https://github.com/microsoft/Megatron-DeepSpeed

## 本地落盘文件
- ../../../sources/llm/2022/megatron-turing-nlg-530b.pdf
