---
title: "DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models"
org: DeepSeek-AI
country: China
date: 2024-01
type: paper
categories: [架构]
url: https://arxiv.org/abs/2401.06066
pdf_url: https://arxiv.org/pdf/2401.06066
github_url: https://github.com/deepseek-ai/DeepSeek-MoE
downloaded: [deepseekmoe.pdf]
---

## 一句话定位
DeepSeekMoE 提出「细粒度专家切分 + 共享专家隔离」两大策略提升专家专业化，让 2B/16B MoE 用更少激活参数匹敌更大稠密模型，是 DeepSeek-V2/V3 MoE 架构的基础。

## 摘要（3-6 句）
传统 MoE 存在知识混杂和专家冗余问题。DeepSeekMoE 通过两点改进：(1) 细粒度专家切分——把每个专家拆得更小、同时激活更多专家，使专家组合数大幅增加，提升专业化；(2) 共享专家隔离——保留少量始终激活的共享专家承载通用知识，减少路由专家的冗余。DeepSeekMoE 2B 接近同激活参数的 GShard 2.9B；DeepSeekMoE 16B（2.8B 激活）匹敌 LLaMA2-7B，仅用约 40% 计算；并验证到 145B 规模。

## 关键技术细节
- 细粒度专家切分（fine-grained segmentation）：把专家 FFN 切小、相应增加激活专家数，组合空间指数级增大。
- 共享专家隔离（shared expert isolation）：N_s 个共享专家恒激活承载共有知识，其余为路由专家。
- 规模点：2B（接近 GShard 2.9B 但更省）、16B（2.8B 激活，约等于 LLaMA2-7B 而省约 60% 算力）、扩展验证到 145B。
- 负载均衡：expert-level + device-level balance loss。
- 是 DeepSeek-V2、DeepSeek-V3 的 MoE 架构原型。

## 原始链接
- url: https://arxiv.org/abs/2401.06066
- pdf_url: https://arxiv.org/pdf/2401.06066
- github_url: https://github.com/deepseek-ai/DeepSeek-MoE

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/deepseekmoe.pdf
