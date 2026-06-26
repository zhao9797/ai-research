---
title: "XVERSE-13B: A multilingual large language model（官方 GitHub）"
org: 深圳元象科技（XVERSE Technology）
country: China
date: 2023-08
type: github
categories: [预训练数据, 架构, AI infra]
url: https://github.com/xverse-ai/XVERSE-13B
pdf_url:
github_url: https://github.com/xverse-ai/XVERSE-13B
downloaded: [xverse-13b-readme.md]
---

## 一句话定位
深圳元象 XVERSE-13B：支持 40+ 语言的多语言开源大模型，2023-11 的 v2 版本训练量增至 3.2T token 并加入工具调用，千卡集群峰值算力利用率 58.5%，是元象 2023 一手资料。

## 摘要（3-6 句）
XVERSE-13B 是深圳元象科技自研的多语言大语言模型，采用主流 Decoder-only 标准 Transformer，支持 8K 上下文（同尺寸最长）。初版（2023/08）训练 1.4T token；v2 版（2023/11）训练量增至 3.2T 并新增工具调用能力。构建覆盖中、英、俄、西等 40 多种语言的高质量多样化数据，精细设置各类型数据采样比例。2024/01 进一步发布支持 256K 上下文的 XVERSE-13B-256K。

## 关键技术细节
- 规模与结构：13B；Decoder-only 标准 Transformer；上下文 8K（同尺寸最长），后扩至 256K（2024/01）。
- 数据：v2 版 3.2 万亿 token（初版 1.4T → 3.2T）；涵盖 40+ 语言，精细设采样比例兼顾中英与多语。
- 分词：BPE，用上百 GB 语料训练，词表大小 100,534，原生支持多语言无需扩表。
- 训练框架/infra：自研高效算子、显存优化、并行调度、数据-计算-通信重叠、平台-框架协同；千卡集群峰值算力利用率（MFU）达 58.5%。
- 后训练：XVERSE-13B-Chat（指令精调，2023/08）；v2-Chat 对齐版；v2 新增工具调用能力。
- 部署：GGUF/GPTQ 量化，支持 llama.cpp、vLLM 在 macOS/Linux/Windows 推理。

## 原始链接
- url: https://github.com/xverse-ai/XVERSE-13B
- github_url: https://github.com/xverse-ai/XVERSE-13B

## 一手源存档（sources/）
- [xverse-13b-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/xverse-13b-readme.md)
