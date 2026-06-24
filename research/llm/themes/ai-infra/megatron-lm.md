---
title: "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism"
org: NVIDIA
country: US
date: 2019-09
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/1909.08053
pdf_url: https://arxiv.org/pdf/1909.08053
github_url: https://github.com/NVIDIA/Megatron-LM
downloaded: [megatron-lm-1909.08053.pdf, megatron-lm-readme.md]
---

## 一句话定位
NVIDIA 提出的张量并行（tensor/intra-layer model parallelism）经典工作，奠定了大模型训练把单层算子切到多卡的事实标准，配套开源 Megatron-LM 仓库。

## 摘要（3-6 句）
论文展示了一种极简的层内模型并行（intra-layer model parallelism）实现，仅在原生 PyTorch 中插入少量 all-reduce 通信，无需新编译器或库改动。该方法对 Transformer 的 MLP 与自注意力按列/行切分权重矩阵，使巨型模型可跨多 GPU 训练。作者训练了高达 83 亿参数的 GPT-2 类模型，在 512 张 V100 上对 8-way 模型并行达到 15.1 PetaFLOPs（76% 扩展效率，基线单卡 39 TeraFLOPs）。在 WikiText103、LAMBADA 上刷新当时 SOTA，并指出 LayerNorm 在残差块中的位置对大模型收敛至关重要。

## 关键技术细节
- 张量并行（TP）：MLP 第一层按列切 GEMM、第二层按行切，自注意力按 attention head 切分；前向 1 次、反向 1 次 all-reduce（identity/all-reduce 对偶算子 f 与 g）。
- 模型规模：训练 1.2B、2.5B、4.2B、8.3B 参数的 GPT-2；8.3B 模型 72 层、hidden 3072、24 attention heads。
- 算力：512×V100（32GB），8-way 模型并行 + 64-way 数据并行；峰值 15.1 PFLOPs，扩展效率 76%。
- 架构修正：将 LayerNorm 重排为 pre-LN 形式以稳定大模型训练。
- 词表 padding 到能被并行度整除以保证切分。

## 原始链接
- url: https://arxiv.org/abs/1909.08053
- pdf_url: https://arxiv.org/pdf/1909.08053
- github_url: https://github.com/NVIDIA/Megatron-LM

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/megatron-lm-1909.08053.pdf
- ../../../../sources/llm/themes/ai-infra/megatron-lm-readme.md
