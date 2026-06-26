---
title: "Introducing DBRX: A New State-of-the-Art Open LLM"
org: Databricks (Mosaic Research)
country: US
date: 2024-03
type: blog
categories: [架构, AI infra, 预训练数据]
url: https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm
pdf_url:
github_url: https://github.com/databricks/dbrx
downloaded: [databricks-dbrx-blog.md]
---

## 一句话定位
DBRX 发布博客：细粒度 MoE 开源模型，132B 总参数 / 36B 激活，16 专家选 4（比 Mixtral/Grok 更细粒度），12T token 预训练。

## 摘要
2024-03-27 发布。DBRX 是 decoder-only Transformer，用 next-token 预测训练，采用细粒度 MoE 架构：132B 总参数、任意输入激活 36B，在 12T token 文本与代码上预训练。相比 Mixtral、Grok-1，DBRX 是细粒度的——用更多更小的专家：16 专家选 4（Mixtral/Grok 为 8 选 2），提供 65× 更多专家组合，提升质量。推理比 LLaMA2-70B 快至多 2×，总/激活参数约为 Grok-1 的 40%，在 Databricks Model Serving 上最高 150 tok/s/用户。训练 MoE 比训练同质量稠密模型 FLOP 效率高约 2×；整体配方比上一代 MPT 少近 4× 算力达同质量。

## 关键技术细节
- 架构：细粒度 MoE，16 专家选 top-4（vs Mixtral/Grok 8 选 2）；132B 总 / 36B 激活。
- 其他：RoPE、GLU、GQA；GPT-4 tokenizer（tiktoken）。
- 预训练：12T token（文本+代码）；32K 上下文；用课程学习（训练中调整数据混合）。
- 数据质量：估计比 MPT 训练数据 token-for-token 好至少 2×。
- 效率：推理较 LLaMA2-70B 快至多 2×；MoE 训练 FLOP 效率约 2×；整体比 MPT 少近 4× 算力。
- 发布：DBRX Base 与 DBRX Instruct，开放许可（Databricks Open Model License）。

## 原始链接
- url: https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm
- github: https://github.com/databricks/dbrx

## 一手源存档（sources/）
- [databricks-dbrx-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/databricks-dbrx-blog.md)
