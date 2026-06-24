---
title: "LongCat-Flash-Thinking-2601 Technical Report"
org: 美团 Meituan (LongCat Team)
country: China
date: 2026-01
type: paper
categories: [架构, AI infra, 后训练, agentic训练, 预训练数据]
url: https://arxiv.org/abs/2601.16725
pdf_url: https://arxiv.org/pdf/2601.16725
github_url: https://github.com/meituan-longcat
downloaded: [longcat-flash-thinking-2601.pdf]
---

## 一句话定位
美团 LongCat-Flash-Thinking-2601，560B MoE 推理模型，主打 agentic 推理（搜索/工具/TIR），采用"领域并行专家训练 + 后续融合"的统一训练框架与端到端协同设计。

## 摘要
LongCat-Flash-Thinking-2601（arXiv 2026-01-23，作者 "Meituan LongCat Team"，166 人）是一款 560B 参数开源 MoE 推理模型，具备强 agentic 推理能力，在 agentic search、agentic tool use、tool-integrated reasoning 等广泛 agentic benchmark 上达开源 SOTA，并对复杂工具交互与噪声真实环境展现强泛化与稳健性。其能力源于统一训练框架：domain-parallel expert training + 后续 fusion（融合），叠加从预训练到后训练的数据构造、环境、算法、基础设施端到端协同设计。复杂工具使用的强泛化来自对 environment scaling 与有原则任务构造的深入探索；为优化长尾偏斜生成与多轮 agentic 交互、实现稳定训练做了专门设计。同系列 2026 H1 还有 LongCat-Flash-Prover（arXiv 2026-03）与 LongCat-Next（arXiv 2026-03，见独立条目）。

## 关键技术细节
- **规格**：560B 参数开源 MoE 推理模型。
- **训练框架**：domain-parallel expert training（领域并行专家训练）+ subsequent fusion（后续融合）。
- **协同设计**：数据构造 + 环境 + 算法 + 基础设施端到端 co-design，覆盖 pre-training → post-training。
- **agentic 能力**：agentic search / agentic tool use / tool-integrated reasoning 开源 SOTA；噪声真实环境稳健。
- **环境/任务**：对 environment scaling 与 principled task construction 深入探索，驱动复杂工具使用泛化。
- **训练稳定性**：针对长尾偏斜生成、多轮 agentic 交互的稳定训练做专门优化。

## 原始链接
- url: https://arxiv.org/abs/2601.16725
- pdf_url: https://arxiv.org/pdf/2601.16725
- github_url: https://github.com/meituan-longcat

## 本地落盘文件
- ../../../sources/llm/2026/longcat-flash-thinking-2601.pdf
