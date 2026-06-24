---
title: Mixtral of Experts
org: Mistral AI
country: EU
date: 2023-12
type: blog
categories: [架构, AI infra]
url: https://mistral.ai/news/mixtral-of-experts/
downloaded: [mixtral-blog.html]
---

## 一句话定位
Mistral 开源稀疏 MoE 模型 Mixtral 8x7B：46.7B 总参/12.9B 激活，质量超 Llama2-70B，2023 末最强开源 MoE。

## 摘要
Mistral AI 官方发布 Mixtral 8x7B 公告。Mixtral 是开放权重的高质量稀疏专家混合(SMoE)模型，Apache 2.0，优雅处理 32k token 上下文。多数基准超 Llama 2 70B、推理快 6x，并媲美/超过 GPT-3.5。是 decoder-only，FFN 从 8 组参数中按 token 选 2 组(router)，总参 46.7B 但每 token 仅用 12.9B。同时发布 Mixtral 8x7B Instruct。

## 关键技术细节
- 架构：稀疏 MoE，decoder-only；每层 FFN 含 8 个专家，router 每 token 选 top-2 专家加权合并。
- 参数：总 46.7B，每 token 激活 12.9B(速度/成本约等于 12.9B 稠密模型)。
- 上下文：32k token。
- 训练：在开放 Web 数据上预训，experts 与 router 同时训练；多语言(英/法/德/西/意)。
- 性能：多数基准超 Llama 2 70B、推理快 6x；媲美/超 GPT-3.5。
- Instruct 版：SFT + DPO，MT-Bench 8.30；Apache 2.0。
- 注：Mixtral 论文 arXiv 2401.04088 于 2024-01 发布，本条为 2023-12 官方公告博客。

## 原始链接
- url: https://mistral.ai/news/mixtral-of-experts/

## 本地落盘文件
- ../../../sources/llm/2023/mixtral-blog.html
