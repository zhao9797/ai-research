---
title: Language Models are Few-Shot Learners (GPT-3)
org: OpenAI
country: US
date: 2020-05
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2005.14165
pdf_url: https://arxiv.org/pdf/2005.14165
github_url:
downloaded: [arxiv-2005.14165.pdf]
---

## 一句话定位
GPT-3：1750 亿参数的自回归语言模型，证明纯规模扩展即可让模型在不更新权重的情况下通过 few-shot/one-shot/zero-shot 上下文学习完成大量 NLP 任务，是“大模型时代”的奠基论文。

## 摘要（3-6 句）
论文训练了 175B 参数的 GPT-3，比此前最大的非稀疏语言模型大 10 倍。模型在不做任何梯度更新或微调的情况下，仅通过文本提示中的少量示例（few-shot in-context learning）即可在翻译、问答、完形填空、推理等任务上取得强劲表现，部分任务接近或超过 SOTA 微调模型。论文系统研究了 zero/one/few-shot 三种设定随模型规模的变化趋势，并讨论了数据污染、偏见、能耗与误用风险。GPT-3 还能生成人类难以分辨真伪的新闻文章，引发对社会影响的讨论。

## 关键技术细节
- 架构：Transformer decoder，与 GPT-2 相同结构，但交替使用 dense 与 locally banded sparse attention（类似 Sparse Transformer）。
- 模型规模谱系（共 8 个模型）：最大模型 GPT-3 175B，参数 1750 亿；96 层（n_layers=96），隐藏维度 d_model=12288，注意力头 96 个（每头维度 128），上下文窗口 n_ctx=2048 tokens。
- 其他规模：125M / 350M / 760M / 1.3B / 2.7B / 6.7B / 13B / 175B。
- 训练数据：约 3000 亿 token，混合 Common Crawl（过滤后约 410B token，权重 60%）、WebText2（19B，22%）、Books1（12B，8%）、Books2（55B，8%）、Wikipedia（3B，3%）；高质量数据集采样权重高于其在语料中的占比。
- Common Crawl 经过基于与高质量参考语料相似度的过滤 + 模糊去重 + 与下游评测集去重。
- tokenizer：BPE，词表约 50257（沿用 GPT-2）。
- 训练算力：175B 模型训练约 3.14e23 FLOPs；论文给出各模型 petaflop/s-days 估算（175B 约 3640 petaflop/s-days）。
- 优化：Adam（β1=0.9, β2=0.95），梯度裁剪 1.0，cosine 学习率衰减，权重共享于 input/output embedding；混合精度训练；在 V100 GPU 集群（微软提供高带宽集群）上训练。
- batch size 随规模增大（175B 用 3.2M tokens 的批量），学习率随规模减小（175B 为 0.6e-4）。
- 后训练/对齐：本论文未做 RLHF；评测全部基于 in-context learning（zero/one/few-shot），few-shot 通常给 10-100 个示例填满 2048 上下文。

## 原始链接
- url: https://arxiv.org/abs/2005.14165
- pdf_url: https://arxiv.org/pdf/2005.14165

## 一手源存档（sources/）
- [arxiv-2005.14165.pdf](https://arxiv.org/pdf/2005.14165)  （arXiv 原文 PDF，不入 git）
