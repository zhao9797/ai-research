---
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
org: "Meta AI (FAIR) / Universitat Pompeu Fabra"
country: US
date: 2023-02
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2302.04761
pdf_url: https://arxiv.org/pdf/2302.04761
github_url:
downloaded: [toolformer-2302.04761.pdf]
---

> 📄 主题索引条目 —— 完整六维精读见 [Toolformer: Language Models Can Teach Themselves to Use Tools](../../2023/toolformer.md)。

## 一句话定位
自监督地让 LM 学会调用外部 API：模型自己生成候选 API 调用、用"是否降低后续 token 困惑度"做过滤，再在增强语料上继续训练，从而内生工具使用能力。
