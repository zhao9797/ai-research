---
title: "MiniCPM5-1B（MiniCPM5 系列首款，端侧 1B SOTA）"
org: 面壁智能 ModelBest / OpenBMB (清华 THUNLP)
country: China
date: 2026-05
type: model-card
categories: [架构, 预训练数据, 后训练, agentic训练]
url: https://huggingface.co/openbmb/MiniCPM5-1B
pdf_url: https://arxiv.org/pdf/2602.09003
github_url: https://github.com/OpenBMB/MiniCPM
downloaded: [minicpm5-readme.md, arxiv-2602.09003-ultradata.pdf, minicpm5-1b-config.json]
---

## 一句话定位
面壁智能 2026-05-19 发布的 **MiniCPM5 系列首款** MiniCPM5-1B —— 面向端侧/本地/资源受限场景的 dense 1B 模型，达到 1B 级开源 SOTA（七项均分 42.57 vs 同级最强 35.61），强在 agentic 工具调用、代码、竞赛数学；同一 checkpoint 支持 Think / No-Think 双模与原生长上下文。

## 摘要
MiniCPM5-1B 是 MiniCPM5 系列首个 checkpoint，定位本地助手、coding agent、tool-use 工作流与轻量推理。采用**标准 `LlamaForCausalLM` 架构**（无自定义 kernel、无需 fork 模型代码），主流推理引擎（transformers/vLLM/SGLang/llama.cpp/ollama/mlx）可直接加载。发布 Base / SFT / Instruct / GGUF / MLX 多版本，Apache-2.0。训练为 UltraData 分层数据管理（base→mid→post 三阶段）的全栈实践，后训练以 RL + OPD（on-policy distillation）两阶段推理 RL 为核心。

## 关键技术细节
- **架构（config.json）**：dense Transformer，`model_type=llama`；hidden 1536；**24 层**；FFN intermediate 4608；注意力 **16 头 / 2 KV 头（GQA）**，head_dim 128；vocab **130560**；**上下文 128K**（max_position 131072）；RoPE θ=5,000,000（无额外 scaling）；`tie_word_embeddings=false`；bf16。
- **数据 / 训练**：UltraData Tiered Data Management 全栈实践（arXiv 2602.09003），三阶段 base training → mid-training → post-training（沿袭面壁 UltraClean/UltraFineWeb 数据线 + WSD 路线，承接 MiniCPM4 体系）。
- **后训练（重点）**：**RL + OPD** 为核心 —— 在 math/code/instruction-following 上把均分 **↑16 分**，同时把触顶 max-tokens 的超长回复占比 **↓29 个百分点**；采用**两阶段 Reasoning RL** pipeline。同一权重内置 Think / No-Think 双模。
- **agentic / 工具调用**：emits XML-style tool calls，SGLang 内置 `minicpm5` parser 原生转 OpenAI 兼容 `tool_calls`（`--tool-call-parser minicpm5`）；官方提供 deploy / finetune 的 Cursor/Claude Code Agent Skills。
- **效果**：对比 LFM2.5-1.2B-Thinking、Qwen3-0.6B、Qwen3.5-0.8B 等同级，1B 级开源 SOTA；优势集中在 tool use、代码生成、难推理。
- **生态**：HF + ModelScope；变体 MiniCPM5-1B / -1B-SFT / -1B-Base / -1B-GGUF / -1B-MLX。

## 原始链接
- url: https://huggingface.co/openbmb/MiniCPM5-1B
- pdf_url (UltraData 数据方法): https://arxiv.org/abs/2602.09003
- github_url: https://github.com/OpenBMB/MiniCPM

## 本地落盘文件
- ../../../sources/llm/2026/minicpm5-readme.md
- ../../../sources/llm/2026/arxiv-2602.09003-ultradata.pdf
- ../../../sources/llm/2026/minicpm5-1b-config.json
