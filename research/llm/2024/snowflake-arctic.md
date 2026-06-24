---
title: "Snowflake Arctic: The Best LLM for Enterprise AI — Efficiently Intelligent, Truly Open"
org: Snowflake
country: US
date: 2024-04
type: blog
categories: [架构, AI infra]
url: https://www.snowflake.com/en/blog/arctic-open-efficient-foundation-language-models-snowflake/
pdf_url:
github_url:
downloaded: [snowflake-arctic-blog.md]
---

## 一句话定位
Snowflake Arctic 发布博客：独特的 Dense-MoE 混合架构（480B 总 / 17B 激活、128 细粒度专家 top-2），训练算力 <$2M（<3K GPU 周），主打企业智能（SQL/代码/指令遵循）。

## 摘要
2024-04-24 发布。Snowflake AI Research 推出 Arctic —— 面向企业的顶级 LLM，推进低成本训练与开放性。Arctic 用独特的 Dense-MoE 混合 Transformer 架构：把 10B 稠密 Transformer 与一个残差 128×3.66B 的 MoE MLP 结合，得到 480B 总参数、17B 激活参数（top-2 gating）。训练算力约 <$2M（<3K GPU 周），却在企业智能（编码 HumanEval+/MBPP+、SQL Spider、指令遵循 IFEval 的平均）上比肩甚至超过算力高得多的开源模型。Apache 2.0 开放，提供权重、训练 recipe（数据课程等）开源 cookbook。

## 关键技术细节
- 架构：Dense-MoE Hybrid = 10B 稠密 Transformer + 残差 128×3.66B MoE MLP；480B 总 / 17B 激活，top-2 gating。
- 训练效率：约 <$2M / <3K GPU 周（H100），比同算力开源模型更强。
- 架构-系统协同设计：用计算与 all-to-all 通信重叠隐藏 MoE 通信开销。
- 推理：17B 激活，batch=1 时显存读取比 Code-Llama 70B 少至多 4×、比 Mixtral 8x22B（44B 激活）少 2.5×。
- 企业智能：编码 + SQL + 指令遵循三项均衡强。
- 开放：Apache 2.0；权重 + 训练 cookbook（数据课程三阶段）。

## 原始链接
- url: https://www.snowflake.com/en/blog/arctic-open-efficient-foundation-language-models-snowflake/

## 本地落盘文件
- ../../../sources/llm/2024/snowflake-arctic-blog.md
