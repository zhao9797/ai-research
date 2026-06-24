---
title: "Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone"
org: Microsoft
country: US
date: 2024-04
type: report
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2404.14219
pdf_url: https://arxiv.org/pdf/2404.14219
github_url:
downloaded: [2404.14219.pdf]
---

## 一句话定位
Phi-3 技术报告：用高度过滤的网页 + 合成数据（"data optimal regime"）训练的小模型，phi-3-mini 3.8B（3072 hidden/32 层/32 头）可跑在手机上却比肩 Mixtral 8x7B / GPT-3.5；含 phi-3-small/medium 与 phi-3.5 系列（MoE + Vision）。

## 摘要
phi-3-mini 为 3.8B 参数、训练 3.3T token 的模型，整体性能比肩 Mixtral 8x7B 与 GPT-3.5（MMLU 69%、MT-bench 8.38），却小到可部署在手机上。训练集是 phi-2 数据的放大版，由高度过滤的公开网页数据与合成数据组成。还给出 7B（phi-3-small）与 14B（phi-3-medium）训练 4.8T token 的结果（MMLU 75%/78%）。phi-3.5 系列含 phi-3.5-mini、phi-3.5-MoE、phi-3.5-Vision。

## 关键技术细节
- phi-3-mini（3.8B）：decoder-only Transformer，hidden 3072、32 头、32 层；默认 context 4K（经 LongRope 扩到 128K）；与 Llama-2 同 tokenizer、词表 32064；bfloat16 训练 3.3T token；MMLU 69%、MT-bench 8.38；4-bit 量化约 1.8GB 可手机本地运行。
- phi-3-small（7B）：hidden 4096、32 头、32 层；交替 dense attention 与 blocksparse attention 层（优化 KV cache + 长上下文检索）；GQA；tiktoken tokenizer、词表 100352；默认 context 8192；GEGLU 激活 + muP（小 proxy 调超参再迁移）；训 4.8T token；MMLU 75%。
- phi-3-medium（14B）：40 头、40 层；与 phi-3-mini 同 tokenizer/架构（词表 32064）；训 4.8T token（略多 epoch）；MMLU 78%。
- 数据哲学："data optimal regime" —— 重过滤网页 + 合成数据（教科书式质量），而非单纯堆 token。
- phi-3.5-MoE：16×3.8B 专家、每 token 选 2、6.6B 活跃参数、42B 总参；用 SparseMixer 训练；比肩 Gemini-1.5-Flash、GPT-4o-mini。
- phi-3.5-Vision：4.2B，由 phi-3.5-mini 派生。
- 长上下文/多语言：LongRope 把上限从 4K 扩到 128K 且不损 4K 任务性能。

## 原始链接
- url: https://arxiv.org/abs/2404.14219
- pdf_url: https://arxiv.org/pdf/2404.14219

## 本地落盘文件
- ../../../sources/llm/2024/2404.14219.pdf
