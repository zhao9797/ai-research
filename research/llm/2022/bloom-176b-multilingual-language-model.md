---
title: "BLOOM: A 176B-Parameter Open-Access Multilingual Language Model"
org: BigScience
country: EU/International
date: 2022-11
type: paper
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2211.05100
pdf_url: https://arxiv.org/pdf/2211.05100
github_url: https://huggingface.co/bigscience/bloom
downloaded: [bloom.pdf]
---

## 一句话定位
BigScience 千人协作产出的 176B 全开放多语言 decoder-only 模型，在法国 Jean Zay 超算上训练，覆盖 46 种自然语言 + 13 种编程语言。

## 摘要
BLOOM 是 1760 亿参数的开放访问语言模型，由数百名研究者合作设计构建，目标是让大模型技术民主化。它是 decoder-only Transformer，在 ROOTS 语料（59 种语言：46 自然语言 + 13 编程语言）上训练。在多种基准上有竞争力，经多任务提示微调（BLOOMZ/xP3）后更强。模型与代码以 Responsible AI License 公开。

## 关键技术细节
- 架构：decoder-only Transformer，176B 参数，70 层，隐藏维度 14336，112 注意力头。
- 架构特性：ALiBi 位置编码、embedding LayerNorm、GeLU；词表 250680（字节级 BPE，多语言）。
- 训练数据：ROOTS 语料，约 1.6TB 文本，46 种自然语言 + 13 种编程语言（共 59 语种），约 366B token。
- Infra：法国 Jean Zay 超算，384 块 NVIDIA A100 80GB；Megatron-DeepSpeed，3D 并行（TP=4, PP=12, DP=8），ZeRO；BF16 混合精度；训练约 3.5 个月（118 天）。
- 训练算力：约 1.08M GPU 卡时。
- 衍生：BLOOMZ（xP3 多任务提示微调，跨语言指令泛化）。
- 开放程度：权重、代码、训练数据、训练过程全公开，是当时最透明的百亿级模型工程。

## 原始链接
- url: https://arxiv.org/abs/2211.05100
- pdf_url: https://arxiv.org/pdf/2211.05100
- github_url: https://huggingface.co/bigscience/bloom

## 本地落盘文件
- ../../../sources/llm/2022/bloom.pdf
