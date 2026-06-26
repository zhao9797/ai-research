---
title: DeepSeek Open Infra Index — Production-tested AI Infrastructure Tools
org: DeepSeek-AI
country: China
date: 2025-02
type: github
categories: [AI infra]
url: https://github.com/deepseek-ai/open-infra-index
github_url: https://github.com/deepseek-ai/open-infra-index
downloaded: [open-infra-index-readme.md]
---

## 一句话定位
DeepSeek 2025 年「开源周」（Open Source Week）的总索引仓库，汇总其生产验证的 AI infra 工具（FlashMLA、DeepEP、DeepGEMM、DualPipe、3FS 等）及 V3/R1 推理系统的 profile 数据。

## 摘要（3-6 句）
2025 年 2 月最后一周，DeepSeek 连续开源 5 个生产级 infra 项目（开源周）：第 1 天 FlashMLA（MLA 解码 kernel）、第 2 天 DeepEP（MoE 专家并行通信库）、第 3 天 DeepGEMM（FP8 GEMM）、第 4 天 DualPipe + EPLB（双向流水 + 专家负载均衡）+ profile-data、第 5 天 3FS + smallpond。本仓库是这些工具的统一入口与说明，并附带 DeepSeek-V3/R1 推理系统的 one-more-thing 概述（大规模 EP 跨节点部署、PD 分离、计算通信重叠）。它是理解 DeepSeek 全栈 infra 的官方索引。

## 关键技术细节
- 开源周 5 天清单：FlashMLA / DeepEP / DeepGEMM / DualPipe(+EPLB+profile-data) / 3FS(+smallpond)。
- EPLB：Expert-Parallel Load Balancer，含冗余专家与启发式打包，缓解 MoE 推理负载不均。
- profile-data：用 PyTorch profiler 记录的 V3 训练/推理 计算-通信重叠时间线（DualPipe、prefill/decode EP）。
- V3/R1 推理系统披露：prefill 阶段 EP32+TP+DP、decode 阶段 EP144 大规模专家并行、PD 分离、双 micro-batch 重叠通信。

## 原始链接
- url: https://github.com/deepseek-ai/open-infra-index
- github_url: https://github.com/deepseek-ai/open-infra-index

## 一手源存档（sources/）
- [open-infra-index-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/open-infra-index-readme.md)
