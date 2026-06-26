---
title: "LongCat-Flash-Prover: Advancing Native Formal Reasoning via Agentic Tool-Integrated Reinforcement Learning"
org: 美团 Meituan (LongCat Team)
country: China
date: 2026-03
type: paper
categories: [后训练, agentic训练, 架构]
url: https://arxiv.org/abs/2603.21065
pdf_url: https://arxiv.org/pdf/2603.21065
github_url: https://github.com/meituan-longcat
downloaded: [longcat-flash-prover.pdf]
---

## 一句话定位
美团 LongCat-Flash-Prover，560B MoE，通过 agentic 工具集成 RL 推进 Lean4 原生形式化推理，提出 HisPO 算法稳定长程 MoE RL。

## 摘要
LongCat-Flash-Prover（arXiv 2026-03-22，作者 Jianing Wang 等 27 人）是 560B 旗舰开源 MoE 模型，通过 agentic tool-integrated reasoning (TIR) 推进 Lean4 中的原生形式化推理。把原生形式化推理任务分解为 auto-formalization、sketching、proving 三种独立能力，并提出 Hybrid-Experts Iteration Framework 扩展高质量任务轨迹（informal→formal statement、whole-proof、lemma-style sketch）。在 agentic RL 中提出 Hierarchical Importance Sampling Policy Optimization (HisPO)，用梯度掩码策略考虑 policy staleness 与 train-inference 引擎差异（序列级与 token 级），稳定长程任务上的 MoE 训练；并引入定理一致性与合法性检测机制消除 reward hacking。

## 关键技术细节
- **规格**：560B 参数旗舰开源 MoE。
- **任务分解**：auto-formalization + sketching + proving 三独立形式化能力（Lean4）。
- **数据扩展-Hybrid-Experts Iteration Framework**：生成 formal statement / whole-proof / lemma-style sketch 三类轨迹。
- **RL 算法-HisPO**：Hierarchical Importance Sampling Policy Optimization，梯度掩码处理 policy staleness 与训练-推理引擎差异（sequence + token 两级），稳定长程 MoE RL。
- **防 reward hacking**：theorem consistency + legality detection 机制。
- **agentic**：tool-integrated reasoning（TIR）形式化证明。

## 原始链接
- url: https://arxiv.org/abs/2603.21065
- pdf_url: https://arxiv.org/pdf/2603.21065
- github_url: https://github.com/meituan-longcat

## 一手源存档（sources/）
- longcat-flash-prover.pdf  （PDF 不入 git，走 HF bucket）
