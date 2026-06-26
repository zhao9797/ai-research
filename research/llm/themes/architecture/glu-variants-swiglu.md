---
title: "GLU Variants Improve Transformer (SwiGLU)"
org: Google
country: US
date: 2020-02
type: paper
categories: [架构]
url: https://arxiv.org/abs/2002.05202
pdf_url: https://arxiv.org/pdf/2002.05202
downloaded: [swiglu.pdf]
---

## 一句话定位
Noam Shazeer 测试一系列门控线性单元 (GLU) 变体替换 Transformer FFN 的激活，发现 SwiGLU/GEGLU 等明显优于 ReLU/GELU，SwiGLU 成为现代 LLM FFN 的事实标准。

## 摘要（3-6 句）
GLU 由两个线性投影的逐元素乘积构成，其中一个先过门控函数。论文把 sigmoid 换成各种非线性（或线性）函数，得到 GEGLU、SwiGLU、ReGLU、Bilinear 等变体，并在 Transformer 的 FFN 子层替换常用的 ReLU/GELU。在 T5 风格的迁移学习评测中，这些 GLU 变体（尤其 GEGLU、SwiGLU）在预训练困惑度和下游任务上稳定优于基线，几乎不增加计算（保持 FLOPs 相当需把隐藏维度乘 2/3）。

## 关键技术细节
- SwiGLU：FFN(x) = (Swish(xW) ⊙ xV) W2，用 Swish/SiLU 作门控；GEGLU 用 GELU。
- 为保持参数/FLOPs 与标准 FFN 相当，门控版把中间维度设为约 2/3·(4d)（即 8/3·d）。
- 结果：GEGLU、SwiGLU 在 T5 预训练与 GLUE/SuperGLUE 下游上优于 ReLU、GELU。
- 现状：SwiGLU 被 LLaMA、PaLM、Qwen、Mistral、DeepSeek 等几乎所有现代 LLM 采用。
- 作者：Noam Shazeer。

## 原始链接
- url: https://arxiv.org/abs/2002.05202
- pdf_url: https://arxiv.org/pdf/2002.05202

## 一手源存档（sources/）
- swiglu.pdf  （PDF 不入 git，走 HF bucket）
