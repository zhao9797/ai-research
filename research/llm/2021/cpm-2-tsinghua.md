---
title: "CPM-2: Large-scale Cost-effective Pre-trained Language Models"
org: 清华 (Tsinghua) / BAAI 智源
country: China
date: 2021-06
type: paper
categories: [AI infra, 架构, 后训练]
url: https://arxiv.org/abs/2106.10715
pdf_url: https://arxiv.org/pdf/2106.10715
github_url:
downloaded: [arxiv-2106.10715.pdf]
---

## 一句话定位
清华 + 智源的 CPM-2：面向"低成本"使用大模型的全栈技术——知识继承加速预训练、prompt tuning 降低微调成本、INFMOE 工具降低推理门槛；含 11B 中英双语稠密模型与 198B MoE 模型。

## 摘要（3-6 句）
CPM-2 针对大模型预训练、微调、推理三阶段的效率问题给出一套低成本技术：①知识继承（knowledge inheritance）复用已有模型加速预训练；②prompt tuning 大幅减少任务特定参数，降低微调与存储成本；③提出 INFMOE 推理工具，让有限算力也能跑大模型。发布 11B 中英双语模型与 198B MoE 模型。

## 关键技术细节
- 模型：11B 中英双语稠密模型 + 198B 参数 MoE 模型。
- 知识继承（knowledge inheritance）：用小模型/已有 PLM 初始化加速大模型预训练。
- prompt tuning：仅训练少量可学习 prompt，显著减少可训练参数与存储。
- INFMOE：面向单卡/有限资源的 MoE 推理框架，offload + 调度降低推理硬件门槛。
- 由清华 + 智源（BAAI）联合，属悟道（WuDao）/CPM 系列。

## 原始链接
- url: https://arxiv.org/abs/2106.10715
- pdf_url: https://arxiv.org/pdf/2106.10715

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2106.10715.pdf
