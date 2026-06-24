---
title: GLU Variants Improve Transformer
org: Google
country: US
date: 2020-02
type: paper
categories: [架构]
url: https://arxiv.org/abs/2002.05202
pdf_url: https://arxiv.org/pdf/2002.05202
github_url:
downloaded: [arxiv-2002.05202.pdf]
---

## 一句话定位
Noam Shazeer 提出在 Transformer 前馈层用门控线性单元变体（尤其 GEGLU/SwiGLU）替代 ReLU/GELU，带来稳定质量提升，后被 PaLM、LLaMA 等主流大模型广泛采用。

## 摘要（3-6 句）
论文系统比较了 Transformer FFN 中用各种 GLU（Gated Linear Unit）变体替换标准 ReLU/GELU 激活的效果，包括 GLU、GEGLU、SwiGLU、ReGLU、Bilinear 等。在 T5 的去噪预训练与多项下游迁移任务上，GLU 变体（尤其 GEGLU、SwiGLU）一致地优于基线 FFN，且额外计算开销很小。这一改进成为后续大模型 FFN 的事实标准之一。

## 关键技术细节
- GLU 形式：FFN(x) = (xW + b) ⊗ σ(xV + c)，即一路线性 × 一路门控激活，逐元素相乘。
- 变体：GLU(sigmoid 门)、GEGLU(GELU 门)、SwiGLU(Swish 门)、ReGLU(ReLU 门)、Bilinear(无激活)。
- 为保持参数量一致，GLU FFN 把隐藏维度按比例缩小（因引入第三个权重矩阵 V）。
- 实验：基于 T5 框架，在 C4 去噪预训练困惑度与 GLUE/SuperGLUE/SQuAD 等下游任务上，GEGLU/SwiGLU 一致领先。
- 影响：SwiGLU 后被 PaLM、LLaMA 等采用为默认 FFN。

## 原始链接
- url: https://arxiv.org/abs/2002.05202
- pdf_url: https://arxiv.org/pdf/2002.05202

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2002.05202.pdf
