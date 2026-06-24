---
title: How Far Can Camels Go? (Tülu)
org: Allen Institute for AI (AI2)
country: US
date: 2023-06
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2306.04751
pdf_url: https://arxiv.org/pdf/2306.04751
github_url: https://github.com/allenai/open-instruct
downloaded: [tulu-camels.pdf]
---

## 一句话定位
AI2 系统横评 12 个开源指令数据集，发布 Tülu 模型与 open-instruct 框架，给开源后训练立基准。

## 摘要
本文横向评测在多种开源指令数据集上的 instruction tuning。提供 6.7B–65B 的指令微调模型，训练于 12 个数据集(从人工 OpenAssistant 到合成蒸馏 Alpaca)，用自动/模型/人类多维评测。提出 Tülu——融合多个高质量开源资源的最佳模型套件。发现没有单一数据集在所有维度最优；最佳模型平均达 ChatGPT 87%、GPT-4 73%。

## 关键技术细节
- 模型：6.7B/13B/30B/65B（基于 LLaMA），含全参微调 65B Tülu。
- 数据集：12 个——SuperNI、CoT、Flan V2、Dolly、OpenAssistant、Self-Instruct、Alpaca、Code-Alpaca、GPT4-Alpaca、Baize、ShareGPT 等。
- 评测维度：事实知识(MMLU)、推理(GSM8K/BBH)、多语言(TyDiQA)、代码(HumanEval)、开放指令(AlpacaEval/人评)。
- 关键发现：不同数据集激发不同能力，无单一最优；模型/人偏好评测无法反映 benchmark 暴露的能力差异。
- 结论：最佳模型平均达 ChatGPT 87%、GPT-4 73%，仍需更好底座+数据。
- 开源：models + code + open-instruct 评测框架。

## 原始链接
- url: https://arxiv.org/abs/2306.04751
- pdf_url: https://arxiv.org/pdf/2306.04751
- github_url: https://github.com/allenai/open-instruct

## 本地落盘文件
- ../../../sources/llm/2023/tulu-camels.pdf
