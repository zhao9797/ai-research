---
title: GPT-4 Technical Report
org: OpenAI
country: US
date: 2023-03
type: paper
categories: [预训练数据, 架构, AI infra, 后训练]
url: https://arxiv.org/abs/2303.08774
pdf_url: https://arxiv.org/pdf/2303.08774
downloaded: [gpt-4-technical-report.pdf]
---

## 一句话定位
OpenAI 旗舰多模态大模型 GPT-4 的官方技术报告，刻意不披露架构/数据/算力细节，重点讲可预测扩展与对齐。

## 摘要
GPT-4 是可接受图文输入、输出文本的大规模多模态 Transformer。在多项专业与学术考试上达人类水平（模拟律考成绩约前 10%）。基于下一 token 预测预训练，后训练对齐过程提升事实性与遵循度。核心是构建在大范围尺度上可预测的基础设施与优化方法。

## 关键技术细节
- 架构：Transformer 自回归，预训练目标为下一 token 预测；具体层数/隐藏维度/参数量官方明确**不披露**（出于竞争与安全考量）。
- 多模态：支持图像+文本输入，输出文本。
- 可预测扩展（infra 核心）：用不超过 GPT-4 算力 1/1000 的小模型，准确预测 GPT-4 部分性能（如最终损失、HumanEval 通过率），实现 loss/能力的提前外推。
- 后训练：RLHF 对齐；提升 factuality 和对期望行为的遵循。
- 评测：模拟律考前 10%，多项学术/专业基准接近人类；MMLU 等大幅领先 GPT-3.5。
- 训练数据/token 数/GPU 卡时/上下文长度：报告均**未披露**具体数字（这是该报告的标志性特征）。

## 原始链接
- url: https://arxiv.org/abs/2303.08774
- pdf_url: https://arxiv.org/pdf/2303.08774

## 一手源存档（sources/）
- gpt-4-technical-report.pdf  （PDF 不入 git，走 HF bucket）
