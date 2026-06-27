---
title: "DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models"
org: 深度求索（DeepSeek-AI）
country: China
date: 2024-01
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2401.06066
pdf_url: https://arxiv.org/pdf/2401.06066
github_url: https://github.com/deepseek-ai/DeepSeek-MoE
downloaded: [deepseekmoe.pdf]
---

## 一句话定位
提出"细粒度专家切分 + 共享专家隔离"的 MoE 架构，成为后来 DeepSeek-V2/V3 的 MoE 基础，是中国团队在 MoE 架构上的奠基性一手论文。（2024-01 发布，属 2023 工作的跨年报告。）

## 摘要（3-6 句）
针对传统 MoE（如 GShard top-K）专家专精不足的问题，DeepSeekMoE 提出两大策略：(1) 细粒度专家切分（将 N 个专家切成 mN 个、激活 mK 个），(2) 共享专家隔离（K_s 个常激活共享专家捕获公共知识）。2B 规模即可媲美 1.5× 参数与计算的 GShard 2.9B，并接近同参数 dense 上界。扩展到 16B 时仅用约 40% 计算量即媲美 LLaMA2-7B；初步扩到 145B 时仅用 28.5%（甚至 18.2%）计算量即媲美 DeepSeek 67B。

## 关键技术细节
- 核心架构创新：
  - Fine-Grained Expert Segmentation：保持参数与计算量不变，将每个专家 FFN 中间维切成 1/m，专家数变为 mN，激活数变为 mK，允许更灵活的激活组合。
  - Shared Expert Isolation：隔离 K_s 个始终激活的共享专家以压缩公共知识，减少 routed 专家间冗余。
- DeepSeekMoE 16B：28 层，总参约 16.4B、激活约 2.8B；每个 MoE 层 = 2 共享专家 + 64 routed 专家（每专家 0.25× 标准 FFN），每 token 走 2 共享 + 6/64 routed；maxLR 4.2e-4，词表 100K；2T token 训练；仅约 40% 计算即媲美 dense DeepSeek-7B 与 LLaMA2-7B；可单卡部署。
- DeepSeekMoE 145B（初步）：62 层，每 MoE 层 = 4 共享 + 128 routed（每专家 0.125× FFN），每 token 走 4 共享 + 12/128 routed；用专家并行（EP）；初步仅训练 245B token，batch 18M token、13000 步；仅 28.5%（甚至 18.2%）计算即媲美 DeepSeek 67B。
- DeepSeekMoE 2B：12 个零样本/少样本基准上超 GShard 2B，媲美 GShard 2.9B，近 dense 上界。
- DeepSeekMoE 145B（初步）：相比 GShard 持续占优；仅 28.5%（甚至 18.2%）计算量即媲美 DeepSeek 67B。
- 负载均衡：使用专家级 + 设备级负载均衡损失。
- 对齐：对 DeepSeekMoE 16B 成功做 SFT，chat 版媲美 DeepSeek-Chat-7B / LLaMA2-SFT-7B。
- 后续影响：直接成为 DeepSeek-V2（160 routed 专家）/ V3（256 routed + 1 shared）的 FFN 基础。

## 原始链接
- url: https://arxiv.org/abs/2401.06066
- pdf_url: https://arxiv.org/pdf/2401.06066
- github_url: https://github.com/deepseek-ai/DeepSeek-MoE

## 一手源存档（sources/）
- deepseekmoe.pdf  （PDF 不入 git，走 HF bucket）
