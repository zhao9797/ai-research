---
title: "Kimi K2: Open Agentic Intelligence"
org: "Moonshot AI (月之暗面 / Kimi Team)"
country: China
date: 2025-07
type: report
categories: [预训练数据, 架构, 后训练, agentic训练, AI infra]
url: https://arxiv.org/abs/2507.20534
pdf_url: https://arxiv.org/pdf/2507.20534
github_url: https://github.com/MoonshotAI/Kimi-K2
downloaded: [kimi-k2-2507.20534.pdf]
---

## 一句话定位
1T 参数/32B 激活的开源 MoE，专为 agentic 智能打造：MuonClip 优化器(QK-clip 解决训练不稳)零 loss spike 预训练 15.5T token，配大规模 agentic 数据合成 + 联合 RL，在 SWE-bench Verified/Tau2-Bench 等 agentic 基准领跑开源。

## 摘要
Kimi K2 是 32B 激活、1T 总参的 MoE 大模型。提出 MuonClip 优化器——在 Muon 基础上加 QK-clip 技术解决训练不稳，同时保留 Muon 的 token 效率优势。基于 MuonClip，K2 在 15.5T token 上预训练且零 loss spike。后训练采用多阶段流程，重点是大规模 agentic 数据合成管线与联合强化学习阶段——模型通过与真实/合成环境交互提升能力。K2 在开源非思考(non-thinking)模型中达 SOTA，尤擅 agentic 能力：Tau2-Bench 66.1、ACEBench(En) 76.5、SWE-Bench Verified 65.8、SWE-Bench Multilingual 47.3，超过多数开闭源基线；编码/数学/推理也强(LiveCodeBench v6 53.7、AIME 2025 49.5、GPQA-Diamond 75.1、OJBench 27.1)，均不用扩展思考。开源 base 与 post-trained 检查点。

## 关键技术细节
- 架构：MoE，1T 总参 / 32B 激活参数。
- 优化器 MuonClip：Muon + QK-clip(裁剪 attention 的 query/key 以防注意力 logit 爆炸)，解决大规模训练不稳；预训练 15.5T token 零 loss spike。
- 后训练：① 大规模 agentic 数据合成管线(自动生成工具使用/多步任务轨迹)；② 联合 RL(与真实+合成环境交互的强化学习)。
- 模式：non-thinking(不强制长思考)即取得强 agentic/coding 成绩。
- agentic 基准：Tau2-Bench 66.1、ACEBench(En) 76.5、SWE-Bench Verified 65.8、SWE-Bench Multilingual 47.3。
- 通用：LiveCodeBench v6 53.7、AIME 2025 49.5、GPQA-Diamond 75.1、OJBench 27.1。
- 开源 base + post-trained 权重；定位"开源 agentic intelligence"。

## 原始链接
- url: https://arxiv.org/abs/2507.20534
- pdf_url: https://arxiv.org/pdf/2507.20534
- github_url: https://github.com/MoonshotAI/Kimi-K2

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/kimi-k2-2507.20534.pdf
