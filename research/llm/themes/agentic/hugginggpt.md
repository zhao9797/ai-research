---
title: "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face"
org: "Zhejiang University / Microsoft Research Asia"
country: China
date: 2023-03
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2303.17580
pdf_url: https://arxiv.org/pdf/2303.17580
github_url: https://github.com/microsoft/JARVIS
downloaded: [hugginggpt-2303.17580.pdf]
---

## 一句话定位
让 LLM 当"调度大脑"，把 Hugging Face 上成百上千个专家模型当工具，按"任务规划→模型选择→任务执行→结果汇总"四步编排，完成跨模态复杂任务。

## 摘要
HuggingGPT 用 ChatGPT 作为控制器(controller)来管理和调用 Hugging Face 社区的大量 AI 模型解决复杂多模态任务。流程四阶段：① 任务规划——把用户请求解析成结构化子任务序列；② 模型选择——按子任务描述从 HF 选择合适的专家模型；③ 任务执行——调用模型并整合结果；④ 响应生成——汇总各模型输出形成回复。借助语言作为通用接口，ChatGPT 得以连接视觉、语音等众多领域模型，覆盖语言/视觉/语音等多模态、跨领域任务。

## 关键技术细节
- 控制器：ChatGPT(GPT-3.5/GPT-4)，负责规划、选模、汇总。
- 工具库：Hugging Face Hub 上的开源专家模型（图像分类/检测/分割、ASR、TTS、文本生成等）。
- 四阶段流水线：Task Planning → Model Selection → Task Execution → Response Generation。
- 任务间依赖通过资源引用(如 <resource-1>)在子任务之间传递中间结果。
- 代号 JARVIS，开源于 microsoft/JARVIS；是"LLM 作为编排器调度模型即工具"的代表。

## 原始链接
- url: https://arxiv.org/abs/2303.17580
- pdf_url: https://arxiv.org/pdf/2303.17580
- github_url: https://github.com/microsoft/JARVIS

## 一手源存档（sources/）
- [hugginggpt-2303.17580.pdf](https://arxiv.org/pdf/2303.17580)  （arXiv 原文 PDF，不入 git）
