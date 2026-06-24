---
title: HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face
org: Microsoft Research / Zhejiang University
country: US
date: 2023-03
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2303.17580
pdf_url: https://arxiv.org/pdf/2303.17580
github_url: https://github.com/microsoft/JARVIS
downloaded: [hugginggpt.pdf]
---

## 一句话定位
用 ChatGPT 当“控制器”调度 HuggingFace 上海量专家模型，LLM-as-controller 的多模型编排范式。

## 摘要
主张用 LLM 作控制器管理现有 AI 模型解决复杂任务，语言作通用接口。HuggingGPT 用 ChatGPT 做任务规划：收到请求后规划子任务、按 HuggingFace 模型功能描述选模型、用所选模型执行子任务、再汇总结果。借 ChatGPT 强语言能力与 HF 海量模型，可跨模态/领域处理语言、视觉、语音等复杂任务，迈向 AGI。

## 关键技术细节
- 四阶段流水线：Task Planning(ChatGPT 解析请求成子任务) → Model Selection(按 HF 模型卡描述选模型) → Task Execution(调用推理) → Response Generation(汇总)。
- 控制器：ChatGPT(GPT-3.5)；专家模型：HuggingFace Hub 上的视觉/语音/NLP 模型。
- 接口：自然语言作为模型间通用协议。
- 代码即 JARVIS 项目(microsoft/JARVIS)。
- 意义：LLM 编排专家模型的早期代表，启发后续 agent/tool-routing 工作。

## 原始链接
- url: https://arxiv.org/abs/2303.17580
- pdf_url: https://arxiv.org/pdf/2303.17580
- github_url: https://github.com/microsoft/JARVIS

## 本地落盘文件
- ../../../sources/llm/2023/hugginggpt.pdf
