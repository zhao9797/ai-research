---
title: "Hy3 preview (Hunyuan 3 preview)"
org: 腾讯混元 Tencent Hunyuan (Hy Team)
country: China
date: 2026-04
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://huggingface.co/tencent/Hy3-preview
pdf_url: ""
github_url: https://github.com/Tencent-Hunyuan/Hy3-preview
downloaded: [hunyuan-3-preview-modelcard.md]
---

## 一句话定位
腾讯混元 Hy3 preview，295B / 21B 激活的 MoE 大模型，是混元在"重建基础设施"上训练的第一个、也是迄今最强的模型，强化复杂推理、指令跟随、上下文学习、代码与 agent。

## 摘要
Hy3 preview（HuggingFace tencent 官方组织，createdAt 2026-04-13）是腾讯 Hy Team 研发的 295B 参数 MoE 模型，21B 激活 + 3.8B MTP 层参数。它是混元在重建基础设施（rebuilt infrastructure）上训练的首个模型，也是其迄今最强模型，在复杂推理、指令跟随、上下文学习、编码、agent 任务上显著提升。架构为 80 层（不含 MTP）+ 1 层 MTP；64 注意力头（GQA，8 KV 头，head dim 128）；hidden size 4096；中间维 13312；192 专家 top-8 激活；256K 上下文；词表 120832；BF16。代码与权重在 HF/ModelScope/GitHub 开源。同期混元还发布 Hy-MT2 翻译系列（2026-05）与 Hy-Embodied 具身/VLA 系列。

## 关键技术细节
- **规格**：295B 总参 / 21B 激活 / 3.8B MTP 层参（MoE）。
- **层数**：80 层（不含 MTP）+ 1 层 MTP。
- **注意力**：64 heads，GQA（8 KV heads，head dim 128）。
- **隐藏维**：hidden size 4096；intermediate size 13312。
- **专家**：192 experts，top-8 激活。
- **上下文**：256K；词表 120832；精度 BF16。
- **AI infra**：首个在"重建基础设施"上训练的模型；重建 RL 基础设施 + 更大规模训练任务带来 code/agent 最大增幅。
- **能力亮点**：FrontierScience-Olympiad、IMOAnswerBench 等 STEM；自建 CL-bench / CL-bench-Life 度量上下文学习；SWE-bench Verified、Terminal-Bench 2.0、BrowseComp、WideSearch 等 agent benchmark。
- **基座评测（节选，对比同级 Base）**：MATH 76.28、GSM8K 95.37、LiveCodeBench-v6 34.86、SuperGPQA 51.60、MMMLU 80.15（多项超 Kimi-K2/DeepSeek-V3/GLM-4.5 同级 Base，尽管激活参数仅 21B）。

## 原始链接
- url: https://huggingface.co/tencent/Hy3-preview
- github_url: https://github.com/Tencent-Hunyuan/Hy3-preview
- 官网: https://aistudio.tencent.com/

## 本地落盘文件
- ../../../sources/llm/2026/hunyuan-3-preview-modelcard.md
