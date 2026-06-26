---
title: "The Jamba 1.5 Open Model Family: The Most Powerful and Efficient Long Context Models"
org: AI21 Labs
country: US
date: 2024-08
type: blog
categories: [架构, AI infra]
url: https://www.ai21.com/blog/announcing-jamba-model-family/
pdf_url: https://arxiv.org/pdf/2408.12570
github_url:
downloaded: [ai21-jamba-1-5-blog.md, 2408.12570.pdf]
---

## 一句话定位
Jamba 1.5（Mini + Large）发布博客：首次把非 Transformer（SSM-Transformer 混合）模型成功扩展到市场领先质量，256K 有效上下文 + 自研 ExpertsInt8 量化。

## 摘要
2024-08-22 发布 Jamba 1.5 Mini 与 Jamba 1.5 Large，构建于 AI21 的 SSM-Transformer 混合架构。是首次把非 Transformer 模型扩展到市场领先质量与强度。256K 有效上下文窗口（市场最长之一），长上下文上最高快 2.5×、同级各上下文长度最快。Jamba 1.5 Mini 以 Arena Hard 46.1 成为同级最强开放模型（超 Mixtral 8x22B、Command-R+）；Jamba 1.5 Large 65.4，超过 Llama 3.1 70B 与 405B。配套提出 ExpertsInt8 量化以在 8×80GB GPU 上服务 Large。

## 关键技术细节
- 架构：Mamba(SSM) + Transformer 混合 + MoE。
- Mini：12B 激活 / 52B 总参数；Large：94B 激活 / 398B 总参数。
- 上下文：256K（公开模型中有效长上下文最长之一）。
- 量化：自研 ExpertsInt8（MoE 与 MLP 权重 INT8），Large 可在单节点 8×80GB GPU 服务 256K 上下文。
- 性能：Large Arena Hard 65.4 超 Llama 3.1 405B；长上下文最高 2.5× 速度。
- 许可：Jamba Open Model License；权重在 HuggingFace 开放。

## 原始链接
- url: https://www.ai21.com/blog/announcing-jamba-model-family/
- 研究页: https://www.ai21.com/research/jamba-1-5-hybrid-transformer-mamba-models-at-scale/
- paper: https://arxiv.org/abs/2408.12570

## 一手源存档（sources/）
- [ai21-jamba-1-5-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/ai21-jamba-1-5-blog.md)
- [2408.12570.pdf](https://arxiv.org/pdf/2408.12570)  （arXiv 原文 PDF，不入 git）
