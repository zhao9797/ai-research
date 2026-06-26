---
title: gpt-oss-120b & gpt-oss-20b Model Card (OpenAI)
org: OpenAI
country: US
date: 2025-08
type: model-card
categories: [架构, 后训练, AI infra]
url: https://openai.com/index/gpt-oss-model-card/
pdf_url: https://cdn.openai.com/pdf/419b6906-9da6-406c-a19d-1bb078ac7637/oai_gpt-oss_model_card.pdf
github_url: https://github.com/openai/gpt-oss
downloaded: [files/gpt-oss-model-card.pdf]
---

## 一句话定位
OpenAI 2025-08-05 发布的首个开放权重大模型 gpt-oss（120b/20b）官方 model card，Apache 2.0 许可的 MoE 推理模型，可在单卡部署并支持可调推理强度与全链工具使用。

## 摘要
gpt-oss 是 OpenAI 自 GPT-2 以来首次发布开放权重模型：gpt-oss-120b 与 gpt-oss-20b，均为 MoE 架构、面向推理与 agentic 工具使用，Apache 2.0 许可。120b 可在单张 80GB GPU（MXFP4 量化）运行，20b 可在 16GB 端侧运行。支持 low/medium/high 三档 reasoning effort 与完整 CoT 输出。配套 arXiv 报告 2508.10925。

## 关键技术细节（带数字）
- gpt-oss-120b：116.83B 总参 / 每 token 5.13B 激活参；36 层，每 MoE 块 128 个专家，每 token top-4 激活；SwiGLU 门控。
- gpt-oss-20b：20.91B 总参 / 3.61B 激活参；24 层，每 MoE 块 32 个专家，top-4 激活。
- 注意力：banded window 与 full dense 交替（带宽 128 tokens）；每层 64 个 query head（head dim 64），GQA 8 个 KV head；RoPE + YaRN 扩展 dense 层至 131,072 上下文；含 attention sink/学习偏置。
- 量化：MoE 权重原生 MXFP4（4.25 bits/参数，占 90%+ 参数量）；120b 单卡 80GB GPU 运行，20b 16GB 端侧运行。
- 预训练：text-only 数据集"trillions of tokens"，知识截止 2024-06；NVIDIA H100 + PyTorch + Triton kernel；120b 训练 2.1M H100-hours，20b ≈10x 更少。
- 后训练：与 o3 类似的 CoT RL（含 variable-effort reasoning 训练 + agentic tool use）。
- 推理强度：low/medium/high 三档可调；harmony chat 格式（analysis/commentary/final 通道）。
- tokenizer：o200k_harmony（扩展 o200k，共 201,088 tokens）。
- 许可：Apache 2.0。发布日期 2025-08-05；配套 arXiv:2508.10925。

## 原始链接
- 官方页面：https://openai.com/index/gpt-oss-model-card/
- 官方 PDF：https://cdn.openai.com/pdf/419b6906-9da6-406c-a19d-1bb078ac7637/oai_gpt-oss_model_card.pdf
- arXiv：https://arxiv.org/abs/2508.10925
- GitHub：https://github.com/openai/gpt-oss

## 一手源存档（sources/）
- gpt-oss-model-card.pdf  （PDF 不入 git，走 HF bucket）
