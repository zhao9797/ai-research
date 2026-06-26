---
title: "gpt-oss-120b & gpt-oss-20b Model Card"
org: OpenAI
country: US
date: 2025-08
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://openai.com/index/gpt-oss-model-card/
pdf_url: https://arxiv.org/pdf/2508.10925
github_url: https://github.com/openai/gpt-oss
downloaded: [gpt-oss.pdf]
---

## 一句话定位
gpt-oss 是 OpenAI 时隔多年的开放权重模型（Apache 2.0），罕见地公开了其架构：MoE + 交替带状窗口/全密注意力 + attention sink + RoPE + YaRN，MoE 权重原生 MXFP4 量化，使 120B 装进单张 80GB GPU。

## 摘要（3-6 句）
gpt-oss-120b 与 gpt-oss-20b 是两个开放权重推理模型，Apache 2.0 许可。纯文本，面向 agentic 工作流，强指令遵循、工具使用（网搜、Python）、可调推理强度（reasoning effort）、完整可见 CoT 和结构化输出。120b 有 36 层、116.8B 总参 / 5.13B 激活；20b 有 24 层、20.9B 总参 / 3.6B 激活。MoE 权重用 MXFP4（每参数约 4.25 bit）量化，使 120b 可装单张 80GB GPU、20b 可在 16GB 系统运行。gpt-oss-120b 在 reasoning high 下接近 o4-mini、超过 o3-mini。

## 关键技术细节
- 规模：120b = 36 层 / 116.8B 总参 / 5.13B 激活；20b = 24 层 / 20.9B 总参 / 3.6B 激活；残差维度 2880。
- MoE：120b 每层 128 专家、20b 32 专家；每 token top-4 专家，softmax 仅在所选专家上加权；专家 FFN 用 gated SwiGLU。
- 注意力：交替「banded window（局部滑窗）」与「fully dense（全局）」模式（类 GPT-3）；带 attention sink（每头一个可学习的偏置 logit）；GQA。
- 位置/长上下文：RoPE + YaRN 扩展，支持长上下文（128K）。
- 归一化：每个 attention/MoE 块前用 RMSNorm；Pre-LN 放置（类 GPT-2）。
- 量化：MoE 权重原生 MXFP4（4.25 bit/参数，占 90%+ 参数），单卡部署友好。
- tokenizer：o200k_harmony（BPE，扩展自 GPT-4o/o4-mini 的 o200k，加 harmony chat 格式 token），开源于 TikToken。
- 后训练：面向推理与工具使用；variable effort reasoning（low/medium/high 推理强度）；agentic tool use；harmony chat 格式。

## 原始链接
- url: https://openai.com/index/gpt-oss-model-card/
- pdf_url: https://arxiv.org/pdf/2508.10925
- github_url: https://github.com/openai/gpt-oss

## 一手源存档（sources/）
- gpt-oss.pdf  （PDF 不入 git，走 HF bucket）
