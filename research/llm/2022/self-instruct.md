---
title: "Self-Instruct: Aligning Language Models with Self-Generated Instructions"
org: Univ. of Washington / AllenAI 等
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
Self-Instruct：让模型自举生成指令-输入-输出数据来微调自己，几乎不用人工标注即逼近 InstructGPT-001，催生 Alpaca 等开源指令数据范式。

## 摘要
指令微调模型能 zero-shot 泛化到新任务，但高度依赖数量、多样性、创意有限的人工指令数据，限制了泛化。Self-Instruct 框架通过模型自身生成来 bootstrap 指令遵循能力：用语言模型生成指令、输入、输出样本，过滤无效或过于相似者，再用其微调原模型。把方法用于原始 GPT-3，在 Super-NaturalInstructions 上获得 33% 绝对提升，与 InstructGPT-001 相当——而后者用了私有人工标注。

## 关键技术细节
- 流程：从 175 条人工种子任务出发 → 用 GPT-3 生成新指令 → 生成对应实例（input/output）→ ROUGE 相似度过滤去重 → 用约 52K 自动生成指令数据微调 GPT-3。
- 结果：在 Super-NaturalInstructions 上比原 GPT-3 提升 33% 绝对值，与 InstructGPT-001 持平。
- 几乎零人工标注（仅 175 种子 + 少量人工验证），极大降低指令数据获取成本。
- 直接启发 Stanford Alpaca（用 text-davinci-003 self-instruct 生成数据微调 LLaMA）等开源对齐浪潮。
- 公开 52K 指令数据与代码。

## 原始链接
- url: https://arxiv.org/abs/2212.10560
- pdf_url: https://arxiv.org/pdf/2212.10560
- github_url: https://github.com/yizhongw/self-instruct

## 一手源存档（sources/）
- self-instruct.pdf  （PDF 不入 git，走 HF bucket）
