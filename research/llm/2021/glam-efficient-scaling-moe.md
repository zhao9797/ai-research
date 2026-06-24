---
title: "GLaM: Efficient Scaling of Language Models with Mixture-of-Experts"
org: Google
country: US
date: 2021-12
type: paper
categories: [架构, AI infra, 预训练数据]
url: https://arxiv.org/abs/2112.06905
pdf_url: https://arxiv.org/pdf/2112.06905
github_url:
downloaded: [arxiv-2112.06905.pdf]
---

## 一句话定位
Google 的 GLaM：用稀疏激活 MoE 把模型扩到 1.2 万亿参数，但每 token 只激活约 97B，训练能耗仅为 GPT-3 的 1/3、推理 FLOPs 为其一半。

## 摘要（3-6 句）
GLaM（Generalist Language Model）使用稀疏激活的 Mixture-of-Experts 架构在扩大模型容量的同时大幅降低训练成本。最大的 GLaM 有 1.2 万亿总参数，约为 GPT-3 的 7 倍，但训练只消耗 GPT-3 约 1/3 的能量、推理只需一半的计算 FLOPs，在 29 个 NLP 任务上的 zero/one/few-shot 综合表现仍优于 GPT-3。

## 关键技术细节
- 总参数 1.2T，每 MoE 层 64 个专家（experts per layer）。
- 路由：每个 token 从 64 个专家中选 top-2（gating 选最相关的 2 个专家），输出送入上层。
- 激活参数 nact-params ≈ 97B（每 token 实际激活约 97 亿）。
- MoE 层与 Transformer 层交替；专家是独立的前馈网络（FFN）。
- 训练数据：1.6 万亿 tokens 的高质量语料（含不同来源数据集与混合权重 weight in mixture）。
- 训练成本：能耗为训练 GPT-3 的 1/3，推理 FLOPs 为 GPT-3 一半。
- 基于 GShard 思路的稀疏激活高效实现，TPU 上训练。

## 原始链接
- url: https://arxiv.org/abs/2112.06905
- pdf_url: https://arxiv.org/pdf/2112.06905

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2112.06905.pdf
