---
title: "Qwen3 Technical Report"
org: "阿里巴巴 通义千问 (Alibaba Qwen Team)"
country: China
date: 2025-05
type: report
categories: [架构, 后训练, agentic训练]
url: https://arxiv.org/abs/2505.09388
pdf_url: https://arxiv.org/pdf/2505.09388
github_url: https://github.com/QwenLM/Qwen3
downloaded: [qwen3-2505.09388.pdf]
---

## 一句话定位
通义 Qwen3 系列：把"思考/非思考"统一进单一模型并引入"思考预算"，0.6B-235B 全开源(Apache 2.0)，在 agent 任务上对标更大 MoE 与闭源模型，是开源 agentic 基座的主力之一。

## 摘要
Qwen3 是 Qwen 模型家族最新版本，含稠密与 MoE 两类架构、参数从 0.6B 到 235B。关键创新是把"思考模式"(复杂多步推理)与"非思考模式"(快速、上下文驱动响应)统一进单一框架，无需在 chat 优化模型(如 GPT-4o)与专用推理模型(如 QwQ-32B)间切换，可按用户查询/对话模板动态切换；并引入"思考预算(thinking budget)"机制，让用户在推理时自适应分配算力以平衡时延与性能。通过从旗舰模型蒸馏知识，大幅降低构建小模型所需算力同时保持竞争力。实证显示 Qwen3 在代码生成、数学推理、agent 任务等多基准达 SOTA，可与更大 MoE 及闭源模型竞争。多语言从 Qwen2.5 的 29 种扩到 119 种语言/方言。所有模型 Apache 2.0 开源。

## 关键技术细节
- 规模：稠密 0.6B/1.7B/4B/8B/14B/32B + MoE(Qwen3-30B-A3B、旗舰 Qwen3-235B-A22B，即 235B 总参/22B 激活)。
- 统一思考/非思考：单模型双模式，按 chat template 或查询动态切换。
- 思考预算(thinking budget)：推理期可设定思考 token 上限，自适应平衡延迟与精度。
- 训练：旗舰→小模型的强到弱蒸馏(strong-to-weak distillation)；预训练规模约 36T token(技术报告)。
- agentic：原生支持 function calling / 工具使用(配 Qwen-Agent 框架)，在 agent 任务基准表现强。
- 多语言：29→119 种语言/方言；全系 Apache 2.0 开源。

## 原始链接
- url: https://arxiv.org/abs/2505.09388
- pdf_url: https://arxiv.org/pdf/2505.09388
- github_url: https://github.com/QwenLM/Qwen3

## 一手源存档（sources/）
- [qwen3-2505.09388.pdf](https://arxiv.org/pdf/2505.09388)  （arXiv 原文 PDF，不入 git）
