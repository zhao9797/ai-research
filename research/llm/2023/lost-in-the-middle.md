---
title: "Lost in the Middle: How Language Models Use Long Contexts"
org: Stanford University
country: US
date: 2023-07
type: paper
categories: [架构]
url: https://arxiv.org/abs/2307.03172
pdf_url: https://arxiv.org/pdf/2307.03172
downloaded: [lost-in-the-middle.pdf]
---

## 一句话定位
斯坦福揭示 LLM 长上下文“中间遗忘”现象：关键信息在首尾时最好用、在中间时性能骤降，长上下文评测奠基。

## 摘要
近期模型能接受长上下文输入，但对其能多好地利用长上下文所知甚少。分析模型在两类需识别上下文中相关信息的任务(多文档 QA、键值检索)上的表现，发现改变相关信息位置会显著影响性能：当相关信息位于输入开头或结尾时性能最高，需访问长上下文中部信息时性能显著下降——即便是显式长上下文模型。该分析有助理解 LLM 如何使用输入上下文，并为未来长上下文模型给出新评测协议。

## 关键技术细节
- 现象：U 形性能曲线——相关信息在开头/结尾时准确率高，在中间时骤降(“lost in the middle”)。
- 任务：多文档问答(把答案文档放在不同位置)、键值检索。
- 范围：GPT-3.5-Turbo、Claude、含显式长上下文版本均有此现象。
- 影响：扩大上下文窗口 ≠ 能用好；推动 retrieval 排序、位置感知与长上下文评测。
- 实践启示：把最重要信息放上下文首尾。

## 原始链接
- url: https://arxiv.org/abs/2307.03172
- pdf_url: https://arxiv.org/pdf/2307.03172

## 一手源存档（sources/）
- lost-in-the-middle.pdf  （PDF 不入 git，走 HF bucket）
