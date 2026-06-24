---
title: "Solving math word problems with process- and outcome-based feedback"
org: DeepMind
country: UK
date: 2022-11
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2211.14275
pdf_url: https://arxiv.org/pdf/2211.14275
downloaded: [process-outcome-feedback.pdf]
---

## 一句话定位
首次在自然语言推理任务（GSM8K）上系统对比"过程监督（process-based）vs 结果监督（outcome-based）"的奠基论文，提出并量化了二者在最终答案错误率与推理过程错误率上的差异——后续 PRM / Math-Shepherd / o1 等过程奖励工作的概念源头。

## 摘要（3-6 句）
让 LM 生成推理步骤能提升许多推理任务表现；但超越 prompting 进入训练阶段后，关键问题是：该如何监督这类模型——监督最终结果（outcome-based），还是监督推理过程本身（process-based）？二者的差异不仅体现在最终答案错误上，更体现在推理错误上，而推理错误难以察觉、在教育等真实领域尤其有害。论文在 GSM8K 这一自然语言任务上做了首个过程 vs 结果监督的全面对比。发现：纯结果监督（outcome-based）能用更少的标注监督达到相近的最终答案错误率；但要得到正确的推理步骤，则必须使用过程监督，或使用"模拟过程反馈的学习型奖励模型"。总体上，把此前最佳结果从最终答案错误率 16.8% → 12.7%、并把"最终答案正确解中的推理错误率"从 14.0% → 3.4%。

## 关键技术细节
- 任务：GSM8K 小学数学应用题（自然语言推理基准），首个在 NL 任务上做 process vs outcome 全面对比。
- 两种监督定义：outcome-based 只监督最终答案是否正确；process-based 监督每一步推理是否正确。
- 核心发现 1：纯结果监督即可用更少标注达到与过程监督相近的最终答案准确率（final-answer error 相当）。
- 核心发现 2：要降低"推理过程错误"（即答案对但过程错的 trace），必须用过程监督，或用一个"模拟过程反馈的学习型奖励模型"（learned reward model emulating process feedback）——后者即后来 PRM（process reward model）的雏形。
- 量化结果：最终答案错误率 16.8% → 12.7%；在最终答案正确的解中，推理错误率 14.0% → 3.4%（约 4 倍降低）。
- 意义：明确区分 outcome reward 与 process reward，指出 outcome 监督会留下"对的答案、错的过程"的隐患，奠定后续 process reward model（Math-Shepherd、Let's Verify Step by Step）与 o1 类过程监督路线的理论动机。

## 原始链接
- url: https://arxiv.org/abs/2211.14275
- pdf_url: https://arxiv.org/pdf/2211.14275

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/process-outcome-feedback.pdf
