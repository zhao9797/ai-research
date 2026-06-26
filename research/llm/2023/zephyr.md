---
title: "Zephyr: Direct Distillation of LM Alignment"
org: Hugging Face
country: US
date: 2023-10
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2310.16944
pdf_url: https://arxiv.org/pdf/2310.16944
github_url: https://github.com/huggingface/alignment-handbook
downloaded: [zephyr.pdf]
---

## 一句话定位
HuggingFace 用 dSFT+dDPO 蒸馏出 Zephyr-7B，无任何人工标注就超 Llama2-Chat-70B，DPO 实战标杆。

## 摘要
目标是产出对齐用户意图的小模型。先对大模型输出做 distilled SFT(dSFT)，再用 AI Feedback(AIF) 偏好数据做 distilled DPO(dDPO) 学对话模型，显著改善意图对齐。仅需数小时训练、微调中无需额外采样。Zephyr-7B 在 7B 级 chat 基准上 SOTA，无人工标注；MT-Bench 上超过最佳开源 RLHF 模型 Llama2-Chat-70B。

## 关键技术细节
- 底座：Mistral 7B。
- dSFT：用 UltraChat（GPT-3.5 合成多轮对话）做蒸馏式 SFT。
- dDPO：用 UltraFeedback（多个模型回复 + GPT-4 打分排序）构造偏好对，做 distilled DPO，无 RL、无人工标注。
- 训练：仅数小时，DPO 阶段无需在线采样。
- 评测：MT-Bench 7.34，超 Llama2-Chat-70B；AlpacaEval 领先同尺寸。
- 开源：alignment-handbook 全流程。

## 原始链接
- url: https://arxiv.org/abs/2310.16944
- pdf_url: https://arxiv.org/pdf/2310.16944
- github_url: https://github.com/huggingface/alignment-handbook

## 一手源存档（sources/）
- zephyr.pdf  （PDF 不入 git，走 HF bucket）
