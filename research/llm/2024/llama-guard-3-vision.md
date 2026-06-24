---
title: "Llama Guard 3 Vision: Safeguarding Human-AI Image Understanding Conversations"
org: Meta
country: US
date: 2024-11
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2411.10414
pdf_url: https://arxiv.org/pdf/2411.10414
github_url: https://github.com/meta-llama/PurpleLlama
downloaded: [2411.10414.pdf]
---

## 一句话定位
Llama Guard 3 Vision：基于 Llama 3.2-Vision 微调的多模态安全护栏，对含图像的人机对话做输入（prompt）与输出（response）内容分类。

## 摘要
Llama Guard 3 Vision 是一个基于多模态 LLM 的安全护栏，用于涉及图像理解的人机对话：既可对多模态 LLM 输入（prompt 分类）也可对输出（response 分类）做内容审核。不同于此前纯文本的 Llama Guard，它专为图像推理场景设计，优化用于检测有害的多模态（文本+图像）prompt 及对其的文本回复。基于 Llama 3.2-Vision 微调，在采用 MLCommons taxonomy 的内部基准上表现强劲，并测试了对抗攻击鲁棒性。作者认为它是为多模态人机对话构建更强内容审核工具的良好起点。

## 关键技术细节
- 基座：Llama 3.2-Vision（11B）微调。
- 任务：多模态 prompt 分类 + 文本 response 分类（safe/unsafe + 类别）。
- 分类体系：MLCommons hazard taxonomy（13 类，含新增的"选举/代码解释器滥用"等）。
- 鲁棒性：对 PGD 等对抗攻击做了评估。
- 发布：PurpleLlama 安全工具套件之一。

## 原始链接
- url: https://arxiv.org/abs/2411.10414
- pdf_url: https://arxiv.org/pdf/2411.10414
- github: https://github.com/meta-llama/PurpleLlama

## 本地落盘文件
- ../../../sources/llm/2024/2411.10414.pdf
