---
title: "Query-Key Normalization for Transformers (QKNorm)"
org: 个人/学术合作（Alex Henry 等）
country: US
date: 2020-10
type: paper
categories: [架构]
url: https://arxiv.org/abs/2010.04245
pdf_url: https://arxiv.org/pdf/2010.04245
downloaded: [qknorm.pdf]
---

## 一句话定位
QKNorm（QK-Norm）在注意力打分前对每个 query / key 沿头维做 ℓ2 归一化，再乘一个可学习温度参数（取代除以 √d），让 softmax 不易任意饱和；成为后续大模型（Chameleon、OLMo-2、Gemma-2/3、Qwen3 等）稳定训练的常用技巧。

## 摘要（3-6 句）
低资源语言翻译是有挑战但有社会价值的 NLP 任务。沿着把 Transformer 归一化适配到该场景的近期工作，本文提出 QKNorm：修改注意力机制，使 softmax 不易任意饱和而不牺牲表达力。具体做法是在相乘前对每个 query 矩阵与 key 矩阵沿头维做 ℓ2 归一化，然后乘一个可学习参数放大，而不是除以嵌入维度的平方根。在 TED Talks 语料 + IWSLT'15 的 5 个低资源翻译对上，相对 SOTA 双语基线平均提升 0.928 BLEU。

## 关键技术细节
- 核心操作：对每个 head 的 q、k 沿 head 维做 ℓ2 归一化（单位向量），注意力打分 = g · (q̂ · k̂)，其中 g 为可学习的标量温度，取代标准的 1/√d_k 缩放。
- 效果机理：归一化把点积约束在 [-1,1]，再由 g 控制软化/锐化程度，避免 logits 过大导致 softmax 饱和、梯度消失，从而提升训练稳定性。
- 原始实证：5 个低资源翻译对（TED Talks + IWSLT'15）平均 +0.928 BLEU；论文 8 页，收录于 Findings of EMNLP 2020。
- 现代应用：被多款大模型采纳以稳定大规模训练 —— Chameleon（早融合混合模态训练稳定）、OLMo-2、Gemma-2/Gemma-3、Qwen3/Qwen3-Next 等均在注意力中引入 QK-Norm（多用 RMSNorm 形式的 QK 归一化）。
- 作者：Alex Henry、Prudhvi Raj Dachapally、Shubham Pawar、Yuxuan Chen。

## 原始链接
- url: https://arxiv.org/abs/2010.04245
- pdf_url: https://arxiv.org/pdf/2010.04245

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/qknorm.pdf
