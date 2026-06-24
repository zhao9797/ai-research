---
title: LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale
org: University of Washington / Meta / Hugging Face
country: US
date: 2022-08
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2208.07339
pdf_url: https://arxiv.org/pdf/2208.07339
github_url: https://github.com/bitsandbytes-foundation/bitsandbytes
downloaded: [llm-int8-2208.07339.pdf]
---

## 一句话定位
首个无精度损失的 LLM 8-bit 推理量化方案：用向量级量化处理常规通道，对少数“离群特征维度”保留 FP16，集成进 bitsandbytes/HF。

## 摘要（3-6 句）
作者发现 6.7B 参数以上的 Transformer 出现系统性的 emergent outlier features（少数维度幅值极大），简单 INT8 会因此崩溃。LLM.int8() 用混合精度分解：对 99.9% 的常规维度做 vector-wise INT8 矩阵乘，对离群维度（约 0.1%）保留 FP16，结果无性能损失。由此可在消费级/单卡上推理 175B 模型，显存近半。该方法已集成 bitsandbytes 并成为 HF Transformers 的默认 8-bit 加载。

## 关键技术细节
- vector-wise quantization：行/列各自独立缩放，比 tensor-wise 误差小。
- mixed-precision decomposition：检测 outlier feature dimension，对其用 FP16，其余 INT8。
- 6.7B 起出现 emergent outliers，是大模型量化崩溃的根因。
- 175B 模型可在单节点 8-bit 推理，无 zero-shot 性能下降；集成 bitsandbytes + HF。

## 原始链接
- url: https://arxiv.org/abs/2208.07339
- pdf_url: https://arxiv.org/pdf/2208.07339
- github_url: https://github.com/bitsandbytes-foundation/bitsandbytes

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/llm-int8-2208.07339.pdf
