---
title: Emergent Abilities of Large Language Models
org: Google / DeepMind / Stanford / UNC    country: US    date: 2022-06    type: paper
categories: [架构]
url: https://arxiv.org/abs/2206.07682    pdf_url: https://arxiv.org/pdf/2206.07682    github_url:
downloaded: [emergent-abilities.pdf]
---

## 一句话定位
系统提出"涌现能力"概念：某些能力在小模型上不存在、在大模型上突然出现，无法从小模型外推。

## 摘要
语言模型随规模增大不仅有量的提升，还出现新的质变能力。本文将"涌现能力"定义为：在小模型中不存在、但在大模型中出现的能力——即无法仅通过外推小模型性能来预测。论文综述了多种涌现能力（few-shot 提示任务、增强提示策略如 CoT/指令微调等），并讨论其对未来研究、能力预测与社会影响的意义。

## 关键技术细节
- 定义：能力 = emergent，当其在某临界规模（FLOPs/参数）以下接近随机、之上骤升。
- 给出多个涌现实例：3-digit 算术、跨语言 QA、IPA 音标转写、词义消歧等，多在 10^22–10^24 训练 FLOPs 区间涌现。
- 涌现的"增强提示"：CoT 推理、指令微调、program execution、self-consistency 等也仅在足够大模型上有效。
- 用 GPT-3、LaMDA、PaLM、Gopher、Chinchilla 等模型族横向对比规模阈值。
- 讨论涌现是否为度量假象（后续社区有争议），但奠定了"规模驱动能力相变"的叙事。

## 原始链接
- url: https://arxiv.org/abs/2206.07682
- pdf_url: https://arxiv.org/pdf/2206.07682

## 本地落盘文件
- ../../../sources/llm/2022/emergent-abilities.pdf
