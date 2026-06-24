---
title: "Gemma 2: Improving Open Language Models at a Practical Size"
org: Google DeepMind
country: US
date: 2024-06
type: report
categories: [架构, 后训练]
url: https://arxiv.org/abs/2408.00118
pdf_url: https://arxiv.org/pdf/2408.00118
downloaded: [gemma2.pdf]
---

## 一句话定位
Gemma 2（2B/9B/27B）把交错局部-全局注意力、GQA、logit soft-capping 引入小开放模型，并用知识蒸馏训练 2B/9B，性能匹敌 2-3 倍大的模型。

## 摘要（3-6 句）
Gemma 2 是 Google DeepMind 轻量开放模型族，规模 2B 到 27B。它对 Transformer 做若干已知改造：交错局部-全局注意力（local-global attention，借鉴 Longformer）和分组查询注意力 (GQA)。2B 和 9B 模型用知识蒸馏（而非纯 next-token 预测）训练。结果在各自规模上最佳，甚至可与大 2-3 倍的模型竞争。所有模型对社区开放。

## 关键技术细节
- 交错局部-全局注意力：每隔一层用滑动窗口（局部，窗口 4096）+ 全局注意力，降低长上下文 KV 开销。
- GQA、RMSNorm（pre + post norm 双归一化）、GeGLU 激活。
- logit soft-capping：对 attention 与 final logits 做 tanh 软上限，稳定训练。
- 知识蒸馏：2B、9B 用更大教师模型的分布蒸馏训练，提升小模型样本效率。
- 规模：2B、9B、27B；27B 在 8192 token 上下文上训练。
- 发布 2024-06-27，开放权重。

## 原始链接
- url: https://arxiv.org/abs/2408.00118
- pdf_url: https://arxiv.org/pdf/2408.00118

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/gemma2.pdf
