---
title: "Mistral Small 4 119B A6B（统一 Instruct + Reasoning + Devstral）"
org: Mistral AI
country: EU (France)
date: 2026-03
type: model-card
categories: [架构, 后训练, agentic训练]
url: https://huggingface.co/mistralai/Mistral-Small-4-119B-2603
downloaded: [mistral-small-4-readme.md, mistral-small-4-config.json]
---

## 一句话定位
把 **Instruct + Reasoning（原 Magistral）+ Devstral** 三家族统一进单一混合模型，可按需在「即时回复」与「推理」间切换；MoE 119B/6.5B，多模态输入，Apache-2.0（2026-03 发布，初版调研窗口前漏收）。

## 架构（config.json，model_type=mistral4 / Mistral3ForConditionalGeneration）
- **MoE**：128 路由专家 + 1 共享，**每 token 选 4 active**；**119B 总参 / 6.5B 激活**（名 "119B A6B"）。
- hidden 4096；**36 层**；32 注意力头 / 32 KV（**MHA**），qk_head_dim 128（nope 64 + rope 64）；moe_intermediate 2048；上下文 **256K**；rope_theta 1e4（+ 扩展）。
- **多模态输入**（图 + 文进、文字出）；24 种语言。

## 后训练 / 模式
- 统一三能力族；**reasoning_effort 每请求可调**：`none`（快，等同 Mistral-Small-3.2-24B-Instruct 风格）/ `high`（深推理，verbosity 近 Magistral）。
- 推理轨迹用 `[THINK]…[/THINK]` 标记；温度建议 high→0.7、none→0–0.7。
- （预训练数据/算力官方未在 card 披露。）

## 效率 / AI infra
- vs Mistral Small 3：延迟优化下端到端完成时间 **−40%**，吞吐优化下 **3× RPS**。
- 配套 **eagle head 投机解码** 版本 + **NVFP4 4-bit** 量化 checkpoint。
- vLLM（`--attention-backend FLASH_ATTN_MLA`、`--tool-call-parser mistral`、`--reasoning-parser mistral`、tp=2）/ llama.cpp(GGUF) / LM Studio / SGLang / transformers；Axolotl 微调。

## agentic
- best-in-class agentic：原生 function calling + JSON 输出；强 system prompt 遵从；面向 SWE 自动化与代码库探索（Devstral 血统）。

## Benchmark（数值读自官方图表）
- **vs 自家（带 reasoning）**：GPQA-Diamond 71.2 · MMLU-Pro 78 · AllenAI IFBench 48 · Arena Hard 58.3 · MMMU-Pro 60 —— 全面超 Small 3.2，逼近/部分超 Medium 3.1 与 Large 3。
- **vs Magistral（推理预代）**：AA LCR 71.2 · AIME25 83.8 · Collie 62.9 · LiveCodeBench 63.6（接近 Magistral Medium 1.2）。
- **vs 外部（Score @ 输出长度，reasoning 模式，"短输出"是卖点）**：
  - AA LCR：Mistral **72 @1.6K 字符** vs GPT-OSS-120B 51 @2.5K · Claude Haiku 80 @2.7K · Qwen3-Next-80B 75 @5.8K · Qwen3.5-122B 84 @5.7K（同档分数下输出最短）。
  - LiveCodeBench：Mistral **64 @4.7K** vs GPT-OSS-120B 63 @23.6K（分数胜且输出仅 1/5）· Qwen3.5-122B 74 @20.9K。
  - AIME25：Mistral 84 @27.9K vs GPT-OSS-120B 89 @14.9K · Qwen3.5-122B 93 @26.4K（此项略低于 GPT-OSS）。

## 原始链接
- url: https://huggingface.co/mistralai/Mistral-Small-4-119B-2603 （另：-eagle 投机解码 / -NVFP4 量化）

## 本地落盘文件
- ../../../sources/llm/2026/mistral-small-4-readme.md
- ../../../sources/llm/2026/mistral-small-4-config.json
