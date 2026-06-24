---
title: "Intern-S2-Preview（上海 AILab：35B 科学多模态，task scaling）"
org: 上海人工智能实验室 Shanghai AI Lab (InternLM)
country: China
date: 2026-06
type: model-card
categories: [架构, 后训练, 预训练数据, agentic训练]
url: https://huggingface.co/internlm/Intern-S2-Preview-FP8
github_url: https://github.com/InternLM/Intern-S1
downloaded: [intern-s2-preview-readme.md, intern-s2-preview-config.json]
---

## 一句话定位
35B 科学多模态基础模型，提出 **task scaling**（提升科学任务难度/多样性/覆盖面）：仅 35B 即在多项核心专业科学任务上**比肩万亿级 Intern-S1-Pro**，且响应更短、token 效率更高。

## 架构（config.json，model_type=intern_s2_preview / qwen3_5_moe_text）
- hidden 2048；**40 层**；16 注意力头 / 2 KV，head_dim 256；**256 专家，每 token 选 8**，moe_intermediate 512；MTP 1 层；vocab 251392；上下文 256K（262,144）；rope 1e7；**FP8** 权重。**从 Qwen3.5 续训**。

## 数据 / 训练（task scaling 全链）
- 在参数/数据 scaling 之外探索**任务 scaling**：把**数百个专业科学任务**从预训练贯通到 RL 的全链训练。
- 强化小分子结构的**空间建模** + **实值预测模块** → **首个兼具材料晶体结构生成与强通用能力的开源模型**。
- 升级**时序建模**：支持长、异构时间序列（10^0–10^6 点），如从地震信号检测 P 波/S 波。

## RL / 后训练
- **shared-weight MTP + KL loss**：降低训练/推理行为失配，显著提升 MTP accept 率与生成速度。
- **CoT 压缩**：在保推理能力前提下缩短响应，性能与效率双升（复杂数学上以更短响应超越万亿级 S1-Pro）。
- thinking 默认开启（agentic 任务不建议关）。

## agentic
- 较上一代显著增强科学工作流 agent 能力；可接入 OpenClaw / Hermes / Claude Code（OpenAI 兼容 + Anthropic 兼容网关；`--tool-call-parser interns2-preview`）。

## Benchmark
- 官方以图表披露（figs/performance.png）；用 OpenCompass + VLMEvalKit；文本推理 128K、多模态 64K 最大推理长度；效率图显示在复杂数学上 accuracy 高于 S1-Pro 且响应更短。

## AI infra / 部署
- LMDeploy / vLLM / SGLang；FP8；时序推理目前仅 LMDeploy 支持；采样 temp 0.8 / top_p 0.95 / top_k 50。

## 原始链接
- url: https://huggingface.co/internlm/Intern-S2-Preview-FP8 · github: https://github.com/InternLM/Intern-S1 · chat: https://chat.intern-ai.org.cn

## 本地落盘文件
- ../../../sources/llm/2026/intern-s2-preview-readme.md
- ../../../sources/llm/2026/intern-s2-preview-config.json
