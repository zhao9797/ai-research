---
title: Collective Constitutional AI: Aligning a Language Model with Public Input
org: Anthropic
country: US
date: 2023-10
type: blog
categories: [后训练]
url: https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input
downloaded: [anthropic-collective-cai.html]
---

## 一句话定位
Anthropic 与 Collective Intelligence Project 合作，用公众投票产生的"集体宪法"训练模型，把 CAI 从"实验室写原则"推向"民主参与式对齐"。

## 摘要（3-6 句）
Collective Constitutional AI 探索让公众而非仅 Anthropic 员工来撰写模型对齐所依据的宪法原则。约 1000 名美国民众通过 Polis 平台提交与投票产生一部"公众宪法"，Anthropic 据此训练了一个模型，并与基于 Anthropic 自有宪法的模型对比。结果显示两模型在能力与安全上相当，但公众宪法模型在多项社会维度上偏见更低，对不同群体更公平。该工作是把民主流程引入 AI 对齐的早期一手实验，公开了流程、宪法差异与评测结论。

## 关键技术细节
- 方法：用 Polis 众包 + 投票，约 1000 名美国代表性参与者产出公众宪法原则集（与 Anthropic 宪法约半数重叠、半数不同）。
- 训练：用 CAI/RLAIF 流程，把"公众宪法"替换为对齐依据，训练对照模型。
- 评测：BBQ（偏见基准）等显示公众宪法模型偏见更低；语言能力、数学、有用/无害与原模型相当。
- 公开差异：公众宪法更强调可及性、客观平衡，少了一些 Anthropic 自有的细则表达。
- 意义：示范"参与式/民主式对齐"，回应对齐价值由谁决定的问题。

## 原始链接
- url: https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/anthropic-collective-cai.html
