---
title: "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale"
org: Univ. of Washington / Meta AI 等 (bitsandbytes)
country: US
date: 2022-08
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2208.07339
pdf_url: https://arxiv.org/pdf/2208.07339
github_url: https://github.com/bitsandbytes-foundation/bitsandbytes
downloaded: [llm-int8.pdf]
---

## 一句话定位
提出 LLM.int8() 推理量化：175B 模型 INT8 推理显存减半且无精度损失，关键在处理大模型涌现的离群特征。

## 摘要
大模型广泛应用但推理需大量 GPU 显存。本文提出 Transformer 中前馈与注意力投影层的 Int8 矩阵乘法过程，将推理显存减半且保持全精度性能。一个 175B 参数的 16/32-bit 检查点可被加载、转为 Int8 并立即使用而无性能损失。其可行性源于理解并绕过 Transformer 中高度系统化的"涌现特征"（emergent features，主导注意力与预测性能的离群维度）。为此提出两段式量化 LLM.int8()：先用 vector-wise 量化（每个内积单独的归一化常数）量化大部分值。

## 关键技术细节
- 两段式：(1) vector-wise INT8 量化常规权重/激活；(2) 对离群特征维度保留 16-bit 做混合精度分解（约 0.1% 的维度）。
- 关键发现：约 6.7B 参数起出现系统性"离群特征"（outlier features），少数维度的极大激活值若被量化会摧毁性能，故单独高精度处理。
- 效果：OPT-175B / BLOOM-176B 等可在更少 GPU 上 INT8 推理，显存约减半，零精度损失。
- 落地：成为 Hugging Face `bitsandbytes` 库核心，催生大模型平民化部署（消费级多卡跑百亿模型）。

## 原始链接
- url: https://arxiv.org/abs/2208.07339
- pdf_url: https://arxiv.org/pdf/2208.07339
- github_url: https://github.com/bitsandbytes-foundation/bitsandbytes

## 本地落盘文件
- ../../../sources/llm/2022/llm-int8.pdf
