---
title: Pangu Pro MoE - Mixture of Grouped Experts for Efficient Sparsity
org: 华为 (Huawei) 盘古
country: China
date: 2025-05
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2505.21411
pdf_url: https://arxiv.org/pdf/2505.21411
github_url:
downloaded: [pangu-pro-moe.pdf]
---

## 一句话定位
华为提出 MoGE（分组专家混合）：把专家等分成组、约束每 token 在每组内激活等量专家，从架构层面天然均衡多设备负载；据此构建 Pangu Pro MoE 72B 总参 / 16B 激活，针对昇腾 300I Duo / 800I A2 优化，推理 1148 tokens/s·卡（投机解码 1528），超 GLM-Z1-32B、Qwen3-32B。arXiv 2505.21411，发布 2025-05-27。

## 摘要
常规 Top-K MoE 存在专家激活不均：少数专家被频繁选中，多设备并行时"最忙设备"拖慢整体训练/推理。论文提出 Mixture of Grouped Experts (MoGE)：选专家时先把 N 个专家等分为 M 组（每组通常映射到一台设备），用全局 softmax router 打分后在每组内做 Top-K′ 选择，保证每组激活专家数相同，从而各设备计算负载天然均衡。基于 MoGE 在昇腾上构建 Pangu Pro MoE（72B 总参 / 16B 激活），配置经大量系统仿真针对昇腾 300I Duo 与 800I A2 优化，并辅以 hierarchical & hybrid 并行、量化压缩、自研 MulAttention / SwiftGMM 算子。

## 关键技术细节
- 架构创新：MoGE（Mixture of Grouped Experts），N 专家等分 M 组、组内 Top-K′ 选择，跨设备负载天然均衡。
- 配置（Table 1）：词表 153,376；hidden size 5120；intermediate size 1344；query heads 40、KV heads 8（GQA）、head size 128；48 层；路由专家 64、激活专家 8、共享专家 4；激活参数 16.50B、总参数 71.99B。
- 注意力/归一化：Group-Query Attention + RMSNorm。
- 预训练：13T tokens（同一 tokenizer，词表 153,376，domain-aware 词表策略）；4K 集群训练。
- 推理性能：昇腾 800I A2 上 1148 tokens/s·卡，投机解码可提升至 1528 tokens/s·卡，优于同档 32B / 72B dense 模型；昇腾 300I Duo 上有优异性价比。
- 系统优化：hierarchical & hybrid 并行 + 通信策略（与昇腾互联拓扑协同设计）；shared experts 走 TP8；量化压缩；自研 MulAttention / SwiftGMM 高性能算子。
- 定位：sub-100B 总参档领先开源模型，超 GLM-Z1-32B、Qwen3-32B。

## 原始链接
- url: https://arxiv.org/abs/2505.21411
- pdf_url: https://arxiv.org/pdf/2505.21411
- code: https://gitcode.com/ascend-tribe/pangu-pro-moe

## 本地落盘文件
- ../../../sources/llm/2025/pangu-pro-moe.pdf
