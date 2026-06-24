---
title: Self-Instruct: Aligning Language Models with Self-Generated Instructions
org: University of Washington / AI2
country: US
date: 2022-12
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2212.10560
pdf_url: https://arxiv.org/pdf/2212.10560
github_url: https://github.com/yizhongw/self-instruct
downloaded: [self-instruct.pdf]
---

## 一句话定位
Self-Instruct：让模型自举生成指令数据再自我微调，几乎零标注对齐，Alpaca 等无数后续工作的方法源头(ACL 2023)。

## 摘要
指令微调模型依赖人写指令数据，受限于数量/多样性/创造力。Self-Instruct 通过让预训练 LM 自举自身生成来提升指令遵循：流水线从 LM 生成指令、输入、输出样本，过滤无效或相似的再用于微调原模型。应用于原始 GPT-3，在 Super-NaturalInstructions 上较原模型绝对提升 33%，与用私有数据+人类标注训练的 InstructGPT-001 持平。仅留 5% 差距落后 InstructGPT-001。几乎无需标注。开源大型合成数据集。

## 关键技术细节
- 流程：从 175 条人写种子任务出发 → LM 生成新指令 → 判断是否分类任务 → 生成 input/output(input-first/output-first) → 过滤(ROUGE 去重、启发式过滤) → 回填任务池 → 微调原 LM。
- 规模：自举出约 52K 指令、82K 实例(应用于 GPT-3)。
- 结果：GPT-3 + Self-Instruct 在 SuperNI 绝对 +33%，≈ InstructGPT-001。
- 意义：Alpaca/Vicuna/WizardLM 等合成指令数据方法的鼻祖；几乎零人工标注。
- 注：v1 于 2022-12 上 arXiv，正式发表于 ACL 2023。

## 原始链接
- url: https://arxiv.org/abs/2212.10560
- pdf_url: https://arxiv.org/pdf/2212.10560
- github_url: https://github.com/yizhongw/self-instruct

## 本地落盘文件
- ../../../sources/llm/2023/self-instruct.pdf
