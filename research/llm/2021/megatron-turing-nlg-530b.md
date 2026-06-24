---
title: "Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, A Large-Scale Generative Language Model"
org: Microsoft & NVIDIA
country: US
date: 2021-10
type: paper
categories: [AI infra, 预训练数据, 架构]
url: https://arxiv.org/abs/2201.11990
pdf_url: https://arxiv.org/pdf/2201.11990
github_url: https://github.com/NVIDIA/Megatron-LM
downloaded: [arxiv-2201.11990.pdf, ms-mtnlg-blog.html, nvidia-mtnlg-blog.html]
---

## 一句话定位
微软 + NVIDIA 联合训练的 530B 稠密单体 Transformer MT-NLG，当时最大的单体语言模型，靠 DeepSpeed + Megatron 的 3D 并行实现。

## 摘要（3-6 句）
MT-NLG 是微软与 NVIDIA 联合训练的最大单体（monolithic）Transformer 语言模型，5300 亿参数。论文重点介绍其基础设施与用 DeepSpeed + Megatron 实现的 3D 并行（数据并行 + 流水并行 + 张量切片并行）方法，以及训练语料的设计与数据清洗技术。MT-NLG 在多个 NLP 基准上取得 zero-/one-/few-shot 的 SOTA。官方博客（2021-10-11）为首发公告，arXiv 论文 2022-01。

## 关键技术细节
- 参数：530B（530 billion），稠密单体 Transformer。
- 3D 并行：tensor-slicing + pipeline + data parallelism，结合 DeepSpeed 与 Megatron-LM。
- 内存：训练 530B 需 >10 TB 聚合内存（单 A100 80GB 远不够）。
- 硬件：NVIDIA Selene 超算，560 个 DGX A100 节点，每节点 8×80GB A100（共 4480 GPU），HDR InfiniBand 互联。
- 精度：16-bit bfloat16 混合精度。
- 吞吐：A100 16-bit 峰值 312 teraFLOP/s；实测在 280/350/420 DGX A100 服务器上分别为 126/121/113 teraFLOP/s per GPU。
- 数据：精心设计的训练语料 + 数据清洗管线（去重等）被视为成功关键。
- 官方发布博客同时由 Microsoft Research 与 NVIDIA Developer 发布。

## 原始链接
- url: https://arxiv.org/abs/2201.11990
- pdf_url: https://arxiv.org/pdf/2201.11990
- blog: https://www.microsoft.com/en-us/research/blog/using-deepspeed-and-megatron-to-train-megatron-turing-nlg-530b-the-worlds-largest-and-most-powerful-generative-language-model/
- github_url: https://github.com/NVIDIA/Megatron-LM

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2201.11990.pdf
- ../../../sources/llm/2021/ms-mtnlg-blog.html
- ../../../sources/llm/2021/nvidia-mtnlg-blog.html
