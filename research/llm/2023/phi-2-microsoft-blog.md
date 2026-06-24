---
title: "Phi-2: The surprising power of small language models"
org: Microsoft Research
country: US
date: 2023-12
type: blog
categories: [预训练数据]
url: https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/
downloaded: [phi-2-microsoft-blog.html]
---

## 一句话定位
微软 Phi-2 发布博客：2.7B 在 <13B 基础模型中 SOTA，教材级数据 + 知识迁移，96 张 A100 训 14 天。

## 摘要
微软研究院官方发布 Phi-2 的博客。Phi-2 是 2.7B 参数语言模型，在 <13B 基础模型中推理与语言理解 SOTA，部分基准甚至匹敌/超过最高 25x 大的模型。两大关键：(1)训练数据质量——教材级合成数据 + 精选高价值网络数据；(2)从 1.3B 的 Phi-1.5 做知识迁移(嵌入式扩展)以加速收敛。

## 关键技术细节
- 参数：2.7B；Transformer，下一词预测目标。
- 训练 token：1.4T，来自合成 + 网络数据(NLP 与代码)多次遍历。
- infra：96 张 A100 GPU，训练 14 天。
- 知识迁移：从 Phi-1.5(1.3B) 嵌入知识到 Phi-2(2.7B)，加速收敛、提升分数。
- 数据哲学：'textbook-quality' 数据 + 高教育价值/高质量网络数据筛选。
- 评测：在 <13B 基础模型中 BBH/常识/语言理解/数学/代码 SOTA；未做 RLHF/指令微调仍表现好(毒性更低)。

## 原始链接
- url: https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/

## 本地落盘文件
- ../../../sources/llm/2023/phi-2-microsoft-blog.html
