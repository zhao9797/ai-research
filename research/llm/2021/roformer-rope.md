---
title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
org: Zhuiyi Technology (追一科技)
country: China
date: 2021-04
type: paper
categories: [架构]
url: https://arxiv.org/abs/2104.09864
pdf_url: https://arxiv.org/pdf/2104.09864
github_url:
downloaded: [arxiv-2104.09864.pdf]
---

## 一句话定位
追一科技提出 Rotary Position Embedding（RoPE）：用旋转矩阵把相对位置编码进 query/key，成为日后几乎所有主流 LLM（LLaMA、GLM、Qwen 等）的默认位置编码。

## 摘要（3-6 句）
RoFormer 提出 Rotary Position Embedding（RoPE），通过旋转矩阵把绝对位置信息融入自注意力，使内积自然包含相对位置依赖。RoPE 兼具相对位置编码的灵活性、可扩展到任意序列长度、且对线性注意力友好。论文从理论与实验证明 RoPE 在多项长文本任务上优于既有位置编码方法。

## 关键技术细节
- 核心：把每个维度对按位置角度做旋转（rotary），使 q·k 内积仅依赖相对位置 m-n。
- 优点：①相对位置感知；②序列长度可扩展（外推友好）；③与线性注意力（linear attention）兼容；④无需额外可学习参数。
- 实现简单：对 query/key 向量逐维做旋转变换即可。
- 影响：后被 LLaMA、PaLM、GLM、Qwen、Mistral 等广泛采用，是 2021 年最具影响力的架构改进之一。
- 作者 Jianlin Su（苏剑林）等，追一科技（Zhuiyi）。

## 原始链接
- url: https://arxiv.org/abs/2104.09864
- pdf_url: https://arxiv.org/pdf/2104.09864

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2104.09864.pdf
