---
title: "SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models"
org: MIT (Han Lab) / NVIDIA
country: US
date: 2022-11
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2211.10438
pdf_url: https://arxiv.org/pdf/2211.10438
github_url: https://github.com/mit-han-lab/smoothquant
downloaded: [smoothquant-2211.10438.pdf]
---

## 一句话定位
W8A8（权重和激活都 8-bit）的 PTQ 方法，通过把激活的量化难度“迁移”到权重上，使整个矩阵乘都能用 INT8，无需混合精度。

## 摘要（3-6 句）
激活含离群值导致直接 INT8 激活量化掉点严重，而权重分布平滑易量化。SmoothQuant 引入一个逐通道平滑因子 s，把激活按 1/s 缩小、权重按 s 放大（数学等价），从而把量化难度从激活迁移到权重，使 W8A8 全 INT8 成为可能。它是免训练、保精度的，在 OPT/BLOOM/GLM 等 100B+ 模型上几乎无损，相对 FP16 实现最高 1.56× 加速、显存减半。被 TensorRT-LLM 等集成。

## 关键技术细节
- 平滑变换：X̂ = X·diag(1/s)，Ŵ = diag(s)·W，s 由 per-channel 激活/权重幅值的迁移强度 α 决定。
- W8A8 全 INT8 GEMM（区别于 LLM.int8 的混合精度），更利于硬件 Tensor Core。
- 100B+ 模型（OPT-175B、BLOOM-176B、GLM-130B）几乎无损；最高 1.56× speedup、2× 显存节省。
- 训练-free PTQ，集成进 NVIDIA TensorRT-LLM、FasterTransformer。

## 原始链接
- url: https://arxiv.org/abs/2211.10438
- pdf_url: https://arxiv.org/pdf/2211.10438
- github_url: https://github.com/mit-han-lab/smoothquant

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/smoothquant-2211.10438.pdf
