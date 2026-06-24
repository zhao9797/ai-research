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

## 一句话定位
自监督地让 LM 学会调用外部 API：模型自己生成候选 API 调用、用"是否降低后续 token 困惑度"做过滤，再在增强语料上继续训练，从而内生工具使用能力。

## 摘要
Toolformer 提出一种自监督方式，让语言模型自主决定调用哪些 API、何时调用、传什么参数、如何把返回结果融入后续生成。方法仅需每个 API 少量人工示范：模型先在大量文本中采样可能插入 API 调用的位置与内容，执行调用，然后用一个基于困惑度的过滤准则（API 返回是否帮助预测后续 token）筛掉无用调用，最后在这份自标注、API 增强的语料上对模型做常规语言建模微调。Toolformer（基于 GPT-J 6.7B）在多种下游任务上大幅提升零样本表现，常超越更大模型，且不损失核心语言建模能力。

## 关键技术细节
- 基座：GPT-J 6.7B。
- 工具集：问答 API、计算器、维基搜索、机器翻译系统、日历等。
- 自监督数据构造三步：① 采样候选 API 调用位置/内容；② 执行 API 得到返回；③ 用自监督损失过滤——只保留"加入 API 返回后能显著降低未来 token 损失"的调用。
- 训练：在过滤后的 API 增强数据上做标准 LM 微调，无需任何人类标注的工具使用轨迹。
- 推理：生成到特殊标记时中断、实际调用 API、把结果插回上下文继续解码。
- 结果：在 LAMA、数学(ASDiv/SVAMP)、QA(WebQS/NQ)、时间类等任务零样本超过 GPT-3 175B 等更大模型，且常规语言建模困惑度基本不变。

## 原始链接
- url: https://arxiv.org/abs/2302.04761
- pdf_url: https://arxiv.org/pdf/2302.04761

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/toolformer-2302.04761.pdf
