---
title: DeBERTa — Decoding-enhanced BERT with Disentangled Attention
org: Microsoft
country: US
date: 2020-06
type: paper
categories: [架构]
url: https://arxiv.org/abs/2006.03654
pdf_url: https://arxiv.org/pdf/2006.03654
github_url: https://github.com/microsoft/DeBERTa
downloaded: [arxiv-2006.03654.pdf]
---

## 一句话定位
微软 DeBERTa 用“解耦注意力”（内容与位置分开编码）+ 增强型掩码解码器改进 BERT/RoBERTa，是 2020 年编码器预训练架构的代表性进步，后续 1.5B 版本首次在 SuperGLUE 上超过人类基线。

## 摘要（3-6 句）
DeBERTa 引入两项关键改进：一是解耦注意力（disentangled attention），每个 token 用内容向量和相对位置向量两个向量表示，注意力权重由内容-内容、内容-位置等解耦项计算；二是增强型掩码解码器（enhanced mask decoder, EMD），在 softmax 前注入绝对位置信息以辅助掩码词预测。论文还提出尺度不变微调（SiFT）正则化。DeBERTa 用一半训练数据即超过 RoBERTa-large，在 MNLI、SQuAD、RACE 等多项 NLU 任务上刷新 SOTA。

## 关键技术细节
- 解耦注意力：token = 内容向量 + 相对位置向量；注意力得分由内容→内容、内容→位置、位置→内容三类项组成（去掉位置→位置项）。
- 增强型掩码解码器（EMD）：在最后预测层之前重新注入绝对位置，弥补相对位置编码丢失的绝对位置信息。
- SiFT（Scale-invariant Fine-Tuning）：对归一化后的词嵌入加扰动做对抗式正则，用于大模型微调。
- 规模：base/large；后续 DeBERTa-large (约 390M) 与 1.5B 版本（48 层）在 SuperGLUE 上 90.3 分，首次超过人类基线 89.8。
- 训练数据：约 78GB 文本（Wikipedia、BookCorpus、OpenWebText、STORIES、CC-News 等），词表 50K。
- 效率：用 RoBERTa 一半的训练数据即在多数任务上超过 RoBERTa-large。

## 原始链接
- url: https://arxiv.org/abs/2006.03654
- pdf_url: https://arxiv.org/pdf/2006.03654
- github_url: https://github.com/microsoft/DeBERTa

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2006.03654.pdf
