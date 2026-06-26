---
title: "Grok-1 open release"
org: xAI
country: US
date: 2024-03
type: github
categories: [架构]
url: https://github.com/xai-org/grok-1
pdf_url:
github_url: https://github.com/xai-org/grok-1
downloaded: [xai-grok-1-README.md]
---

## 一句话定位
xAI 开源 Grok-1 的权重与 JAX 推理代码：314B 参数的 8 专家 MoE（每 token 用 2），Apache 2.0，是 2024 年 3 月当时最大的开源权重模型。

## 摘要
2024-03-17 xAI 开源 Grok-1 基础模型（base，非微调）的权重与 JAX 示例代码（加载与推理）。Grok-1 是 314B 参数的 Mixture-of-Experts 模型（8 专家，每 token 用 2），以 Apache 2.0 许可发布。仓库提供权重下载（磁力链 / HuggingFace），并说明因模型巨大需要多 GPU 才能跑示例；仓库内 MoE 层实现为正确性验证而非效率优化。

## 关键技术细节
- 参数：314B（base）。
- 架构：MoE，8 专家、每 token 用 2 个专家。
- 层数：64 层。
- 注意力：48 个 query head、8 个 key/value head（GQA）。
- 嵌入维度：6,144。
- tokenizer：SentencePiece，词表 131,072。
- 位置编码：RoPE；支持激活分片与 8-bit 量化。
- 最大上下文：8,192 token。
- 许可：Apache 2.0；权重经磁力链/HuggingFace（xai-org/grok-1）分发。

## 原始链接
- url: https://github.com/xai-org/grok-1
- github: https://github.com/xai-org/grok-1
- weights: https://huggingface.co/xai-org/grok-1

## 一手源存档（sources/）
- [xai-grok-1-README.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/xai-grok-1-README.md)
