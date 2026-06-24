---
title: Mistral 7B
org: Mistral AI
country: EU
date: 2023-10
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2310.06825
pdf_url: https://arxiv.org/pdf/2310.06825
downloaded: [mistral-7b.pdf]
---

## 一句话定位
法国 Mistral 的开山之作，7B 超 Llama2-13B，靠 SWA+GQA 把小模型效率推到新高度，Apache 2.0。

## 摘要
Mistral 7B v0.1 是 7B 参数模型，在所有评测基准上超过 Llama 2 13B，在推理/数学/代码上超过 Llama 1 34B。用 Grouped-Query Attention(GQA) 加速推理，用 Sliding Window Attention(SWA) 以更低成本处理任意长序列。还发布指令微调版 Mistral 7B-Instruct，超过 Llama 2 13B-Chat。Apache 2.0 许可。

## 关键技术细节
- 参数：7.3B；架构 Transformer decoder。
- GQA：分组查询注意力，加快解码、降显存。
- SWA：滑动窗口注意力，窗口 4096；每层只看前 4096 个隐状态，借堆叠层实现远距感受野，理论注意力跨度 = 层数 × 窗口。
- 上下文：训练 8192；SWA 使其能处理任意长序列且推理成本线性。
- Rolling buffer KV cache：缓存固定为窗口大小，配合 FlashAttention/xFormers，16k 序列 4k 窗口下约 2x 提速。
- 评测：MMLU 上等效 3x 参数的 Llama2；全面超 Llama2-13B。

## 原始链接
- url: https://arxiv.org/abs/2310.06825
- pdf_url: https://arxiv.org/pdf/2310.06825

## 本地落盘文件
- ../../../sources/llm/2023/mistral-7b.pdf
