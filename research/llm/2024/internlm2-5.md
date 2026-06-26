---
title: "InternLM2.5-7B-Chat (Model Card)"
org: 上海人工智能实验室 (Shanghai AI Laboratory)
country: 中国
date: 2024-07
type: model-card
categories: [后训练, 架构]
url: https://huggingface.co/internlm/internlm2_5-7b-chat
pdf_url:
github_url: https://github.com/InternLM/InternLM
downloaded: [files/internlm2-5-hf-readme.md]
---

## 一句话定位
书生·浦语 2.5（7B）2024-07 发布，主打卓越推理能力、1M 长上下文与更强工具调用（agent）。

## 摘要
InternLM2.5 官方 model card 强调三大特性：(1) 出色推理——数学推理超越 Llama3、Gemma2-9B 等同尺寸模型；(2) 1M 上下文窗口，在 1M 长文 "大海捞针" 中近乎完美，配合 LMDeploy 部署；(3) 更强工具使用——可从上百网页搜集信息做分析（配合 Lagent），指令跟随、工具选择与反思能力显著提升。

## 关键技术细节（带数字）
- 规模：InternLM2.5-7B（Base / Chat / Chat-1M）。
- 上下文：1M tokens（1M 长文 Needle-in-a-Haystack 近满分）。
- 推理：数学推理超越 Llama3-8B、Gemma2-9B 等同级模型。
- Agent：多步工具调用、网页信息聚合分析（Lagent 框架），指令/工具/反思能力增强。
- 部署：LMDeploy（支持 1M 上下文推理）。

## 原始链接
- HF model card: https://huggingface.co/internlm/internlm2_5-7b-chat
- GitHub: https://github.com/InternLM/InternLM

## 一手源存档（sources/）
- [internlm2-5-hf-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/internlm2-5-hf-readme.md)
