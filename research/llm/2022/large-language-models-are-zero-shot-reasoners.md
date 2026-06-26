---
title: Large Language Models are Zero-Shot Reasoners
org: Univ. of Tokyo / Google Research
country: Japan/US
date: 2022-05
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2205.11916
pdf_url: https://arxiv.org/pdf/2205.11916
github_url:
downloaded: [zero-shot-reasoners.pdf]
---

## 一句话定位
发现只需加一句"Let's think step by step"即可触发零样本思维链（Zero-shot-CoT），大幅提升大模型推理。

## 摘要
预训练大模型常被视为优秀的 few-shot 学习者。CoT 提示通过分步示例激发多步推理，在算术与符号推理上取得 SOTA。这些成功常归因于 few-shot 能力。本文表明 LLM 也是不错的 zero-shot 推理者：只需在每个答案前加上"Let's think step by step"。实验显示该 Zero-shot-CoT（用同一句模板）在多种基准推理任务上显著优于普通 zero-shot。

## 关键技术细节
- 方法：两阶段——先用"Let's think step by step"诱导推理链，再用第二个提示抽取最终答案。
- 无需任何示例（zero-shot），单一通用模板跨任务通用。
- 提升（InstructGPT/text-davinci-002、PaLM 540B）：MultiArith 17.7%→78.7%，GSM8K 10.4%→40.7% 等大幅跃升。
- 说明大模型推理能力是"潜在的"，可由极简提示触发，不必依赖任务特定 few-shot 示例。
- 与 few-shot CoT、self-consistency 共同构成 2022 提示推理三大支柱。

## 原始链接
- url: https://arxiv.org/abs/2205.11916
- pdf_url: https://arxiv.org/pdf/2205.11916

## 一手源存档（sources/）
- zero-shot-reasoners.pdf  （PDF 不入 git，走 HF bucket）
