---
title: "TigerBot: An Open Multilingual Multitask LLM"
org: 虎博科技（TigerBot / TigerResearch）
country: China
date: 2023-12
type: paper
categories: [预训练数据, 架构, AI infra, 后训练]
url: https://arxiv.org/abs/2312.08688
pdf_url: https://arxiv.org/pdf/2312.08688
github_url: https://github.com/TigerResearch/TigerBot
downloaded: [tigerbot.pdf]
---

## 一句话定位
虎博 TigerBot：基于 Llama-2 与 BLOOM 续训的 7B–180B 多语言多任务模型族，在数据、训练算法、infra 与应用工具上做工程优化，中文较 SOTA 开源模型提升约 20%。

## 摘要（3-6 句）
TigerBot 是一组 7B/13B/70B/180B 的开源大模型（base + chat），从 Llama-2 与 BLOOM 出发，在数据、训练算法、基础设施与应用工具四方面进一步突破。相比 Llama-2 等 SOTA 开源模型，英文提升约 6%、中文提升约 20%。模型在主流学术与工业基准/榜单上领先，作者将其训练方法、数据与工具一并开源回馈社区。

## 关键技术细节
- 规模：7B / 13B / 70B / 180B（base 与 chat）；7B/13B 基于 Llama-2，180B 基于 BLOOM。
- 数据：清洗的多语言预训练语料（中英为主）；续训而非从零。
- 训练算法：在 SFT/对齐上引入若干工程改进（如指令完成率优化、安全过滤）。
- infra：针对续训与并行做工程优化（含 holistic 训练管线、稳定性优化）。
- tokenizer：扩充中文词表以提升中文压缩率与表现。
- 性能：相对 Llama-2，英文 +6%、中文 +20%；多榜单领先。
- 应用：开源配套应用工具（如长文本摘要、函数调用/插件等），面向落地。

## 原始链接
- url: https://arxiv.org/abs/2312.08688
- pdf_url: https://arxiv.org/pdf/2312.08688
- github_url: https://github.com/TigerResearch/TigerBot

## 本地落盘文件
- ../../../sources/llm/2023/tigerbot.pdf
