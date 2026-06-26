---
title: Image GPT — Generative Pretraining from Pixels
org: OpenAI
country: US
date: 2020-06
type: blog
categories: [架构, 预训练数据]
url: https://openai.com/index/image-gpt/
pdf_url: https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V2.pdf
github_url: https://github.com/openai/image-gpt
downloaded: [image-gpt-v2.pdf, openai-image-gpt.html]
---

## 一句话定位
把训练 GPT-2 的纯自回归像素预测搬到图像上（iGPT）：不看标签、不用卷积，仅靠预测下一个像素就学到强大的图像表征，证明序列 Transformer 的生成式预训练范式跨模态通用。

## 摘要（3-6 句）
OpenAI（2020-06-17 发布博客，对应 ICML 2020 论文）训练了与 GPT-2 同构的 Transformer，直接在像素序列上做自回归（或 BERT 式掩码）预训练，不引入任何 2D 图像结构先验。学到的特征经线性探针（linear probe）或微调后在 CIFAR-10、CIFAR-100、STL-10、ImageNet 等基准上达到与顶尖自监督方法可比的水平。结果表明：足够规模 + 足够数据下，同一套生成式序列建模方法可同时用于语言和图像，是“通用无监督学习”的证据。

## 关键技术细节
- 架构：GPT-2 同款 Transformer decoder，无卷积、无 2D 位置先验，把图像拉平为一维像素序列。
- 模型规模：iGPT-S/M/L/XL，最大 iGPT-XL 约 68 亿（6.8B）参数；iGPT-L 约 14 亿（1.4B）。
- 输入：为降低序列长度，先把图像下采样到低分辨率（如 32×32、48×48、64×64），并对颜色做聚类量化到 512 色的“调色板” token（9-bit 颜色码本）。
- 预训练目标：自回归预测下一像素（GPT 式），也实验了 BERT 式掩码目标。
- 评测：linear probe（冻结特征 + 线性分类）在 CIFAR-10 达 96.3%，ImageNet linear probe 达 72.0%（iGPT-L/XL）。
- 计算成本极高：作者明确指出像素级建模算力消耗巨大，仅作为方法可行性验证而非实用方案。
- 提供两版论文：ICML 2020 V1 与扩展 V2（cdn.openai.com）。

## 原始链接
- url: https://openai.com/index/image-gpt/
- pdf_url (V2): https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V2.pdf
- pdf_url (V1 ICML): https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V1_ICML.pdf
- github_url: https://github.com/openai/image-gpt

## 一手源存档（sources/）
- image-gpt-v2.pdf  （PDF 不入 git，走 HF bucket）
- [openai-image-gpt.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2020/openai-image-gpt.html)
