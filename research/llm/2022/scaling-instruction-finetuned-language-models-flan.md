---
title: Scaling Instruction-Finetuned Language Models (Flan / Flan-PaLM)
org: Google Research
country: US
date: 2022-10
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2210.11416
pdf_url: https://arxiv.org/pdf/2210.11416
github_url: https://github.com/google-research/FLAN
downloaded: [flan-scaling.pdf]
---

## 一句话定位
系统研究指令微调的三个缩放维度（任务数、模型规模、是否含 CoT 数据），Flan-PaLM 540B 在 1.8K 任务上微调后大幅超越 PaLM。

## 摘要
将语言模型在大量以指令形式表述的数据集上微调，可提升性能与对未见任务的泛化。本文聚焦三方面：(1) 扩展任务数量，(2) 扩展模型规模，(3) 在思维链数据上微调。结果显示指令微调能在多种模型（PaLM、T5、U-PaLM）、多种提示设置（zero/few-shot、CoT）、多种基准（MMLU、BBH、TyDiQA、MGSM、开放生成）上大幅提升性能。Flan-PaLM 540B 在 1.8K 任务上微调，平均比 PaLM 540B 高 9.4%，五-shot MMLU 达 75.2% SOTA。公开 Flan-T5 检查点。

## 关键技术细节
- 任务数扩展到 1836 个（合并 Muffin、T0-SF、NIV2、CoT 等任务集合）。
- 关键创新：在微调集中混入约 9 个带 CoT 的推理数据集，使模型保留并提升 zero-shot CoT 推理能力。
- Flan-PaLM 540B：五-shot MMLU 75.2%（SOTA），平均比 PaLM 540B +9.4%。
- 公开 Flan-T5 系列（80M–11B）检查点，小模型 few-shot 性能可媲美更大模型（如 Flan-T5-XL 超过 PaLM 62B）。
- 证明指令微调与模型缩放正交、收益叠加；指令微调是低成本的通用增益手段。

## 原始链接
- url: https://arxiv.org/abs/2210.11416
- pdf_url: https://arxiv.org/pdf/2210.11416
- github_url: https://github.com/google-research/FLAN

## 一手源存档（sources/）
- flan-scaling.pdf  （PDF 不入 git，走 HF bucket）
